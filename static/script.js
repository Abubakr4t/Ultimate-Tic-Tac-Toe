let board = null;
let activeBoard = null;
let currentPlayer = 'X';
let gameOver = false;
let statusMessage = '';
let difficulty = 4;

async function fetchGameState() {
    try {
        const response = await fetch('/reset');
        const data = await response.json();
        board = data.board;
        activeBoard = data.active_board;
        currentPlayer = data.current_player;
        gameOver = data.game_over;
        statusMessage = '';
        renderBoard();
        document.getElementById('status').textContent = 'Your turn (X)';
    } catch (error) {
        console.error('Error loading game:', error);
        document.getElementById('status').textContent = 'Error loading game: ' + error.message;
    }
}

function renderBoard() {
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            const boardIdx = i * 3 + j;
            const boardDiv = document.getElementById(`board-${i}-${j}`);
            if (!boardDiv) continue;
            
            boardDiv.innerHTML = '';
            boardDiv.className = 'board grid grid-cols-3 gap-px bg-gray-400 p-1 rounded relative';
            
            const boardState = board[boardIdx];
            const boardWinner = checkSmallBoardWinner(boardState);
            
            // Handle won/tied boards
            if (boardWinner) {
                if (boardWinner === 'T') {
                    boardDiv.classList.add('board-tied');
                    const overlay = document.createElement('div');
                    overlay.className = 'winner-overlay absolute inset-0 flex items-center justify-center text-4xl text-gray-600';
                    overlay.textContent = 'T';
                    boardDiv.appendChild(overlay);
                } else {
                    boardDiv.classList.add(`board-won-${boardWinner.toLowerCase()}`);
                    const overlay = document.createElement('div');
                    overlay.className = `winner-overlay absolute inset-0 flex items-center justify-center text-6xl font-bold`;
                    overlay.textContent = boardWinner;
                    overlay.style.color = boardWinner === 'X' ? '#ef4444' : '#22c55e';
                    boardDiv.appendChild(overlay);
                }
            }
            
            // Active/inactive highlighting
            if (!gameOver) {
                if (activeBoard === null || activeBoard === boardIdx) {
                    boardDiv.classList.add('active-board');
                } else {
                    boardDiv.classList.add('inactive-board');
                }
            }
            
            // Only render cells if board isn't won/tied
            if (!boardWinner) {
                for (let r = 0; r < 3; r++) {
                    for (let c = 0; c < 3; c++) {
                        const cell = document.createElement('div');
                        cell.className = 'cell flex items-center justify-center text-xl font-bold border border-gray-500 bg-white';
                        
                        const cellValue = boardState[r][c];
                        cell.textContent = cellValue === ' ' ? '' : cellValue;
                        
                        if (cellValue === 'X') cell.classList.add('won-x');
                        if (cellValue === 'O') cell.classList.add('won-o');
                        
                        if (!gameOver && currentPlayer === 'X' && cellValue === ' ' && 
                            (activeBoard === null || activeBoard === boardIdx)) {
                            cell.classList.add('cursor-pointer', 'hover:bg-blue-50');
                            cell.onclick = () => handleMove(i, j, r, c);
                        } else {
                            cell.classList.add('cursor-default');
                        }
                        
                        boardDiv.appendChild(cell);
                    }
                }
            }
        }
    }
    
    // Update game status
    if (gameOver) {
        document.getElementById('status').textContent = statusMessage;
    } else {
        document.getElementById('status').textContent = currentPlayer === 'X' 
            ? 'Your turn (X)' 
            : 'AI is thinking...';
    }
}

function checkSmallBoardWinner(board) {
    const lines = [
        [[0,0],[0,1],[0,2]], [[1,0],[1,1],[1,2]], [[2,0],[2,1],[2,2]],
        [[0,0],[1,0],[2,0]], [[0,1],[1,1],[2,1]], [[0,2],[1,2],[2,2]],
        [[0,0],[1,1],[2,2]], [[0,2],[1,1],[2,0]]
    ];
    
    for (const line of lines) {
        const [a, b, c] = line;
        if (board[a[0]][a[1]] === board[b[0]][b[1]] && 
            board[b[0]][b[1]] === board[c[0]][c[1]] && 
            board[a[0]][a[1]] !== ' ') {
            return board[a[0]][a[1]];
        }
    }
    
    // Check for tie
    if (isBoardFull(board)) {
        return 'T';
    }
    
    return null;
}

function isBoardFull(board) {
    return board.every(row => row.every(cell => cell !== ' '));
}

async function handleMove(bigRow, bigCol, smallRow, smallCol) {
    if (gameOver || currentPlayer !== 'X') return;
    
    try {
        const response = await fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                board: board,
                big_row: bigRow,
                big_col: bigCol,
                small_row: smallRow,
                small_col: smallCol,
                player: 'X',
                active_board: activeBoard
            })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            document.getElementById('status').textContent = result.message || 'Invalid move';
            return;
        }
        
        board = result.new_board;
        
        if (result.message) {
            gameOver = true;
            statusMessage = result.message;
            renderBoard();
            document.getElementById('ai-stats').textContent = '';
            return;
        }
        
        activeBoard = result.next_board;
        currentPlayer = 'O';
        renderBoard();
        
        if (!gameOver) {
            document.getElementById('game').classList.add('loading');
            
            setTimeout(async () => {
                try {
                    const aiResponse = await fetch('/ai_move', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            board: board,
                            active_board: activeBoard,
                            depth: difficulty
                        })
                    });
                    
                    const aiResult = await aiResponse.json();
                    
                    document.getElementById('ai-stats').textContent = 
                        `AI ran ${aiResult.simulations.toLocaleString()} simulations in ${aiResult.time_spent}s (Win probability: ${aiResult.win_prob}%)`;
                    
                    const moveResponse = await fetch('/move', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            board: board,
                            big_row: aiResult.move[0],
                            big_col: aiResult.move[1],
                            small_row: aiResult.move[2],
                            small_col: aiResult.move[3],
                            player: 'O',
                            active_board: activeBoard
                        })
                    });
                    
                    const moveResult = await moveResponse.json();
                    
                    if (moveResult.success) {
                        board = moveResult.new_board;
                        
                        if (moveResult.message) {
                            gameOver = true;
                            statusMessage = moveResult.message;
                        } else {
                            activeBoard = moveResult.next_board;
                            currentPlayer = 'X';
                        }
                    }
                    
                    document.getElementById('game').classList.remove('loading');
                    renderBoard();
                } catch (error) {
                    console.error('AI move error:', error);
                    document.getElementById('game').classList.remove('loading');
                    document.getElementById('status').textContent = 'AI error: ' + error.message;
                }
            }, 500);
        }
    } catch (error) {
        console.error('Move error:', error);
        document.getElementById('status').textContent = 'Move error: ' + error.message;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('reset').onclick = async () => {
        try {
            await fetchGameState();
            document.getElementById('ai-stats').textContent = '';
            document.getElementById('game').classList.remove('loading');
        } catch (error) {
            console.error('Reset error:', error);
        }
    };

    document.getElementById('difficulty').onchange = () => {
        difficulty = parseInt(document.getElementById('difficulty').value);
    };

    fetchGameState();
});