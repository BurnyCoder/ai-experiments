
# Constants for input validation
MIN_INPUT = 0
MAX_INPUT = 900  # Set to avoid RecursionError and stack overflow

def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer using recursion.
    
    This implementation uses a recursive approach to calculate n!
    Time Complexity: O(n) - n recursive calls
    Space Complexity: O(n) - due to recursive call stack
    
    Args:
        n (int): A non-negative integer to calculate factorial for.
            Must be between MIN_INPUT and MAX_INPUT inclusive.
    
    Returns:
        int: The factorial of n (n!)
    
    Raises:
        ValueError: If n is negative or exceeds MAX_INPUT
        TypeError: If n is not an integer
    
    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
        >>> factorial(3)
        6
    """
    # Type checking
    if not isinstance(n, int):
        raise TypeError(f"Input must be an integer, got {type(n).__name__}")
    
    # Input validation
    if n < MIN_INPUT:
        raise ValueError(f"Input must be non-negative, got {n}")
    if n > MAX_INPUT:
        raise ValueError(f"Input exceeds maximum allowed value of {MAX_INPUT}, got {n}")
    
    # Base cases
    if n <= 1:
        return 1
    
    # Recursive case
    return n * factorial(n - 1)

def test_factorial():
    """Test suite for factorial function."""
    # Test valid inputs
    test_cases = [0, 1, 5, 10]
    for n in test_cases:
        assert factorial(n) == math.factorial(n), f"Failed for n={n}"
    
    # Test error cases
    try:
        factorial(-1)
        assert False, "Should raise ValueError for negative input"
    except ValueError:
        pass
    
    try:
        factorial(MAX_INPUT + 1)
        assert False, "Should raise ValueError for input > MAX_INPUT"
    except ValueError:
        pass
    
    try:
        factorial(3.14)
        assert False, "Should raise TypeError for non-integer input"
    except TypeError:
        pass
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    test_factorial()
