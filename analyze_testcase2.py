import json

# Read test case 2
with open('testcase2.json', 'r') as f:
    test_case = json.load(f)

print("Test Case 2 Analysis")
print("=" * 50)
print(f"Number of roots (n): {test_case['keys']['n']}")
print(f"Minimum roots required (k): {test_case['keys']['k']}")
print()

# Decode all points
points = []
for key, value in test_case.items():
    if key == 'keys':
        continue
    
    x = int(key)
    base = int(value['base'])
    y_encoded = value['value']
    
    # Decode the value
    y = int(y_encoded, base)
    
    points.append((x, y))
    print(f"Point {x}:")
    print(f"  Encoded: '{y_encoded}' (base {base})")
    print(f"  Decoded: {y}")
    print()

# Sort by x value
points.sort(key=lambda p: p[0])

print("\nFirst 7 points (for k=7):")
for i in range(7):
    print(f"  ({points[i][0]}, {points[i][1]})")

# Let's also check if there's any pattern or if we can verify the polynomial degree
print("\nChecking decoded values for consistency...")

# Show the exact values that both implementations are using
print("\nExact decoded values for first 7 points:")
for i in range(7):
    x, y = points[i]
    print(f"x={x}: y={y}")
