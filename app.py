from flask import Flask, render_template, jsonify, request
from game_logic import create_board, check_winner, is_board_full, get_board_index, deep_copy_board, make_move, evaluate_board, get_valid_moves, alpha_beta, ai_make_move, reset_game
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset')
def reset():
    board, active_board, current_player, game_over = reset_game()
    return jsonify({
        'board': board,
        'active_board': active_board,
        'current_player': current_player,
        'game_over': game_over
    })

@app.route('/move', methods=['POST'])
def handle_move():
    data = request.json
    result = make_move(
        data['board'],
        data['big_row'],
        data['big_col'],
        data['small_row'],
        data['small_col'],
        data['player'],
        data.get('active_board')
    )
    return jsonify({
        'success': result[0],
        'new_board': result[1],
        'next_board': result[2],
        'message': result[3]
    })

@app.route('/ai_move', methods=['POST'])
def handle_ai_move():
    data = request.json
    start_time = time.time()
    move, simulations, win_prob, time_spent = ai_make_move(
        data['board'],
        data['active_board'],
        data['depth']
    )
    return jsonify({
        'move': move,
        'simulations': simulations,
        'win_prob': win_prob,
        'time_spent': time_spent
    })

if __name__ == '__main__':
    app.run(debug=True)