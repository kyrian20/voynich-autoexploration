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
    # Independent IVTFF physical rows are legal and MUST NOT concatenate
    # adjacent word fragments. The previous implementation rejected them.
    assert tokens([lex('ab.cd'), lex('ef.gh')]) == ['ab', 'cd', 'ef', 'gh']
    assert tokens([lex('a'), lex('b/'), lex('/c'), lex('d')]) == ['a', 'bc', 'd']
    assert tokens([lex('a/'), lex('/b'), lex('c/'), lex('/d')]) == ['ab', 'cd']
    assert tokens([lex('a/'), lex('/b/'), lex('/c')]) == ['abc']
    assert tokens([lex('da /'), lex('/ iin.or'), lex('chedy')]) == ['daiin', 'or', 'chedy']
    assert tokens([lex('a'), lex(''), lex('b')]) == ['a', 'b']
    for broken in (
        [lex('a/'), lex('b')],
        [lex('a'), lex('/b')],
        [lex('a/'), lex('/b'), lex('/c')],
        [lex('a/'), lex('/b/'), lex('c')],
    ):
        try:
            tokens(broken)
        except ValueError:
            pass
        else:
            raise AssertionError('Broken continuation chain accepted')

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
