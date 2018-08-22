
def selection_sort(items):
    """Selection sort."""
    result = []
    for i in range(len(items)):
        smallest_idx = find_smallest(items)
        result.append(items.pop(smallest_idx))
    return result


def find_smallest(items):
    """Find the smallest item's index in list."""
    smallest = items[0]
    idx = 0
    for i, v in enumerate(items):
        if v < smallest:
            smallest = v
            idx = i
    return idx
