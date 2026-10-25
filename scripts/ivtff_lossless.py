#!/usr/bin/env python3
"""Lossless payload lexer, with explicit derived views; not a full IVTFF validator.

Reference: IVTFF document issue 2.0.2, §§5.6, 6.6–6.8. No decoding of high-ASCII
glyph identities is attempted. Existing experiment tokenizers remain unchanged.
Offsets are Python character offsets in the exact input payload, end-exclusive.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re


@dataclass
class Span:
    kind: str
    raw: str
    start: int
    end: int
    children: list = field(default_factory=list)
    options: list = field(default_factory=list)


@dataclass
class Payload:
    raw: str
    spans: list[Span]
    diagnostics: list[dict]


def lex(raw: str) -> Payload:
    diagnostics = []

    def flag(code, start, end):
        diagnostics.append({'code': code, 'start': start, 'end': end})

    def scan(start, stop):
        spans = []
        i = start
        while i < stop:
            ch = raw[i]
            end, children, options = i + 1, [], []
            kind = 'glyph'
            if ch in '\r\n':
                kind = 'unresolved'
                flag('physical_newline_in_payload', i, end)
            elif ch.isspace():
                kind = 'layout_whitespace'
            elif ch in '.,':
                kind = 'word_space' if ch == '.' else 'uncertain_space'
            elif ch == '<':
                close = raw.find('>', i + 1, stop)
                if close < 0:
                    end, kind = stop, 'unresolved'
                    flag('unclosed_comment', i, end)
                else:
                    end = close + 1
                    value = raw[i:end]
                    if value.startswith('<!'):
                        kind = 'comment'
                        if len(value) > 80:
                            flag('comment_too_long', i, end)
                    elif value in ('<->', '<~>'):
                        kind = 'drawing_space'
                    elif value in ('<%>', '<$>'):
                        kind = 'paragraph_start' if value == '<%>' else 'paragraph_end'
                    elif re.fullmatch(r'<@[A-Z]=[^<>\s]>', value):
                        kind = 'text_tag'
                    else:
                        kind = 'unresolved'
                        flag('unsupported_inline_tag', i, end)
            elif ch in '[{':
                closing = ']' if ch == '[' else '}'
                close = raw.find(closing, i + 1, stop)
                if close < 0:
                    end, kind = stop, 'unresolved'
                    flag('unclosed_alternative' if ch == '[' else 'unclosed_ligature', i, end)
                else:
                    end = close + 1
                    if ch == '{':
                        kind = 'ligature'
                        children = scan(i + 1, close)
                        if not children or any(s.kind not in {'glyph', 'high_ascii'} for s in children):
                            flag('invalid_ligature_content', i, end)
                    else:
                        kind = 'alternatives'
                        if '[' in raw[i + 1:close]:
                            flag('nested_alternative', i, end)
                        cuts = [i + 1] + [p + 1 for p in range(i + 1, close) if raw[p] == ':']
                        stops = [p - 1 for p in cuts[1:]] + [close]
                        options = [scan(a, b) for a, b in zip(cuts, stops)]
                        if len(options) not in (2, 3):
                            flag('alternative_arity', i, end)
            elif ch == '@':
                match = re.match(r'@(\d{3});', raw[i:stop])
                if match:
                    end, kind = i + len(match.group()), 'high_ascii'
                    if not 128 <= int(match[1]) <= 255:
                        flag('high_ascii_out_of_range', i, end)
                else:
                    kind = 'unresolved'
                    flag('malformed_high_ascii', i, end)
            elif ch == '?':
                kind = 'unreadable'
            elif ch == '/':
                kind = 'continuation'
                if i not in (0, len(raw) - 1):
                    flag('interior_continuation', i, end)
            elif ch in '>]};':
                kind = 'unresolved'
                flag('unmatched_delimiter', i, end)
            spans.append(Span(kind, raw[i:end], i, end, children, options))
            i = end
        return spans

    spans = scan(0, len(raw))
    assert ''.join(s.raw for s in spans) == raw
    return Payload(raw, spans, diagnostics)


def tokens(payloads: list[Payload], *, uncertain_space='split', alternatives='primary', ligatures='expand') -> list[str]:
    """Declared analytical view. Reject unresolved input; preserve opaque glyph codes.

    Excluding an uncertain span excludes its entire containing word, preventing
    artificial concatenation of fragments. Whitespace/comments do not create
    manuscript word spaces. Commas may split or join, by explicit policy.
    """
    if uncertain_space not in {'split', 'join'} or alternatives not in {'primary', 'exclude_word'} or ligatures not in {'expand', 'opaque'}:
        raise ValueError('Unknown analysis policy')
    if any(p.diagnostics for p in payloads):
        raise ValueError('Unresolved lexical diagnostics; refuse analytical projection')
    # Continuation pairs must be adjacent, but ordinary independent physical
    # lines may occur before, between and after complete continuation chains.
    # Do not concatenate words across an ordinary physical-line boundary.
    for n, payload in enumerate(payloads):
        leading = bool(payload.spans and payload.spans[0].kind == 'continuation')
        trailing = bool(payload.spans and payload.spans[-1].kind == 'continuation')
        previous_trailing = bool(n > 0 and payloads[n - 1].spans and
                                 payloads[n - 1].spans[-1].kind == 'continuation')
        next_leading = bool(n + 1 < len(payloads) and payloads[n + 1].spans and
                            payloads[n + 1].spans[0].kind == 'continuation')
        if leading != previous_trailing or trailing != next_leading:
            raise ValueError('Incomplete or unpaired continuation chain')
    output, word = [], []
    exclude = False

    def flush():
        nonlocal exclude
        if word and not exclude:
            output.append(''.join(word))
        word.clear()
        exclude = False

    def visit(spans):
        nonlocal exclude
        for span in spans:
            if span.kind in {'word_space', 'drawing_space'} or (span.kind == 'uncertain_space' and uncertain_space == 'split'):
                flush()
            elif span.kind == 'alternatives':
                if alternatives == 'exclude_word':
                    exclude = True
                else:
                    visit(span.options[0])
            elif span.kind == 'ligature':
                if ligatures == 'opaque':
                    word.append(span.raw)
                else:
                    visit(span.children)
            elif span.kind in {'glyph', 'high_ascii', 'unreadable'}:
                word.append(span.raw)

    for n, payload in enumerate(payloads):
        if n and not (payload.spans and payload.spans[0].kind == 'continuation'):
            flush()  # ordinary physical-line boundary, not a word continuation
        visit(payload.spans)
    flush()
    return output
