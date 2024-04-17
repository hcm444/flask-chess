from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Global variables to store board and piece positions
size = 8
pieces = [
    ['white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight',
     'white_rook'],
    ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn',
     'white_pawn'],
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn',
     'black_pawn'],
    ['black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight',
     'black_rook']
]

def is_valid_move(from_row, from_col, to_row, to_col, color):
    if not (0 <= from_row < size and 0 <= from_col < size and 0 <= to_row < size and 0 <= to_col < size):
        return False

    if pieces[to_row][to_col] and pieces[to_row][to_col].split('_')[0] == color:
        return False

    return True

def move_piece_knight(from_row, from_col, to_row, to_col, color):
    row_diff = abs(to_row - from_row)
    col_diff = abs(to_col - from_col)
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2) and \
           is_valid_move(from_row, from_col, to_row, to_col, color)

def move_piece_rook(from_row, from_col, to_row, to_col, color):
    if from_row == to_row:
        # Moving horizontally
        step = 1 if from_col < to_col else -1
        for col in range(from_col + step, to_col, step):
            if pieces[from_row][col]:
                return False
    elif from_col == to_col:
        # Moving vertically
        step = 1 if from_row < to_row else -1
        for row in range(from_row + step, to_row, step):
            if pieces[row][from_col]:
                return False
    else:
        return False

    return is_valid_move(from_row, from_col, to_row, to_col, color)

def move_piece_bishop(from_row, from_col, to_row, to_col, color):
    if abs(from_row - to_row) != abs(from_col - to_col):
        return False

    step_row = 1 if from_row < to_row else -1
    step_col = 1 if from_col < to_col else -1

    row, col = from_row + step_row, from_col + step_col
    while row != to_row and col != to_col:
        if pieces[row][col]:
            return False
        row += step_row
        col += step_col

    return is_valid_move(from_row, from_col, to_row, to_col, color)

def move_piece_queen(from_row, from_col, to_row, to_col, color):
    return move_piece_rook(from_row, from_col, to_row, to_col, color) or \
           move_piece_bishop(from_row, from_col, to_row, to_col, color)

def move_piece_king(from_row, from_col, to_row, to_col, color):
    return (abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1) and \
           is_valid_move(from_row, from_col, to_row, to_col, color)

def move_piece_pawn(from_row, from_col, to_row, to_col, color):
    if color == 'white':
        direction = -1
        start_row = 6
    else:
        direction = 1
        start_row = 1

    if from_col == to_col:
        if from_row - to_row == direction:
            # Moving forward by one square
            if pieces[to_row][to_col] is None:
                return True
        elif from_row - to_row == 2 * direction and from_row == start_row:
            # Moving forward by two squares from starting position
            if pieces[from_row + direction][from_col] is None and pieces[to_row][to_col] is None:
                return True
    elif abs(from_col - to_col) == 1 and from_row - to_row == direction:
        # Capturing diagonally
        if pieces[to_row][to_col] and pieces[to_row][to_col].split('_')[0] != color:
            return True

    return False

@app.route('/')
def chessboard():
    return render_template('chessboard.html', size=size, pieces=pieces)

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
            pieces[to_row][to_col] = piece
            pieces[from_row][from_col] = None
            return jsonify({'pieces': pieces})
        else:
            return jsonify({'error': 'Invalid move'})

if __name__ == '__main__':
    app.run(debug=True)
