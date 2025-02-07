# Initial Implementation

def factorial_recursive(n):
    """Calculate factorial recursively.

    Args:
        n (int): Non-negative integer for which to calculate the factorial.

    Returns:
        int: The factorial of n.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is a negative integer.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if n == 0:
        return 1
    else:
        return n * factorial_recursive(n-1)