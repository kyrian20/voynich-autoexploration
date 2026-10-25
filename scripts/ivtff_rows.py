#!/usr/bin/env python3
"""Additive IVTFF multi-row projection; frozen single-row lexer is unchanged.

The historical `ivtff_lossless.tokens` API projects one physical row or one
complete continuation chain. This adapter supports sequences containing
independent rows as well as complete continuation chains, without concatenating
words across independent physical rows. It does not validate folio/locus IDs:
callers must supply rows in source order from the intended scope.
"""
from __future__ import annotations

from scripts.ivtff_lossless import Payload, tokens


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
        if '\n' in payload.raw or '\r' in payload.raw:
            raise ValueError('Physical newline inside an IVTFF row')

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
