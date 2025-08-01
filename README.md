# Catalog Placements Assignment Solution

## Problem Statement
Find the constant term `c` of a polynomial using Lagrange interpolation from given encoded data points.

## Solution Overview

### Algorithm: Lagrange Interpolation
The solution implements Lagrange interpolation to find `f(0)`, which gives the constant term of the polynomial.

**Formula used:**
```
f(0) = Σ(yi * Π(-xj/(xi-xj))) for all i, where j ≠ i
```

### Implementation Features
1. **JSON Parsing**: Handles dynamic root keys in input files
2. **Base Conversion**: Decodes values from bases 2-16 to decimal
3. **Precision Handling**: Uses BigInt for arbitrary precision arithmetic
4. **Efficient Computation**: Only uses first `k` points as specified

## How to Run

```bash
node polynomial_secret.js <testcase.json>
```

## Test Results

| Test Case | n (total roots) | k (roots used) | Secret Found |
|-----------|----------------|----------------|---------------|
| testcase1.json | 4 | 3 | **3** |
| testcase2.json | 10 | 7 | **79836264058144** |

## Files Included
- `polynomial_secret.js` - Main solution implementation
- `testcase1.json` - First test case (provided)
- `testcase2.json` - Second test case (provided)
- `README.md` - This documentation

## Requirements
- Node.js (v12.0.0 or higher)
- No external dependencies
