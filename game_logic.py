import random
import time
import math

def create_board():
    """Create a new empty ultimate tic-tac-toe board"""
    return [[[' ' for _ in range(3)] for _ in range(3)] for _ in range(9)]

def check_winner(board):
    """Check if there's a winner in a 3x3 board"""
    lines = [
        [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]
    ]
    for line in lines:
        a, b, c = line
        if (board[a[0]][a[1]] != ' ' and 
            board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]]):
            return board[a[0]][a[1]]
    return None

def is_board_full(board):
    """Check if a 3x3 board is full"""
    return all(cell != ' ' for row in board for cell in row)

def get_board_index(row, col):
    """Convert 2D board coordinates to 1D index"""
    return row * 3 + col

def deep_copy_board(board):
    """Create a deep copy of the board"""
    return [[[cell for cell in row] for row in small_board] for small_board in board]

def make_move(board, big_row, big_col, small_row, small_col, player, active_board=None):
    """Make a move and return (success, new_board, next_board, message)"""
    board_idx = get_board_index(big_row, big_col)
    sub_board = board[board_idx]
    
    # Check if we're forced to play in this board
    if active_board is not None and board_idx != active_board:
        return False, board, None, "Must play in the specified board"
    
    # Check if sub-board is already completed
    sub_winner = check_winner(sub_board)
    if sub_winner or is_board_full(sub_board):
        return False, board, None, "This board is already completed"
    
    # Check if cell is empty
    if sub_board[small_row][small_col] != ' ':
        return False, board, None, "Cell already taken"
    
    new_board = deep_copy_board(board)
    new_board[board_idx][small_row][small_col] = player
    
    # Check if this move won the sub-board
    winner = check_winner(new_board[board_idx])
    next_board_idx = get_board_index(small_row, small_col)
    
    # Check if next board is playable
    if next_board_idx is not None:
        next_board_winner = check_winner(new_board[next_board_idx])
        if next_board_winner or is_board_full(new_board[next_board_idx]):
            next_board_idx = None  # Free choice if next board is completed
    
    # Check if game is won
    big_board = []
    for i in range(3):
        big_row = []
        for j in range(3):
            small_board_idx = get_board_index(i, j)
            winner = check_winner(new_board[small_board_idx])
            if winner:
                big_row.append(winner)
            elif is_board_full(new_board[small_board_idx]):
                big_row.append('T')
            else:
                big_row.append(None)
        big_board.append(big_row)
    
    game_winner = check_winner(big_board)
    if game_winner:
        return True, new_board, None, f"Player {game_winner} wins the game!"
    
    # Check if game is tied
    if all(cell is not None for row in big_board for cell in row):
        x_wins = sum(1 for row in big_board for cell in row if cell == 'X')
        o_wins = sum(1 for row in big_board for cell in row if cell == 'O')
        if x_wins > o_wins:
            return True, new_board, None, "Player X wins by majority!"
        elif o_wins > x_wins:
            return True, new_board, None, "Player O wins by majority!"
        else:
            return True, new_board, None, "Game is a draw!"
    
    return True, new_board, next_board_idx, None

def evaluate_board(board):
    """Evaluate the current board position for AI"""
    big_board = [[check_winner(board[get_board_index(i, j)]) for j in range(3)] for i in range(3)]
    
    # Check for immediate wins/losses
    game_winner = check_winner(big_board)
    if game_winner == 'O':
        return 1000
    elif game_winner == 'X':
        return -1000
    
    score = 0
    
    # Evaluate small boards
    for i in range(9):
        small_winner = check_winner(board[i])
        if small_winner == 'O':
            score += 100
        elif small_winner == 'X':
            score -= 100
        elif not is_board_full(board[i]):
            # Evaluate potential in incomplete boards
            for line in [[(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
                         [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
                         [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]]:
                values = [board[i][x][y] for (x,y) in line]
                if values.count('O') == 2 and values.count(' ') == 1:
                    score += 10
                if values.count('X') == 2 and values.count(' ') == 1:
                    score -= 10
    
    # Evaluate big board potential
    for line in [[(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
                 [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
                 [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]]:
        values = [big_board[x][y] for (x,y) in line]
        if values.count('O') == 2 and values.count(None) == 1:
            score += 30
        if values.count('X') == 2 and values.count(None) == 1:
            score -= 30
    
    return score

def get_valid_moves(board, active_board):
    """Get all valid moves for the current state"""
    moves = []
    if active_board is None:
        # Can play in any unfinished board
        for board_idx in range(9):
            if check_winner(board[board_idx]) is None and not is_board_full(board[board_idx]):
                big_row, big_col = divmod(board_idx, 3)
                for r in range(3):
                    for c in range(3):
                        if board[board_idx][r][c] == ' ':
                            moves.append((big_row, big_col, r, c))
    else:
        # Must play in the specified board
        if check_winner(board[active_board]) is None and not is_board_full(board[active_board]):
            big_row, big_col = divmod(active_board, 3)
            for r in range(3):
                for c in range(3):
                    if board[active_board][r][c] == ' ':
                        moves.append((big_row, big_col, r, c))
    return moves

def alpha_beta(board, depth, active_board, alpha, beta, maximizing):
    """Alpha-beta pruning minimax algorithm"""
    valid_moves = get_valid_moves(board, active_board)
    
    if depth == 0 or not valid_moves:
        return evaluate_board(board), None
    
    if maximizing:
        max_eval = -math.inf
        best_move = None
        for move in valid_moves:
            big_row, big_col, small_row, small_col = move
            success, new_board, next_board, _ = make_move(
                board, big_row, big_col, small_row, small_col, 'O', active_board)
            
            if not success:
                continue
                
            eval_score, _ = alpha_beta(new_board, depth-1, next_board, alpha, beta, False)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
                
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
                
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        for move in valid_moves:
            big_row, big_col, small_row, small_col = move
            success, new_board, next_board, _ = make_move(
                board, big_row, big_col, small_row, small_col, 'X', active_board)
            
            if not success:
                continue
                
            eval_score, _ = alpha_beta(new_board, depth-1, next_board, alpha, beta, True)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
                
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
                
        return min_eval, best_move

def ai_make_move(board, active_board, depth):
    """Make AI move and return statistics"""
    start_time = time.time()
    score, best_move = alpha_beta(board, depth, active_board, -math.inf, math.inf, True)
    time_spent = time.time() - start_time
    
    if best_move:
        # Calculate win probability based on score
        win_prob = min(95, max(5, 50 + score//10))
        simulations = pow(3, depth)  # Estimate simulations based on depth
        return best_move, simulations, win_prob, round(time_spent, 2)
    
    # Fallback to random move if no best move found
    valid_moves = get_valid_moves(board, active_board)
    if valid_moves:
        return random.choice(valid_moves), 0, 50, 0
    
    return None, 0, 0, 0

def reset_game():
    """Reset the game to initial state"""
    return create_board(), None, 'X', False