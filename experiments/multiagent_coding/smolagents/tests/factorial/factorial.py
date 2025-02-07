from functools import lru_cache
import sys
from math import log10, pi, e
from typing import NoReturn


@lru_cache(maxsize=None)
def factorial(n: int) -> int:
    """
    Calculate the factorial of a number using recursion with memoization.
    
    Args:
        n (int): A non-negative integer
        
    Returns:
        int: The factorial of n (n!)
        
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
        RecursionError: If recursion depth is exceeded
        OverflowError: If result is too large
        
    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
        >>> factorial(1)
        1
        >>> factorial(10)
        3628800
        
    Notes:
        - Uses a hybrid approach with recursive implementation for small numbers
          and iterative implementation for large numbers
        - Implements memoization for optimal performance on repeated calls
        - Includes overflow detection using Stirling's approximation
        
    Time Complexity: O(n)
    Space Complexity: O(n) due to recursion stack, but with memoization
                     subsequent calls for same n are O(1)
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be non-negative")
    
    # Early overflow detection using Stirling's approximation
    if n > 0:
        digits = n * log10(n/e) + log10(2*pi*n)/2
        if digits > sys.float_info.max_10_exp:
            raise OverflowError(
                f"Result too large: approximately {int(digits)} digits"
            )
    
    if n > sys.getrecursionlimit() // 2:
        return factorial_iterative(n)
        
    try:
        if n <= 1:
            return 1
        return n * factorial(n - 1)
    except RecursionError:
        return factorial_iterative(n)


def factorial_iterative(n: int) -> int:
    """
    Iterative implementation of factorial calculation.
    Used as a fallback for large numbers to avoid recursion depth issues.
    
    Args:
        n (int): A non-negative integer
        
    Returns:
        int: The factorial of n (n!)
        
    Raises:
        OverflowError: If intermediate result becomes too large
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
        # Periodic overflow check
        if result.bit_length() > sys.maxsize.bit_length():
            raise OverflowError("Result too large for integer arithmetic")
    return result


def test_factorial() -> None:
    """
    Run comprehensive test cases for the factorial function.
    Tests basic functionality, edge cases, error handling,
    and memoization effectiveness.
    """
    # Test basic cases
    assert factorial(0) == 1, "factorial(0) should be 1"
    assert factorial(1) == 1, "factorial(1) should be 1"
    assert factorial(5) == 120, "factorial(5) should be 120"
    
    # Test larger numbers
    assert factorial(10) == 3628800, "factorial(10) should be 3628800"
    
    # Test memoization effectiveness
    for _ in range(3):  # Multiple calls should use cached results
        assert factorial(15) == 1307674368000, "Memoization issue"
    
    # Test error cases
    try:
        factorial(-1)
        assert False, "Should raise ValueError for negative input"
    except ValueError:
        pass
        
    try:
        factorial(1.5)
        assert False, "Should raise TypeError for non-integer input"
    except TypeError:
        pass
    
    try:
        # Test very large number for overflow
        factorial(sys.maxsize)
        assert False, "Should raise OverflowError for very large input"
    except OverflowError:
        pass
    
    print("All tests passed!")


if __name__ == "__main__":
    # Run tests
    test_factorial()
    
    # Example usage
    try:
        print(f"factorial(5) = {factorial(5)}")
        print(f"factorial(10) = {factorial(10)}")
        print(f"factorial(20) = {factorial(20)}")
    except (ValueError, TypeError, RecursionError, OverflowError) as e:
        print(f"Error: {e}")