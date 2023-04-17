from typing import Union, Any


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
