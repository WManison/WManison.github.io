/*
    TIC TAC TOE
    West Manison
    CS 3300-002 - University of Colorado, Colorado Springs
    Copyright (c) 2025 West Manison. All rights reserved.
    Licensed under the MIT License.
    
    Last edited: 4/16/2025
    Description: adds interactivity for tic tac toe game. must check for specific winning combinations
    and return appropriate game-ending message.
*/

// create constants
const board = document.getElementById('game')
const squares = document.getElementsByClassName('cell')
const players = ['X', 'O']
let currentPlayer = players[0] // player 1 = X
const endMessage = document.createElement('h2')
    endMessage.textContent = "X's turn !"
    endMessage.style.marginTop = '30px'
    endMessage.style.textAlign='center'
board.after(endMessage)

// winning combinations
const winning_combinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

// 
for(let i = 0; i < squares.length; i++){
    squares[i].addEventListener('click', () => {
        if(squares[i].textContent !== ''){
            return
        }
        squares[i].textContent = currentPlayer
        squares[i].classList.add(currentPlayer === 'X' ? 'player-x' : 'player-o');
        if(checkWin(currentPlayer)) {
            endMessage.textContent=`Game over!\n${currentPlayer} wins!`
            endMessage.style.whiteSpace = "pre-line"           
            return
        }
        if(checkTie()) {
            endMessage.textContent= `Game is tied!`
            return
        }
        currentPlayer = (currentPlayer === players[0]) ? players[1] : players[0] 
        if(currentPlayer == players[0]) {
            endMessage.textContent= `X's turn!`
        } else {
            endMessage.textContent= `O's turn!`
        }     
    })   
}

// CHECK WIN.  verify whether any current combinations result in a win
function checkWin(currentPlayer) {
    for(let i = 0; i < winning_combinations.length; i++){
        const [a, b, c] = winning_combinations[i]
        if(squares[a].textContent === currentPlayer && squares[b].textContent === currentPlayer && squares[c].textContent === currentPlayer){
            return true
        }
    }
    return false
}

// CHECK TIE. verify whether all cells are filled without matching winning combination (a tie)
function checkTie(){
    for(let i = 0; i < squares.length; i++) {
        if(squares[i].textContent === '') {
            return false;
        }
    }
    return true
}

// RESTART BUTTON. adds functional restart button
function restartButton() {
    for(let i = 0; i < squares.length; i++) {
        squares[i].textContent = ""
        squares[i].classList.remove('player-x', 'player-o');
    }
    endMessage.textContent=`X's turn!`
    currentPlayer = players[0]
}