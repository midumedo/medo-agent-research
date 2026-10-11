无尾缀的默认填充`.md`， 特殊的我会用“`” 包起来
# 核心文档
vibe coding相关文档，部分文档是重要但不相关的。

## AGENTS.md
完全同类：CLAUDE，GEMINI （最新CLAUDE已经支持 `AGENTS.md` instead of  `CLAUDE.md`）
一定吸纳的：THISIS，BREIF
考虑吸纳：ARCHITECTURE

## ARCHITECTURE.md
考虑被AGENTS吸纳，
考虑独立的原因是：方便`ARCHITECTURE.md`被一个专用skill进行维护

## CONVENTIONS.md
规范，有更好的名字吗？
同类：
吸纳：STYLE、LIMITATIONS
考虑吸纳：CONTEXT

## CONTEXT.md
主要是 有个skill：“grill-with-docs”采用了这个命名，
完全同类：GLOSSARY



---
# 文档枚举
AGENTS（CLAUDE，GEMINI，...，本质相同）
README
THISIS
BREIF
TREE
INDEX

ARCHITECTURE
TRADOFFS
CONVENTIONS
STYLE
LIMITATIONS
CONTEXT or GLOSSARY

MEMORY
USER
AGENTS.local

EXPERIMENTS
DECISIONS
ADR/
dialogue/

PROBLEMS
ROADMAP

registry
outline

旧时代的：
README
SECURITY
CHANGELOG

---

> 本文件是**候选名字清单（意图）**，不是结论：这里只是「想过哪些名字」，不代表真实仓库里有这些文件。
> 实测（哪些名字在 18 个样本仓里真实存在、字节数、角色、出处）见 index.csv 与 ds/；本阶段说明见 README.md。


SOUL.md 423 / BOOTSTRAP.md 247 / IDENTITY.md 149 / USER.md 

## 枚举
分类仅供参考，最终还是要根据

### 纲领 charter · 上电帧
AGENTS（boot image）；CLAUDE / GEMINI / .cursorrules / copilot-instructions（shim）；SOUL；
IDENTITY / THISIS；README（身份卡段，mirror）；VISION / MISSION / PRINCIPLES / VALUES；红线章（≤10 条）

### 图谱 atlas · 上电帧
INDEX；registry；SKILLS 清单；MANIFEST；CHEATSHEET；gen：TREE、BRIEF、outline

### 术语 lexicon · 上电帧（负载词）+ 燃料（全量）
GLOSSARY；术语表；命名词典；缩写表；DOMAIN-GLOSSARY

### 律条 codex · 变更约束（写边界）
CONVENTIONS；STYLE（并入）；CODING-STANDARDS；lint 规则说明；SECURITY（政策）；LIMITATIONS（禁令）；
TESTING（要求）；CODE-REVIEW（标准）；CONTRIBUTING（约束段）；COMMIT / BRANCH / PR 规范；
VERSIONING / SEMVER 政策；COMPATIBILITY（政策段）

### 形制 schematic · 上电帧（骨架）+ 燃料（细节）
ARCHITECTURE（含"原则与取舍"章）；DESIGN；SPECS（未裁决）；DOMAIN / DOMAIN-MODEL；DATA-MODEL；
DIAGRAMS；OVERVIEW；FAQ；PERFORMANCE（现状）；COMPATIBILITY（现状）；MODELS；LIMITATIONS（能力边界）；
gen：API / OpenAPI / typedoc / DEPENDENCIES

### 规程 runbook · 变更约束（多迁技能）
CONTRIBUTING（步骤段）；RELEASE / RELEASE-CHECKLIST；DEPLOY；INSTALL / SETUP / GETTING-STARTED；
ONBOARDING；DEBUGGING / TROUBLESHOOTING；MIGRATION / UPGRADE；HOWTO；TUTORIAL；EXAMPLES；
PLAYBOOK / RUNBOOK / OPERATIONS；TESTING（怎么跑）；BENCHMARK（怎么测）；SECURITY-disclosure

### 议定 ledger · 燃料
ADR/；RFC/；PROPOSALS/（已定稿）；SPECS（已裁决）；POSTMORTEM（结论）；RETRO（决议）；EXPERIMENTS（结论）；gen：DECISIONS 索引

### 时务 board · 上电帧（使命摘要）+ 燃料
ROADMAP；PROBLEMS；LESSONS（原 MEMORY，scope=repo）；TODO（文档侧）；KNOWN-ISSUES；PLANS（已定稿）；
BACKLOG；MILESTONES；RISKS；EXPERIMENTS（计划）；RETRO（行动项）；METRICS；DASHBOARD；sprint/任务板导出（gen）

### 史册 archive · 燃料（禁预热）
dialogue/；incidents/；POSTMORTEM（时间线）；CHANGELOG（gen）；RELEASE-NOTES；MEETING-NOTES；STANDUP；
LOGS；EXPERIMENTS（原始）；BENCHMARKS（结果）；DATASETS；PAPERS/（immutable）；sources/（immutable）；
THIRD-PARTY；会话导出

### 草稿 scratch · 语料外（仅作者）
NOTES/；WIP；DRAFT；scratch/；未命名笔记；脑图；agent 未审提案（proposed）；临时 plans（未定稿）；本研究工作稿（subject=meta）

### 自述 self · 上电帧（身份）
USER；MEMORY（user 级）；AGENTS.local；PERSONA；LOCAL；ENVIRONMENT；个人 config；个人 skills 清单

### 语料外 oob
LICENSE；NOTICE；AUTHORS / CONTRIBUTORS；CITATION.cff；FUNDING.yml；CODE_OF_CONDUCT；SUPPORT；
SECURITY（对外披露页）；VENDOR 条款

AGENTS.md、CONVENTIONS.md、docs/decisions/、TASK.md、INDEX.md
MANIFEST.md