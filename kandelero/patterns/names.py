from typing import Callable, Union


def get_pattern_name(comparator_func: Union[Callable, None]):
    try:
        # remove prefix 'is_'
        pattern_name = comparator_func.__name__[3:]
    except AttributeError:
        return ""
    else:
        return pattern_name.replace("_", " ").title()
