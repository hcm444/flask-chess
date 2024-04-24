from flask import Flask, render_template, request, jsonify
import chess
from chess import *
app = Flask(__name__)
en_passant_target = None
initial_positions = [[None] * size for _ in range(size)]
for i in range(size):
    for j in range(size):
        initial_positions[i][j] = (i, j)

@app.route('/current_player')
def get_current_player():
    return jsonify({'current_player': current_player})

@app.route('/')
def chessboard():
    return render_template('chessboard.html', size=size, pieces=pieces, current_player=current_player)


@app.route('/move_piece', methods=['POST'])
def move_piece():
    if request.method == 'POST':
        data = request.get_json()
        from_row = data['from_row']
        from_col = data['from_col']
        to_row = data['to_row']
        to_col = data['to_col']

        piece = pieces[from_row][from_col]
        if piece is None:
            return jsonify({'error': 'No piece at the selected position'})

        color = piece.split('_')[0]
        piece_type = piece.split('_')[1]

        # Check if it's the current player's turn
        if color != chess.current_player:
            return jsonify({'error': 'It\'s not your turn!'})

        if piece_type == 'knight':
            valid_move = move_piece_knight(from_row, from_col, to_row, to_col, color)
        elif piece_type == 'rook':
            valid_move = move_piece_rook(from_row, from_col, to_row, to_col, color)
        elif piece_type == 'bishop':
            valid_move = move_piece_bishop(from_row, from_col, to_row, to_col, color)
        elif piece_type == 'queen':
            valid_move = move_piece_queen(from_row, from_col, to_row, to_col, color)
        elif piece_type == 'king':
            valid_move = move_piece_king(from_row, from_col, to_row, to_col, color)
        elif piece_type == 'pawn':
            valid_move = move_piece_pawn(from_row, from_col, to_row, to_col, color)
        else:
            # Handle other piece types
            valid_move = False

        if valid_move:
            # Validate the move without making it
            temp_piece_from = pieces[from_row][from_col]
            temp_piece_to = pieces[to_row][to_col]

            pieces[to_row][to_col] = temp_piece_from
            pieces[from_row][from_col] = None

            own_king_in_check = is_king_in_check(color)

            # Undo the temporary move
            pieces[from_row][from_col] = temp_piece_from
            pieces[to_row][to_col] = temp_piece_to

            if own_king_in_check:
                return jsonify({'error': 'Move leaves your king in check'})

            # If the move doesn't put the king in check, apply it
            pieces[to_row][to_col] = temp_piece_from
            pieces[from_row][from_col] = None

            # Update movement history
            if (to_row, to_col) != initial_positions[from_row][from_col]:
                chess.movement_history[from_row][from_col] = True
            if is_king_in_check("white"):
                print("Player White in Check!")
            if is_king_in_check("black"):
                print("Player Black in Check!")
            switch_turn()  # Switch turn after successful move
            # Check for pawn promotion
            if piece_type == 'pawn':
                promoted_piece = promote_pawn(to_row, to_col, color)
                if promoted_piece:
                    pieces[to_row][to_col] = promoted_piece
            return jsonify({'pieces': pieces})
        else:
            return jsonify({'error': 'Invalid move'})

@app.route('/keypress', methods=['POST'])
def key_press():
    key = request.form['key']
    if key.lower() in ['q', 'k', 'r', 'b']:
        print(f"Key '{key}' was pressed")
    return jsonify({'message': 'Key press handled'})

if __name__ == '__main__':
    app.run(debug=True)