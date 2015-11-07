from forestanza.common import resolve_chain

DAT1 = {'_': 1, 'a': 2,
        'b': {'_': 3, 'ib': 4, 'jb': {'m': 1}},
        'c': {'ic': 5}}

class TestF_resolve_chain:
    def test_1L(self):
        assert [] == resolve_chain(DAT1, [])
        assert ['a'] == resolve_chain(DAT1, ['a'])
        assert ['b'] == resolve_chain(DAT1, ['b'])
        assert ['c'] == resolve_chain(DAT1, ['c'])
        assert ['_'] == resolve_chain(DAT1, ['z'])

    def test_2L(self):
        assert ['a'] == resolve_chain(DAT1, ['a', 'z'])
        assert ['_'] == resolve_chain(DAT1, ['c', 'z'])
        assert ['_'] == resolve_chain(DAT1, ['y', 'z'])
        assert ['b', 'ib'] == resolve_chain(DAT1, ['b', 'ib'])
        assert ['b', '_'] == resolve_chain(DAT1, ['b', 'z'])
        assert ['c', 'ic'] == resolve_chain(DAT1, ['c', 'ic'])
        assert ['_'] == resolve_chain(DAT1, ['c', 'z'])

    def test_3L(self):
        assert ['a'] == resolve_chain(DAT1, ['a', 'y', 'z'])
        assert ['_'] == resolve_chain(DAT1, ['c', 'y', 'z'])
        assert ['b', 'ib'] == resolve_chain(DAT1, ['b', 'ib', 'z'])
        assert ['b', '_'] == resolve_chain(DAT1, ['b', 'y', 'z'])
        assert ['c', 'ic'] == resolve_chain(DAT1, ['c', 'ic', 'z'])
        assert ['b', 'jb', 'm'] == resolve_chain(DAT1, ['b', 'jb', 'm'])
        assert ['b', '_'] == resolve_chain(DAT1, ['b', 'jb', 'z'])
