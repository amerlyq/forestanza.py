from forestanza.common import (
    KEYDEF, dict_resolve, dict_flatten, dict_intersect)

DATA = {KEYDEF: 1, 'a': 2, 'b': {'ib': 5},
        'c': {KEYDEF: 3, 'ic': 4, 'jc': {'m': 1}}}

def chain_resolve(*chain):
    return dict_resolve(DATA, list(chain))[0]

class TestF_resolve_chain:
    def test_1L(self):
        assert [] == chain_resolve()
        assert ['a'] == chain_resolve('a')
        assert ['b'] == chain_resolve('b')
        assert ['c'] == chain_resolve('c')
        assert [KEYDEF] == chain_resolve('z')

    def test_2L(self):
        assert ['a'] == chain_resolve('a', 'z')
        assert [KEYDEF] == chain_resolve('b', 'z')
        assert [KEYDEF] == chain_resolve('y', 'z')
        assert ['b', 'ib'] == chain_resolve('b', 'ib')
        assert [KEYDEF] == chain_resolve('b', 'z')
        assert ['c', 'ic'] == chain_resolve('c', 'ic')
        assert ['c', KEYDEF] == chain_resolve('c', 'z')

    def test_3L(self):
        assert ['a'] == chain_resolve('a', 'y', 'z')
        assert ['b', 'ib'] == chain_resolve('b', 'ib', 'z')
        assert [KEYDEF] == chain_resolve('b', 'y', 'z')
        assert ['c', 'ic'] == chain_resolve('c', 'ic', 'z')
        assert ['c', KEYDEF] == chain_resolve('c', 'y', 'z')
        assert ['c', 'jc', 'm'] == chain_resolve('c', 'jc', 'm')
        assert ['c', KEYDEF] == chain_resolve('c', 'jc', 'z')


class TestF_dict_flatten:
    def test_1L(self):
        assert [] == list(dict_flatten({}))
        assert [(['a'], 1)] == list(dict_flatten({'a': 1}))
        assert ([(['a'], 1), (['b'], 2)] ==
                list(dict_flatten({'a': 1, 'b': 2})))

    def test_2L(self):
        assert ([(['a', 'c'], 3), (['a', 'd'], 4)] ==
                list(dict_flatten({'a': {'c': 3, 'd': 4}})))


# MASK = {'a': [1, 2], 'c': {'ic': [3, 4], 'ff': 5}, 'f': [6]}
# class TestF_dict_intersect:
#     def test_1L(self):
#         assert {'_': 1} == dict_intersect(DATA, {})
#         assert {'_': 1, 'a': 2} == dict_intersect(DATA, {'a': 0})
#         assert {'_': 1, 'c': {'_': 3}} == dict_intersect(DATA, {'c': 0})
#         assert {'_': 1} == dict_intersect(DATA, {'b': 0})
#         assert {'_': 1} == dict_intersect(DATA, {'z': 0})
