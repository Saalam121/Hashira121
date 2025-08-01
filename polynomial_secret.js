const fs = require('fs');

// Function to decode a value from given base to decimal
function decodeValue(value, base) {
    // For bases > 10, we need to handle letters
    if (base <= 10) {
        return BigInt(parseInt(value, base));
    } else {
        // Convert using BigInt for large numbers
        let result = 0n;
        const baseBI = BigInt(base);
        
        for (let i = 0; i < value.length; i++) {
            const char = value[i];
            let digit;
            
            if (char >= '0' && char <= '9') {
                digit = BigInt(char.charCodeAt(0) - '0'.charCodeAt(0));
            } else if (char >= 'a' && char <= 'z') {
                digit = BigInt(10 + char.charCodeAt(0) - 'a'.charCodeAt(0));
            } else if (char >= 'A' && char <= 'Z') {
                digit = BigInt(10 + char.charCodeAt(0) - 'A'.charCodeAt(0));
            }
            
            result = result * baseBI + digit;
        }
        
        return result;
    }
}

// Function to parse test case and extract points
function extractPoints(testCase) {
    const points = [];
    
    for (const [key, value] of Object.entries(testCase)) {
        if (key === 'keys') continue;
        
        const x = BigInt(key);
        const base = parseInt(value.base);
        const y = decodeValue(value.value, base);
        
        points.push({ x, y });
    }
    
    return points;
}

// Extended Euclidean Algorithm for modular inverse
function modInverse(a, m) {
    const [g, x] = extendedGCD(a, m);
    if (g !== 1n) throw new Error('Modular inverse does not exist');
    return ((x % m) + m) % m;
}

function extendedGCD(a, b) {
    if (a === 0n) return [b, 0n, 1n];
    const [g, x1, y1] = extendedGCD(b % a, a);
    const x = y1 - (b / a) * x1;
    const y = x1;
    return [g, x, y];
}

// GCD function for fraction reduction
function gcd(a, b) {
    a = a < 0n ? -a : a;
    b = b < 0n ? -b : b;
    while (b !== 0n) {
        const temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Lagrange interpolation to find f(0) (the constant term)
function lagrangeInterpolation(points, k) {
    // Use only the first k points
    const selectedPoints = points.slice(0, k);
    
    // We'll accumulate the result as a fraction (numerator/denominator)
    let totalNumerator = 0n;
    let totalDenominator = 1n;
    
    for (let i = 0; i < selectedPoints.length; i++) {
        // Calculate Li(0) = product of (-xj)/(xi - xj) for all j != i
        let termNumerator = selectedPoints[i].y;
        let termDenominator = 1n;
        
        for (let j = 0; j < selectedPoints.length; j++) {
            if (i !== j) {
                // numerator *= -xj
                termNumerator *= -selectedPoints[j].x;
                // denominator *= (xi - xj)
                termDenominator *= (selectedPoints[i].x - selectedPoints[j].x);
            }
        }
        
        // Add this term to our total: total = total + term
        // (a/b) + (c/d) = (a*d + b*c) / (b*d)
        totalNumerator = totalNumerator * termDenominator + totalDenominator * termNumerator;
        totalDenominator = totalDenominator * termDenominator;
        
        // Reduce the fraction to prevent overflow
        const g = gcd(totalNumerator, totalDenominator);
        totalNumerator = totalNumerator / g;
        totalDenominator = totalDenominator / g;
    }
    
    // The result should be an integer for this problem
    if (totalDenominator !== 1n && totalNumerator % totalDenominator !== 0n) {
        throw new Error('Result is not an integer');
    }
    
    return totalNumerator / totalDenominator;
}

// Main function
function main() {
    const args = process.argv.slice(2);
    if (args.length < 1) {
        console.log('Usage: node polynomial_secret.js <testcase.json>');
        return;
    }
    
    const filename = args[0];
    
    try {
        // Read and parse the test case
        const data = fs.readFileSync(filename, 'utf8');
        const testCase = JSON.parse(data);
        
        console.log(`Test Case: ${filename}`);
        console.log(`Number of roots (n): ${testCase.keys.n}`);
        console.log(`Minimum roots required (k): ${testCase.keys.k}`);
        console.log('\nDecoded Points:');
        
        // Extract and decode points
        const points = extractPoints(testCase);
        
        // Print decoded points
        points.forEach(point => {
            console.log(`  x = ${point.x}, y = ${point.y}`);
        });
        
        // Find the secret using Lagrange interpolation
        const secret = lagrangeInterpolation(points, testCase.keys.k);
        console.log(`\nSecret (constant term c): ${secret}`);
        
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
}

// Run the main function
main();
