#!/usr/bin/env python3
"""Specification-grounded synthetic fixtures for the lossless lexical layer.

Sections refer to IVTFF document issue 2.0.2. Derived views are explicit analysis
choices, not normative word definitions. Historical tokenizers are untouched.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ivtff_lossless import lex, tokens
from scripts.ivtff_rows import tokens_rows, tokens_scoped_rows


FIXTURES = [
    ('F01', '6.6', 'daiin.chedy', ['daiin', 'chedy']),
    ('F02', '6.6', 'or,y', ['or', 'y']),
    ('F03', '6.6', 'qo[ke:te]dy', ['qokedy']),
    ('F04', '6.6', 'dai{ch}in', ['daichin']),
    ('F05', '5.7.2', 'qo<!x>dy.or', ['qody', 'or']),
    ('F06a', '6.7', 'or<->dy', ['or', 'dy']),
    ('F06b', '6.7', 'or<~>dy', ['or', 'dy']),
    ('F07', '6.9', '<%>daiin.or<$>', ['daiin', 'or']),
    ('F12', '6.6', '@140;.daiin', ['@140;', 'daiin']),
    ('F13', '6.6', 'qo{@140;}dy', ['qo@140;dy']),
    ('F14', '6.6', 'qo[{ch}:sh]dy', ['qochdy']),
    ('F15', '6.6', 'daiin[:y]', ['daiin']),
    ('F16', '5.6', 'da ii n.or', ['daiin', 'or']),
    ('F17', '6.6', 'q?dy.???', ['q?dy', '???']),
    ('F18', '6.8', '<@L=B>daiin', ['daiin']),
    ('F19', '5.7.2', 'or<! / { [ @12; >dy', ['ordy']),
]


def check_offsets(payload):
    def visit(spans):
        for span in spans:
            assert payload.raw[span.start:span.end] == span.raw, span
            visit(span.children)
            for option in span.options:
                visit(option)
    assert ''.join(x.raw for x in payload.spans) == payload.raw
    visit(payload.spans)


def main():
    for name, section, raw, expected in FIXTURES:
        payload = lex(raw)
        check_offsets(payload)
        assert not payload.diagnostics, (name, section, payload.diagnostics)
        assert tokens([payload]) == expected, (name, tokens([payload]))
    assert tokens([lex('or,y')], uncertain_space='join') == ['ory']
    assert tokens([lex('qo[ke:te]dy.or')], alternatives='exclude_word') == ['or']
    assert tokens([lex('qo{ch}dy')], ligatures='opaque') == ['qo{ch}dy']
    # F08: no artificial word space at the physical wrap. §6.6.
    assert tokens([lex('dai /'), lex('/ in.or')]) == ['daiin', 'or']
    # Additive adapter handles independent rows without modifying the frozen
    # lexer used by historical snapshots. No cross-row word concatenation.
    assert tokens_rows([lex('ab.cd'), lex('ef.gh')]) == ['ab', 'cd', 'ef', 'gh']
    assert tokens_rows([lex('a'), lex('b/'), lex('/c'), lex('d')]) == ['a', 'bc', 'd']
    assert tokens_rows([lex('a/'), lex('/b'), lex('c/'), lex('/d')]) == ['ab', 'cd']
    assert tokens_rows([lex('a/'), lex('/b/'), lex('/c')]) == ['abc']
    assert tokens_rows([lex('da /'), lex('/ iin.or'), lex('chedy')]) == ['daiin', 'or', 'chedy']
    assert tokens_rows([lex('a'), lex(''), lex('b')]) == ['a', 'b']
    assert tokens_rows([]) == []
    # A Payload is a mutable dataclass: a raw-row edit, changed span, or
    # discarded diagnostic used to be silently projected as different text.
    # The adapter must fail closed while the frozen historical lexer stays as-is.
    stale_raw = lex('ab')
    stale_raw.raw = 'cd'
    changed_span = lex('ab')
    changed_span.spans[0].raw = 'zz'
    lost_diagnostic = lex('a[bad')
    assert lost_diagnostic.diagnostics
    lost_diagnostic.diagnostics.clear()
    for tampered in (stale_raw, changed_span, lost_diagnostic):
        for projector in (
            lambda p: tokens_rows([p]),
            lambda p: tokens_scoped_rows([('ZL3b', 'f1r', p)]),
        ):
            try:
                projector(tampered)
            except ValueError as exc:
                assert 'disagree with raw row' in str(exc), str(exc)
            else:
                raise AssertionError('Stale or tampered IVTFF Payload accepted')
    wrong_raw_type = lex('ab')
    wrong_raw_type.raw = None
    try:
        tokens_rows([wrong_raw_type])
    except TypeError as exc:
        assert 'raw row must be text' in str(exc), str(exc)
    else:
        raise AssertionError('Non-text IVTFF raw row accepted')
    # A physical newline hidden inside an angle-bracket comment is swallowed
    # by the frozen single-row lexer; the additive row APIs must reject it.
    physical_breaks = ('\n', '\r', '\r\n', '\v', '\f', '\x1c', '\x1d',
                       '\x1e', '\x85', '\u2028', '\u2029')
    malformed_rows = [f'a<!hidden{sep}comment>b' for sep in physical_breaks]
    malformed_rows += [f'a{sep}b' for sep in physical_breaks]
    for malformed_row in malformed_rows:
        assert len(malformed_row.splitlines()) == 2
        for projector in (
            lambda p: tokens_rows([p]),
            lambda p: tokens_scoped_rows([('ZL3b', 'f1r', p)]),
        ):
            try:
                projector(lex(malformed_row))
            except ValueError as exc:
                assert 'Physical newline' in str(exc), str(exc)
            else:
                raise AssertionError('Physical newline hidden in comment accepted')
    try:
        tokens_rows(['not-a-payload'])
    except TypeError:
        pass
    else:
        raise AssertionError('Non-payload input accepted by row adapter')
    # A slash continuation may not bridge physical source/folio scopes.
    assert tokens_scoped_rows([
        ('ZL3b', 'f1r', lex('a/')),
        ('ZL3b', 'f1r', lex('/b')),
        ('ZL3b', 'f1v', lex('c')),
        ('IT2a', 'f1v', lex('d/')),
        ('IT2a', 'f1v', lex('/e')),
    ]) == ['ab', 'c', 'de']
    assert tokens_scoped_rows([]) == []
    for invalid_scoped in (
        [('ZL3b', 'f1r', lex('a/')), ('ZL3b', 'f1v', lex('/b'))],
        [('ZL3b', 'f1r', lex('a/')), ('IT2a', 'f1r', lex('/b'))],
        [('ZL3b', 'f1r', lex('a')), ('ZL3b', 'f1v', lex('b')),
         ('ZL3b', 'f1r', lex('c'))],
        [('', 'f1r', lex('a'))],
        [('ZL3b', ' ', lex('a'))],
    ):
        try:
            tokens_scoped_rows(invalid_scoped)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid source/folio scope accepted')
    try:
        tokens_scoped_rows([], uncertain_space='not-a-policy')
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid policy accepted for empty scoped input')
    try:
        tokens_scoped_rows([('ZL3b', 'f1r', 'not-lexed')])
    except TypeError:
        pass
    else:
        raise AssertionError('Non-payload input accepted')
    assert tokens_rows([lex('qo[ke:te]dy'), lex('or,y')], uncertain_space='join') == ['qokedy', 'ory']
    assert tokens_rows([lex('qo[ke:te]dy'), lex('or,y')], alternatives='exclude_word') == ['or', 'y']
    for broken in (
        [lex('a/'), lex('b')],
        [lex('a'), lex('/b')],
        [lex('a/'), lex('/b'), lex('/c')],
        [lex('a/'), lex('/b/'), lex('c')],
        [lex('a/')],
        [lex('/b')],
    ):
        try:
            tokens_rows(broken)
        except ValueError:
            pass
        else:
            raise AssertionError('Broken continuation chain accepted')
    for invalid_policy in ({'uncertain_space': 'invalid'}, {'alternatives': 'invalid'}):
        try:
            tokens_rows([], **invalid_policy)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid policy accepted for empty input')

    invalid = ['qo[te', 'qo{ch', 'q}', '@12;', '@127;', '@256;', '[x]',
               '[a:b:c:d]', '{a.b}', '{a?b}', '<!unclosed', 'or/x', 'a\nb']
    for raw in invalid:
        payload = lex(raw)
        check_offsets(payload)
        assert payload.diagnostics, raw
        try:
            tokens([payload])
        except ValueError:
            pass
        else:
            raise AssertionError(f'Invalid payload projected: {raw}')
    for wrapped in [[lex('dai/')], [lex('/in')], [lex('a/'), lex('b')]]:
        try:
            tokens(wrapped)
        except ValueError:
            pass
        else:
            raise AssertionError('Unpaired continuation accepted')
    print(f'{len(FIXTURES)} named fixtures plus policy, malformed-input, offset and continuation checks passed.')


if __name__ == '__main__':
    main()
