"""Read or rewrite actual Markdown/HTML link destinations without touching code."""

import re


def _without_code(text):
    """Keep offsets unchanged while masking fenced and inline code literals."""
    characters = list(text)
    fence = None
    offset = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        hidden = fence is not None
        if fence is not None:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
        elif marker:
            fence = (marker[1][0], len(marker[1]))
            hidden = True
        if hidden:
            for index in range(offset, offset + len(line)):
                if characters[index] not in "\r\n":
                    characters[index] = " "
        offset += len(line)
    visible = "".join(characters)
    position = 0
    while True:
        opening = re.search(r"(?<!\\)`+", visible[position:])
        if not opening:
            break
        start = position + opening.start()
        end = position + opening.end()
        count = end - start
        closing = re.search(r"(?<!`)`{" + str(count) + r"}(?!`)", visible[end:])
        if closing:
            stop = end + closing.end()
            for index in range(start, stop):
                if characters[index] not in "\r\n":
                    characters[index] = " "
            position = stop
        else:
            position = end
    return "".join(characters)


def _map_destination(value, resolver):
    leading = value[:len(value) - len(value.lstrip())]
    token = value[len(leading):]
    if token.startswith("<") and ">" in token:
        end = token.index(">")
        destination = token[1:end]
        replacement = resolver(destination)
        return leading + "<" + replacement + ">" + token[end + 1:] if replacement is not None else value
    title = re.search(r"\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\))\s*$", token)
    destination = token[:title.start()] if title else token.rstrip()
    suffix = token[len(destination):]
    replacement = resolver(destination)
    return leading + replacement + suffix if replacement is not None else value


def rewrite_links(text, resolver, *, images_only=False):
    """Call resolver once per destination; None preserves its original text.

    Handles inline Markdown destinations (including balanced parentheses),
    reference definitions and quoted HTML img src. With images_only, visit
    only image destinations and their used definitions. Literal paths in
    prose or code are not links. URL parsing/encoding belongs to the caller.
    """
    visible = _without_code(text)
    replacements = []
    image_labels = set()
    if images_only:
        for image in re.finditer(r"(?<!\\)!\[([^\]\n]*)\](?:\[([^\]\n]*)\])?(?!\()", visible):
            image_labels.add(" ".join((image[2] or image[1]).split()).casefold())
    for match in re.finditer(r"(?<!\\)\]\(", visible):
        # Require an opening label on the same line rather than treating an
        # arbitrary mathematical ]( sequence as a Markdown destination.
        line_start = visible.rfind("\n", 0, match.start()) + 1
        if "[" not in visible[line_start:match.start()]:
            continue
        if images_only:
            depth = 1
            opening = None
            for index in range(match.start() - 1, line_start - 1, -1):
                if index > 0 and visible[index - 1] == "\\":
                    continue
                if visible[index] == "]":
                    depth += 1
                elif visible[index] == "[":
                    depth -= 1
                    if depth == 0:
                        opening = index
                        break
            if opening is None or opening == 0 or visible[opening - 1] != "!" or (opening > 1 and visible[opening - 2] == "\\"):
                continue
        start = match.end()
        depth, quote, angle, escaped = 1, None, False, False
        for index in range(start, len(text)):
            char = text[index]
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if quote:
                if char == quote:
                    quote = None
                continue
            if angle:
                if char == ">":
                    angle = False
                continue
            if char == "<":
                angle = True
            elif char in "\"'" and index > start and text[index - 1].isspace():
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    replacements.append((start, index, _map_destination(text[start:index], resolver)))
                    break
            elif char == "\n":
                break
    for match in re.finditer(r"<img\b[^>]*?\s+src\s*=\s*([\"'])(.*?)\1", visible, re.I | re.S):
        start, end = match.span(2)
        value = text[start:end]
        mapped = resolver(value)
        if mapped is not None:
            replacements.append((start, end, mapped))
    for match in re.finditer(r"^ {0,3}\[([^\]\n]+)\]:[ \t]*(.+)$", visible, re.M):
        if images_only and " ".join(match[1].split()).casefold() not in image_labels:
            continue
        start, end = match.span(2)
        replacements.append((start, end, _map_destination(text[start:end], resolver)))
    previous_start = len(text) + 1
    for start, end, replacement in sorted(replacements, reverse=True):
        if end > previous_start:
            continue
        text = text[:start] + replacement + text[end:]
        previous_start = start
    return text
