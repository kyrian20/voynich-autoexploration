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
