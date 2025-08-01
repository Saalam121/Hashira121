# Polynomial Secret Finder

This project solves the Catalog Placements Assignment for finding the secret constant term of a polynomial using Lagrange interpolation.

## Problem Description

Given a set of polynomial roots in various bases, the task is to:
1. Parse JSON input containing encoded polynomial roots
2. Decode Y values from different bases to decimal
3. Use Lagrange interpolation to find the secret (constant term c) of the polynomial

## Solution Approach

The solution uses **Lagrange Interpolation** to reconstruct the polynomial and find f(0), which gives us the constant term.

### Key Components:

1. **JSON Parsing**: Reads test cases from JSON files with dynamic root keys
2. **Base Decoding**: Converts values from bases 2-16 to decimal using BigInt for large numbers
3. **Lagrange Interpolation**: Calculates f(0) using the formula:
   ```
   f(0) = Σ(yi * Π(-xj/(xi-xj))) for all i, where j ≠ i
   ```

## Implementation Details

### Languages Provided:
- **JavaScript (Node.js)** - `polynomial_secret.js`
- **Python (Verification)** - `verify_results.py`

Both implementations use arbitrary precision arithmetic to handle large numbers accurately.

## Usage

### JavaScript Version:
```bash
node polynomial_secret.js <testcase.json>
```

### Python Verification:
```bash
python verify_results.py <testcase.json>
```

## Test Cases

### Test Case 1:
- n = 4 (total roots provided)
- k = 3 (minimum roots needed)
- **Secret: 3**

### Test Case 2:
- n = 10 (total roots provided)
- k = 7 (minimum roots needed)
- **Secret: 79836264058144**

## Example Output

```
Test Case: testcase1.json
Number of roots (n): 4
Minimum roots required (k): 3

Decoded Points:
  x = 1, y = 4
  x = 2, y = 7
  x = 3, y = 12
  x = 6, y = 39

Secret (constant term c): 3
```

## Algorithm Verification

For Test Case 1, we can verify manually:
- Points: (1,4), (2,7), (3,12)
- Using these points, we can determine the polynomial is: f(x) = x² + 2x + 3
- Therefore, f(0) = 3 (the constant term)

## Dependencies

### JavaScript:
- Node.js (built-in fs module)
- No external packages required

### Python:
- Standard library only (json, fractions, decimal)
- No external packages required

## Notes

- The solution handles large numbers using BigInt in JavaScript and fractions/decimal in Python
- Only the first k points are used for interpolation as specified
- The solution correctly handles different number bases (2-16)
- Python verification script provides step-by-step manual calculation for small test cases
