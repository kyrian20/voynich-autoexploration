#!/usr/bin/env python3
"""Additive IVTFF multi-row projection; frozen single-row lexer is unchanged.

The historical `ivtff_lossless.tokens` API projects one physical row or one
complete continuation chain. This adapter supports sequences containing
independent rows as well as complete continuation chains, without concatenating
words across independent physical rows. It does not validate folio/locus IDs:
callers must supply rows in source order from the intended scope.
"""
from __future__ import annotations

import re

from scripts.ivtff_lossless import Payload, lex, tokens

# Syntax-only guard for caller-supplied physical folio labels. This does not
# authenticate their association with source rows or the reserved-leaf split.
FOLIO_LABEL_RE = re.compile(r'f(?:[0-9]+[rv][1-6]?|Ros)')


def _reject_non_ascii_high_ascii(spans) -> None:
    """Reject Unicode decimal lookalikes accepted by the frozen lexer.

    The historical lexer uses Python's Unicode-aware \\d. This additive guard
    checks parsed code spans, including ligatures and *all* alternatives,
    without rejecting arbitrary digits in free-text IVTFF comments.
    """
    for span in spans:
        if span.kind == 'high_ascii' and not span.raw[1:-1].isascii():
            raise ValueError('Non-ASCII digits in IVTFF high-ASCII code')
        _reject_non_ascii_high_ascii(span.children)
        for option in span.options:
            _reject_non_ascii_high_ascii(option)


def tokens_rows(payloads: list[Payload], **policy) -> list[str]:
    """Project physical rows, joining only explicitly paired slash continuations.

    A row ending in '/' must be followed immediately by a row starting in '/'.
    Independent rows are projected separately, preserving a word boundary.
    Existing lexer diagnostics and policy validation are delegated unchanged.
    """
    # The frozen lexer can absorb a physical newline inside an angle-bracket
    # comment without emitting its usual newline diagnostic. This additive
    # adapter must fail closed rather than joining two physical rows.
    for payload in payloads:
        if not isinstance(payload, Payload):
            raise TypeError('Expected a lexed IVTFF Payload')
        if not isinstance(payload.raw, str):
            raise TypeError('IVTFF Payload raw row must be text')
        # Python splitlines() also treats VT, FF, record separators, NEL and
        # Unicode line/paragraph separators as physical line boundaries. A
        # comment can hide these from the frozen single-row lexer, so reject
        # them here before any analytical projection or continuation joining.
        if any(mark in payload.raw for mark in '\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029'):
            raise ValueError('Physical newline inside an IVTFF row')
        # Payload/Span are mutable public dataclasses. A stale raw string,
        # altered span, or discarded diagnostic must never be projected as
        # if it were the exact physical source row. Re-lex without touching
        # the frozen historical lexer or any archived experiment.
        checked = lex(payload.raw)
        if payload.spans != checked.spans or payload.diagnostics != checked.diagnostics:
            raise ValueError('IVTFF Payload spans/diagnostics disagree with raw row')
        _reject_non_ascii_high_ascii(checked.spans)

    output: list[str] = []
    chain: list[Payload] = []

    for payload in payloads:
        leading = bool(payload.spans and payload.spans[0].kind == 'continuation')
        if not chain:
            if leading:
                raise ValueError('Incomplete or unpaired continuation chain')
            chain = [payload]
            continue

        trailing = bool(chain[-1].spans and chain[-1].spans[-1].kind == 'continuation')
        if trailing:
            if not leading:
                raise ValueError('Incomplete or unpaired continuation chain')
            chain.append(payload)
        else:
            if leading:
                raise ValueError('Incomplete or unpaired continuation chain')
            output.extend(tokens(chain, **policy))
            chain = [payload]

    if chain:
        output.extend(tokens(chain, **policy))
    elif policy:
        # Empty input still must reject invalid analytical policies.
        tokens([], **policy)
    return output


def tokens_scoped_rows(
    rows: list[tuple[str, str, Payload]], **policy
) -> list[str]:
    """Project rows without joining continuations across sources or folios.

    Each input is (source_id, folio_id, lexed_payload), in physical source
    order. Both IDs are caller-supplied provenance labels, NOT independently
    authenticated hashes or validated IVTFF metadata. A scope may occur only
    in one contiguous block; an interrupted scope is rejected, not silently
    reassembled. This guard does not establish holdout eligibility.
    """
    output: list[str] = []
    scope = None
    group: list[Payload] = []
    seen: set[tuple[str, str]] = set()

    for source_id, folio_id, payload in rows:
        if not all(isinstance(v, str) and v.strip() and v == v.strip()
                   for v in (source_id, folio_id)):
            raise ValueError('Nonempty, exact source and folio IDs required')
        if not source_id.isprintable():
            raise ValueError('Source ID contains control or invisible characters')
        if not FOLIO_LABEL_RE.fullmatch(folio_id):
            raise ValueError('Invalid IVTFF physical folio label')
        if not isinstance(payload, Payload):
            raise TypeError('Expected a lexed IVTFF Payload')
        next_scope = (source_id, folio_id)
        if next_scope != scope:
            if next_scope in seen:
                raise ValueError('Non-contiguous repeated source/folio scope')
            if group:
                output.extend(tokens_rows(group, **policy))
            group = []
            scope = next_scope
            seen.add(next_scope)
        group.append(payload)

    if group:
        output.extend(tokens_rows(group, **policy))
    else:
        tokens_rows([], **policy)  # Validate policies even for empty input.
    return output
