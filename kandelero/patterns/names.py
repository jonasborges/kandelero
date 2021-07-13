def get_pattern_name(comparator_func):
    # remove prefix 'is_'
    pattern_name = comparator_func.__name__[3:]
    return pattern_name.replace("_", " ").title()
