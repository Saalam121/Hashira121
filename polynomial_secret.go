package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/big"
	"os"
	"strconv"
)

// TestCase represents the JSON structure
type TestCase struct {
	Keys struct {
		N int `json:"n"`
		K int `json:"k"`
	} `json:"keys"`
	Roots map[string]struct {
		Base  string `json:"base"`
		Value string `json:"value"`
	} `json:"-"`
}

// Point represents a decoded (x, y) point
type Point struct {
	X *big.Int
	Y *big.Int
}

// UnmarshalJSON custom unmarshaler to handle dynamic root keys
func (t *TestCase) UnmarshalJSON(data []byte) error {
	// First unmarshal into a map
	var raw map[string]json.RawMessage
	if err := json.Unmarshal(data, &raw); err != nil {
		return err
	}

	// Parse keys
	if keysData, ok := raw["keys"]; ok {
		if err := json.Unmarshal(keysData, &t.Keys); err != nil {
			return err
		}
	}

	// Parse roots
	t.Roots = make(map[string]struct {
		Base  string `json:"base"`
		Value string `json:"value"`
	})

	for key, value := range raw {
		if key == "keys" {
			continue
		}
		var root struct {
			Base  string `json:"base"`
			Value string `json:"value"`
		}
		if err := json.Unmarshal(value, &root); err == nil {
			t.Roots[key] = root
		}
	}

	return nil
}

// decodeValue decodes a value from given base to decimal
func decodeValue(value string, base int) (*big.Int, error) {
	result := new(big.Int)
	result.SetString(value, base)
	return result, nil
}

// parseTestCase reads and parses the JSON test case
func parseTestCase(filename string) (*TestCase, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	var testCase TestCase
	if err := json.Unmarshal(data, &testCase); err != nil {
		return nil, err
	}

	return &testCase, nil
}

// extractPoints converts the test case into decoded points
func extractPoints(testCase *TestCase) ([]Point, error) {
	points := make([]Point, 0)

	for xStr, root := range testCase.Roots {
		// Parse X value
		x := new(big.Int)
		x.SetString(xStr, 10)

		// Parse base
		base, err := strconv.Atoi(root.Base)
		if err != nil {
			return nil, fmt.Errorf("invalid base: %s", root.Base)
		}

		// Decode Y value
		y, err := decodeValue(root.Value, base)
		if err != nil {
			return nil, fmt.Errorf("failed to decode value: %s in base %d", root.Value, base)
		}

		points = append(points, Point{X: x, Y: y})
	}

	return points, nil
}

// lagrangeInterpolation performs Lagrange interpolation to find f(0)
func lagrangeInterpolation(points []Point, k int) *big.Int {
	// We only need the first k points
	if len(points) > k {
		points = points[:k]
	}

	result := new(big.Int)

	for i := 0; i < len(points); i++ {
		// Calculate Li(0) = product of (-xj)/(xi - xj) for all j != i
		numerator := new(big.Int).Set(points[i].Y)
		denominator := big.NewInt(1)

		for j := 0; j < len(points); j++ {
			if i != j {
				// numerator *= -xj
				negXj := new(big.Int).Neg(points[j].X)
				numerator.Mul(numerator, negXj)

				// denominator *= (xi - xj)
				diff := new(big.Int).Sub(points[i].X, points[j].X)
				denominator.Mul(denominator, diff)
			}
		}

		// Add the contribution to result
		term := new(big.Int).Div(numerator, denominator)
		result.Add(result, term)
	}

	return result
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run polynomial_secret.go <testcase.json>")
		return
	}

	filename := os.Args[1]

	// Parse test case
	testCase, err := parseTestCase(filename)
	if err != nil {
		fmt.Printf("Error parsing test case: %v\n", err)
		return
	}

	fmt.Printf("Test Case: %s\n", filename)
	fmt.Printf("Number of roots (n): %d\n", testCase.Keys.N)
	fmt.Printf("Minimum roots required (k): %d\n", testCase.Keys.K)
	fmt.Println("\nDecoded Points:")

	// Extract and decode points
	points, err := extractPoints(testCase)
	if err != nil {
		fmt.Printf("Error extracting points: %v\n", err)
		return
	}

	// Print decoded points
	for _, point := range points {
		fmt.Printf("  x = %s, y = %s\n", point.X.String(), point.Y.String())
	}

	// Find the secret using Lagrange interpolation
	secret := lagrangeInterpolation(points, testCase.Keys.K)
	fmt.Printf("\nSecret (constant term c): %s\n", secret.String())
}
