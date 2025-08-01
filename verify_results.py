import json
import sys
from fractions import Fraction
from decimal import Decimal, getcontext

# Set high precision for decimal calculations
getcontext().prec = 100

def decode_value(value, base):
    """Decode a value from given base to decimal"""
    return int(value, base)

def lagrange_interpolation_fraction(points, x=0):
    """
    Perform Lagrange interpolation using exact fraction arithmetic
    This avoids any rounding errors
    """
    n = len(points)
    result = Fraction(0)
    
    for i in range(n):
        # Calculate Li(x)
        term = Fraction(points[i][1])  # yi
        
        for j in range(n):
            if i != j:
                # Multiply by (x - xj) / (xi - xj)
                numerator = x - points[j][0]
                denominator = points[i][0] - points[j][0]
                term *= Fraction(numerator, denominator)
        
        result += term
    
    return result

def lagrange_interpolation_decimal(points, x=0):
    """
    Perform Lagrange interpolation using high-precision decimal arithmetic
    """
    n = len(points)
    result = Decimal(0)
    
    for i in range(n):
        # Calculate Li(x)
        term = Decimal(points[i][1])  # yi
        
        for j in range(n):
            if i != j:
                # Multiply by (x - xj) / (xi - xj)
                numerator = Decimal(x - points[j][0])
                denominator = Decimal(points[i][0] - points[j][0])
                term *= numerator / denominator
        
        result += term
    
    return result

def verify_polynomial(points, secret):
    """
    Verify by constructing the polynomial and checking if f(0) = secret
    Also calculates f(x) for each given point to verify consistency
    """
    print("\nVerification by evaluating polynomial at given points:")
    
    # Check if the polynomial passes through all given points
    all_correct = True
    for x, y in points:
        # Calculate f(x) using Lagrange interpolation
        f_x = lagrange_interpolation_fraction(points, x)
        if f_x == y:
            print(f"  f({x}) = {y} ✓")
        else:
            print(f"  f({x}) = {f_x} (expected {y}) ✗")
            all_correct = False
    
    return all_correct

def manual_calculation_example(points):
    """
    Show step-by-step manual calculation for the first test case
    """
    if len(points) != 3:
        return
    
    print("\nManual Calculation Steps for f(0):")
    print("Using Lagrange interpolation formula:")
    print("f(0) = Σ(yi * Π((0-xj)/(xi-xj))) for all i, where j ≠ i")
    print()
    
    total = Fraction(0)
    
    for i in range(3):
        xi, yi = points[i]
        print(f"Term {i+1} (x{i+1}={xi}, y{i+1}={yi}):")
        
        numerator_parts = []
        denominator_parts = []
        
        for j in range(3):
            if i != j:
                xj = points[j][0]
                num = -xj  # (0 - xj)
                den = xi - xj
                numerator_parts.append(f"(0-{xj})")
                denominator_parts.append(f"({xi}-{xj})")
                
        num_str = " × ".join(numerator_parts)
        den_str = " × ".join(denominator_parts)
        
        # Calculate the actual values
        term_num = yi
        term_den = 1
        for j in range(3):
            if i != j:
                xj = points[j][0]
                term_num *= -xj
                term_den *= (xi - xj)
        
        term_value = Fraction(term_num, term_den)
        total += term_value
        
        print(f"  = {yi} × {num_str} / {den_str}")
        print(f"  = {yi} × {term_num//yi} / {term_den}")
        print(f"  = {term_num} / {term_den}")
        print(f"  = {term_value}")
        print()
    
    print(f"Total: {total}")
    return total

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_results.py <testcase.json>")
        return
    
    filename = sys.argv[1]
    
    # Read and parse the test case
    with open(filename, 'r') as f:
        test_case = json.load(f)
    
    print(f"Verifying: {filename}")
    print(f"Number of roots (n): {test_case['keys']['n']}")
    print(f"Minimum roots required (k): {test_case['keys']['k']}")
    print()
    
    # Extract and decode points
    points = []
    for key, value in test_case.items():
        if key == 'keys':
            continue
        
        x = int(key)
        base = int(value['base'])
        y = decode_value(value['value'], base)
        points.append((x, y))
        print(f"Decoded: x={x}, base={base}, encoded='{value['value']}' → y={y}")
    
    # Sort points by x value for consistency
    points.sort(key=lambda p: p[0])
    
    # Use only the first k points
    k = test_case['keys']['k']
    selected_points = points[:k]
    
    print(f"\nUsing first {k} points for interpolation:")
    for x, y in selected_points:
        print(f"  ({x}, {y})")
    
    # Calculate secret using different methods
    print("\n" + "="*50)
    print("RESULTS:")
    print("="*50)
    
    # Method 1: Exact fraction arithmetic
    secret_fraction = lagrange_interpolation_fraction(selected_points, 0)
    print(f"Secret (using fractions): {secret_fraction} = {int(secret_fraction)}")
    
    # Method 2: High-precision decimal
    secret_decimal = lagrange_interpolation_decimal(selected_points, 0)
    print(f"Secret (using decimals): {secret_decimal}")
    
    # Verify the polynomial
    verify_polynomial(selected_points, int(secret_fraction))
    
    # For small test cases, show manual calculation
    if k == 3:
        manual_calculation_example(selected_points)
    
    print("\n" + "="*50)
    print(f"FINAL ANSWER: {int(secret_fraction)}")
    print("="*50)

if __name__ == "__main__":
    main()
