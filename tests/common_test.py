from forestanza.common import (
    KEYDEF, dict_resolve, dict_intersect)

DATA = {KEYDEF: 1, 'a': 2,
        'b': {KEYDEF: 3, 'ib': 4, 'jb': {'m': 1}},
        'c': {'ic': 5}}

class TestF_resolve_chain:
    def test_1L(self):
        assert [] == dict_resolve(DATA, [])
        assert ['a'] == dict_resolve(DATA, ['a'])
        assert ['b'] == dict_resolve(DATA, ['b'])
        assert ['c'] == dict_resolve(DATA, ['c'])
        assert [KEYDEF] == dict_resolve(DATA, ['z'])

    def test_2L(self):
        assert ['a'] == dict_resolve(DATA, ['a', 'z'])
        assert [KEYDEF] == dict_resolve(DATA, ['c', 'z'])
        assert [KEYDEF] == dict_resolve(DATA, ['y', 'z'])
        assert ['b', 'ib'] == dict_resolve(DATA, ['b', 'ib'])
        assert ['b', KEYDEF] == dict_resolve(DATA, ['b', 'z'])
        assert ['c', 'ic'] == dict_resolve(DATA, ['c', 'ic'])
        assert [KEYDEF] == dict_resolve(DATA, ['c', 'z'])

    def test_3L(self):
        assert ['a'] == dict_resolve(DATA, ['a', 'y', 'z'])
        assert [KEYDEF] == dict_resolve(DATA, ['c', 'y', 'z'])
        assert ['b', 'ib'] == dict_resolve(DATA, ['b', 'ib', 'z'])
        assert ['b', KEYDEF] == dict_resolve(DATA, ['b', 'y', 'z'])
        assert ['c', 'ic'] == dict_resolve(DATA, ['c', 'ic', 'z'])
        assert ['b', 'jb', 'm'] == dict_resolve(DATA, ['b', 'jb', 'm'])
        assert ['b', KEYDEF] == dict_resolve(DATA, ['b', 'jb', 'z'])


MASK = {'a': [1, 2], 'b': {'ib': [3, 4], 'ff': 5}, 'f': [6]}

# class TestF_dict_intersect:
#     def test_1L(self):
#         assert {} == dict_intersect(DATA, {})
#         assert {'a': 2} == dict_intersect(DATA, {'a': 0})
#         assert {'b': {'_': 3}} == dict_intersect(DATA, {'b': 0})
#         assert {'_': 1} == dict_intersect(DATA, {'c': 0})
#         assert {'_': 1} == dict_intersect(DATA, {'z': 0})
