from typing import Union, Any


def sequential_values(l: 'list[int]') -> 'bool':
    '''
        checks if list values are sequential
    '''

    last = l[0]
    for i in l[1:]:
        if last + 1 != i:
            return False
    return True


def get_first_occurrences(
    l: 'Union[list, tuple]'
) -> 'list[tuple[int, Any]]':
    '''
        Note: repetitions must be sequential (that's 
        why it is recommended that the input list
        be sorted)
    '''

    ret = []

    last = None
    for i, v in enumerate(l):
        if v != last or i == 0:
            last = v
            ret.append((i, v))

    return ret


def order_by_sublist_index(l: 'list', index: 'int'):
    return sorted(l, key=lambda x: x[index])


def dict_list_values_to_list(d: 'dict'):
    values = list(d.values())
    values = [j for i in values for j in i]
