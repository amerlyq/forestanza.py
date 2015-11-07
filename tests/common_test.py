from forestanza.common import (
    KEYDEF, dict_resolve, dict_intersect)

DATA = {KEYDEF: 1, 'a': 2, 'b': {'ib': 5},
        'c': {KEYDEF: 3, 'ic': 4, 'jc': {'m': 1}}}

class TestF_resolve_chain:
    def test_1L(self):
        assert [] == dict_resolve(DATA, [])
        assert ['a'] == dict_resolve(DATA, ['a'])
        assert ['b'] == dict_resolve(DATA, ['b'])
        assert ['c'] == dict_resolve(DATA, ['c'])
        assert [KEYDEF] == dict_resolve(DATA, ['z'])

    def test_2L(self):
        assert ['a'] == dict_resolve(DATA, ['a', 'z'])
        assert [KEYDEF] == dict_resolve(DATA, ['b', 'z'])
        assert [KEYDEF] == dict_resolve(DATA, ['y', 'z'])
        assert ['b', 'ib'] == dict_resolve(DATA, ['b', 'ib'])
        assert [KEYDEF] == dict_resolve(DATA, ['b', 'z'])
        assert ['c', 'ic'] == dict_resolve(DATA, ['c', 'ic'])
        assert ['c', KEYDEF] == dict_resolve(DATA, ['c', 'z'])

    def test_3L(self):
        assert ['a'] == dict_resolve(DATA, ['a', 'y', 'z'])
        assert ['b', 'ib'] == dict_resolve(DATA, ['b', 'ib', 'z'])
        assert [KEYDEF] == dict_resolve(DATA, ['b', 'y', 'z'])
        assert ['c', 'ic'] == dict_resolve(DATA, ['c', 'ic', 'z'])
        assert ['c', KEYDEF] == dict_resolve(DATA, ['c', 'y', 'z'])
        assert ['c', 'jc', 'm'] == dict_resolve(DATA, ['c', 'jc', 'm'])
        assert ['c', KEYDEF] == dict_resolve(DATA, ['c', 'jc', 'z'])


MASK = {'a': [1, 2], 'c': {'ic': [3, 4], 'ff': 5}, 'f': [6]}

class TestF_dict_intersect:
    def test_1L(self):
        assert {'_': 1} == dict_intersect(DATA, {})
        assert {'_': 1, 'a': 2} == dict_intersect(DATA, {'a': 0})
        assert {'_': 1, 'c': {'_': 3}} == dict_intersect(DATA, {'c': 0})
        assert {'_': 1} == dict_intersect(DATA, {'b': 0})
        assert {'_': 1} == dict_intersect(DATA, {'z': 0})
