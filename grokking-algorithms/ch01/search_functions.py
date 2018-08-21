
def binary_search(items, target):
    """Binary Search algorithm."""
    low = 0
    high = len(items) - 1

    while low <= high:
        mid = (low + high)
        guess = items[mid]
        if guess == target:
            return mid
        if guess > target:
            high = mid - 1
        else:
            low = mid + 1

    return None
