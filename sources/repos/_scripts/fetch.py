"""抓取或更新一个第三方仓库快照。

走 `codeload.github.com` 的 tar.gz（本环境 git 协议慢），因此落盘树**不含 `.git` 历史**。
提交 sha 由 GitHub API 单独取；取不到就留空并标注，**不拿今天的 main 冒充落盘版本**。

多版本规则：更新一个已有目录时，先把旧快照改名 `<id>@<旧sha12>`，再解压新的到 `<id>/`。
账本因此一行一快照，旧行保留，既有结论仍能回溯到当时的版本。旧 sha 没记过时退化为
`<id>@unknown-<今日>`，仍然是「这是旧的那一份」而不是假装它有版本号。

Usage:
    fetch.py <owner/name> [--branch main] [--drop-old]
    fetch.py <id>                     # 已在 _commits.json 里的目录名
    fetch.py --all                    # 按账本更新全部（跳过没有本地目录的行）
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repos  # noqa: E402

API = "https://api.github.com/repos/{slug}/commits?per_page=1"
REPO_API = "https://api.github.com/repos/{slug}"
CODELOAD = "https://codeload.github.com/{slug}/tar.gz/refs/heads/{branch}"
UA = {"User-Agent": "rivet-sources-repos-fetch"}


def _get(url, timeout=60):
    request = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def default_branch(slug):
    """仓库真正的默认分支名；问不到返回 `""`（调用方回落到 main）。

    写死 `main` 会 404——deepseek-ai/deepseek-harness 的默认分支就不是它，实测过。
    """
    try:
        data = json.loads(_get(REPO_API.format(slug=slug)).decode("utf-8"))
    except Exception:
        return ""
    return (data or {}).get("default_branch") or ""


def default_branch_sha(slug, branch=None):
    """默认分支最新提交 sha；取不到返回 `""`（限流、网络、仓库不存在都算取不到）。"""
    try:
        raw = _get(API.format(slug=slug))
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        return ""
    if isinstance(data, dict) and data.get("sha"):  # 单提交端点
        return data["sha"]
    if isinstance(data, list) and data:
        return data[0].get("sha") or ""
    return ""


def download(slug, branch, dest):
    """下载并解压 `slug` 的 `branch` 到 `dest/`。返回 False 表示没拿到完整快照。"""
    url = CODELOAD.format(slug=slug, branch=branch)
    tar_path = os.path.join(os.path.dirname(repos.BASE), f".fetch-{slug.replace('/', '_')}.tar.gz")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=900) as response:
            with open(tar_path, "wb") as out:
                shutil.copyfileobj(response, out)
    except Exception as exc:
        print(f"✗ 下载失败 {url}: {exc}")
        return False

    size = os.path.getsize(tar_path)
    if size < 20000:
        print(f"✗ 下载体积异常（{size}B）: {url}")
        os.remove(tar_path)
        return False

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            # `filter="data"` 挡住 tar-slip（绝对路径、`..`、符号链接逃逸）。3.12+ 才有该参数。
            try:
                tar.extractall(dest, filter="data")
            except TypeError:
                tar.extractall(dest)
    except Exception as exc:
        # 超时截断的 tar 会解到一半就报错——这时 dest 里是**残缺树**，必须隔离，
        # 否则下游会把不完整的 checkout 当成完整的读。
        print(f"✗ 解压失败（tar 可能被截断）: {exc}")
        return False
    finally:
        if os.path.exists(tar_path):
            os.remove(tar_path)

    # GitHub 的 tar 顶层是 `<repo>-<sha>/`，剥掉它。
    entries = [e for e in os.listdir(dest) if not e.startswith(".")]
    if len(entries) == 1 and os.path.isdir(os.path.join(dest, entries[0])):
        inner = os.path.join(dest, entries[0])
        for name in os.listdir(inner):
            shutil.move(os.path.join(inner, name), os.path.join(dest, name))
        os.rmdir(inner)
    return True


def quarantine(partial_dir, stamp):
    """把残缺解压的目录改名为 `_partial-<名字>-<日期>`，让它不再像一份可用的 checkouts。"""
    name = f"_partial-{os.path.basename(partial_dir.rstrip(os.sep))}-dl-failed-{stamp}"
    target = os.path.join(repos.BASE, name)
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.move(partial_dir, target)
    return name


def changelog(line):
    """把事件追加到 `CHANGELOG.md`（只追加，不重排）。"""
    path = os.path.join(repos.BASE, "CHANGELOG.md")
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(line if line.endswith("\n") else line + "\n")


def fetch(token, branch=None, drop_old=False, write_changelog=True):
    commits = repos.read_commits()
    today = datetime.date.today().isoformat()

    if "/" in token:
        slug = token
        ident = slug.split("/")[-1]
    else:
        ident = token
        slug = (commits.get(ident) or {}).get("slug") or ""
        if not slug:
            print(f"✗ {token}: 账本里没有它的上游标识，请用 owner/name 形式")
            return False

    # 没显式指定分支时问 API 要默认分支——写死 main 会 404。
    branch = branch or default_branch(slug) or "main"

    dest = os.path.join(repos.BASE, ident)
    existed = os.path.isdir(dest)
    old_sha = (commits.get(ident) or {}).get("sha") or ""

    new_sha = default_branch_sha(slug, branch)
    # 账本里的旧 sha 只存 12 位，API 给的是 40 位——按前缀比，否则同版本也会被当成「变了」
    # 而白改名一次（本轮实测踩到：upstream 没动，却生出了一个重复的历史快照目录）。
    if existed and old_sha and new_sha and old_sha[:12] == new_sha[:12]:
        print(f"= {ident}: 已是 {new_sha[:12]}，无需更新")
        return True

    if existed:
        if old_sha:
            old_name = f"{ident}@{old_sha[:12]}"
        else:
            old_name = f"{ident}@unknown-{today}"
        print(f"→ 旧快照改名 {ident}/ → {old_name}/")
        shutil.move(dest, os.path.join(repos.BASE, old_name))
        if drop_old:
            shutil.rmtree(os.path.join(repos.BASE, old_name))
            print(f"  （--drop-old：已删除 {old_name}/）")
    else:
        os.makedirs(dest, exist_ok=True)

    ok = download(slug, branch, dest)
    if not ok:
        if existed:
            # 下载/解压失败时把旧的挪回来，别让目录停在半新半旧的状态。
            if os.path.exists(dest):
                shutil.rmtree(dest)
            fallback = old_name if existed else None
            if fallback and os.path.isdir(os.path.join(repos.BASE, fallback)):
                shutil.move(os.path.join(repos.BASE, fallback), dest)
                print(f"← 已还原 {ident}/（原快照回位）")
        else:
            if os.path.exists(dest):
                shutil.rmtree(dest)
        return False

    commits[ident] = {
        "slug": slug,
        "sha": new_sha,
        "date": today,
    }
    repos.write_commits(commits)
    print(f"✓ {ident}: {slug} {new_sha[:12] or '(指纹未取到)'}")

    if write_changelog:
        prior = f"，旧快照存为 `{old_name}/`" if existed and not drop_old else ""
        sha_text = new_sha[:12] if new_sha else "sha 未取到（API 限流）"
        changelog(f"- {today} · 抓取 · `{ident}` · `{slug}`（{sha_text}）{prior}。")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="owner/name 或账本里的目录名")
    ap.add_argument("--branch", default=None, help="默认问 API 取默认分支，取不到回落 main")
    ap.add_argument("--drop-old", action="store_true", help="不保留旧快照（默认保留为 <id>@<sha12>/）")
    ap.add_argument("--all", action="store_true", help="按账本更新全部有本地目录的行")
    ap.add_argument("--no-changelog", action="store_true")
    args = ap.parse_args()

    if args.all:
        targets = [row["id"] for row in repos.read_index()
                   if row["id"] in repos.scan_dirs()]
    elif args.target:
        targets = [args.target]
    else:
        ap.error("给一个目标，或用 --all")

    failed = []
    for token in targets:
        if not fetch(token, branch=args.branch, drop_old=args.drop_old,
                     write_changelog=not args.no_changelog):
            failed.append(token)
    if failed:
        print(f"\n{len(failed)} 个未成功：{'、'.join(failed)}")
        raise SystemExit(1)
    print(f"\n完成：{len(targets)} 个")


if __name__ == "__main__":
    main()
