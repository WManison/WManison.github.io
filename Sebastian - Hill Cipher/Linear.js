/*
Hill Cipher
Sebastian Sanchez 
4/27/2025
University of Colorado Colorado Springs
Copyright (c) 2025 Jack Dodge. All rights reserved.
Licensed under the MIT License.
*/


const A = [
    [1, -1, -1, 1],
    [2, -3, -5, 4],
    [-2, -1, -2, 2],
    [3, -3, -1, 2]
];

// Function to convert character to its decimal
function charDecimal(char) {
    return char.charCodeAt(0);
}

// Convert text to a matrix of Unicode decimal values
function messageMatrix(message) {
    const numbers = Array.from(message).map(c => charDecimal(c));
    while (numbers.length % 4 !== 0) {
        numbers.push(0);  // Pad the message with zeros to make its length a multiple of 4
    }

    // Convert numbers to a matrix (4 rows, N columns)
    const numCols = numbers.length / 4;
    const B = [];
    for (let i = 0; i < 4; i++) {
        B.push(numbers.slice(i * numCols, (i + 1) * numCols));
    }

    return B;
}

// Matrix multiplication
function matrixMultiply(A, B) {
    const result = [];
    for (let i = 0; i < A.length; i++) {
        result.push([]);
        for (let j = 0; j < B[0].length; j++) {
            let sum = 0;
            for (let k = 0; k < A[0].length; k++) {
                sum += A[i][k] * B[k][j];
            }
            result[i].push(sum);
        }
    }
    return result;
}

function encryptMessage(message) {
    const B = messageMatrix(message);
    const C = matrixMultiply(A, B);
    return { C };
}

// Function to handle the encryption when user clicks the button
function encryptMessageFromInput() {
    const userInput = document.getElementById("message").value;
    const result = encryptMessage(userInput);

    // Function to format matrix into a string for display
    const formatMatrix = (matrix) => {
        return matrix.map(row => `[${row.join(", ")}]`).join("\n");
    };

    // Convert the original message into matrix B
    const B = messageMatrix(userInput);

    // Format the original matrix B and the encrypted matrix C
    const originalMatrix = formatMatrix(B);
    const encryptedMatrix = formatMatrix(result.C);

    // Display both matrices in the output box
    const output = `
Original Message Matrix (B):
${originalMatrix}

Encrypted Message Matrix (C):
${encryptedMatrix}`;

    // Set the output in the textarea
    document.getElementById("outputBox").value = output;
}