size = 8
pieces = [
    ['black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight',
     'black_rook'],
    ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn',
     'black_pawn'],
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn',
     'white_pawn'],
    ['white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight',
     'white_rook']
]
current_player = 'white'
movement_history = [[False] * size for _ in range(size)]


def is_square_empty(row, col):
    return pieces[row][col] is None


def is_king_in_check(color):
    # Find the position of the king of the given color
    king_row, king_col = None, None
    for row_idx, row in enumerate(pieces):
        for col_idx, piece in enumerate(row):
            if piece and piece == f'{color}_king':
                king_row, king_col = row_idx, col_idx
                break

    # Check if the king is threatened by any opponent's piece
    for row_idx, row in enumerate(pieces):
        for col_idx, piece in enumerate(row):
            if piece and piece.split('_')[0] != color:
                if piece.split('_')[1] == 'knight':
                    if move_piece_knight(row_idx, col_idx, king_row, king_col, piece.split('_')[0]):
                        return True
                elif piece.split('_')[1] == 'rook':
                    if move_piece_rook(row_idx, col_idx, king_row, king_col, piece.split('_')[0]):
                        return True
                elif piece.split('_')[1] == 'bishop':
                    if move_piece_bishop(row_idx, col_idx, king_row, king_col, piece.split('_')[0]):
                        return True
                elif piece.split('_')[1] == 'queen':
                    if move_piece_queen(row_idx, col_idx, king_row, king_col, piece.split('_')[0]):
                        return True
                elif piece.split('_')[1] == 'king':
                    if move_piece_king(row_idx, col_idx, king_row, king_col, piece.split('_')[0]):
                        return True
                elif piece.split('_')[1] == 'pawn':
                    if move_piece_pawn(row_idx, col_idx, king_row, king_col, piece.split('_')[0]):
                        return True
    return False


def promote_pawn(row, col, color):
    if color == 'white' and row == 0:
        return 'white_queen'
    elif color == 'black' and row == 7:
        return 'black_queen'
    else:
        return None


def switch_turn():
    global current_player
    if current_player == 'white':
        current_player = 'black'
    else:
        current_player = 'white'


def is_valid_move(from_row, from_col, to_row, to_col, color):
    if not (0 <= from_row < size and 0 <= from_col < size and 0 <= to_row < size and 0 <= to_col < size):
        return False

    if pieces[to_row][to_col] and pieces[to_row][to_col].split('_')[0] == color:
        return False

    return True


def move_piece_knight(from_row, from_col, to_row, to_col, color):
    row_diff = abs(to_row - from_row)
    col_diff = abs(to_col - from_col)

    if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
        if pieces[to_row][to_col] is None or pieces[to_row][to_col].split('_')[0] != color:
            return is_valid_move(from_row, from_col, to_row, to_col, color)
    return False


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
    if color == 'white':
        if from_row == 7 and from_col == 4:
            if to_row == 7 and to_col == 6:
                if is_square_empty(7, 5) and is_square_empty(7, 6):
                    if (movement_history[7][4]) is False and (movement_history[7][7]) is False and True:
                        pieces[7][5] = pieces[7][7]
                        pieces[7][7] = None
                        return True
        if from_row == 7 and from_col == 4:
            if to_row == 7 and to_col == 2:
                if is_square_empty(7, 1) and is_square_empty(7, 2) and is_square_empty(7, 3):
                    if (movement_history[7][4]) is False and (movement_history[7][0]) is False and True:
                        pieces[7][3] = pieces[7][0]
                        pieces[7][0] = None
                        return True
    else:
        if from_row == 0 and from_col == 4:
            if to_row == 0 and to_col == 6:
                if is_square_empty(0, 5) and is_square_empty(0, 6):
                    if (movement_history[0][4]) is False and (movement_history[0][7]) is False and True:
                        pieces[0][5] = pieces[0][7]
                        pieces[0][7] = None
                        return True
        if from_row == 0 and from_col == 4:
            if to_row == 0 and to_col == 2:
                if is_square_empty(0, 1) and is_square_empty(0, 2) and is_square_empty(0, 3):
                    if (movement_history[0][4]) is False and (movement_history[0][0]) is False and True:
                        pieces[0][3] = pieces[0][0]
                        pieces[0][0] = None
                        return True

    return (abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1) and \
        is_valid_move(from_row, from_col, to_row, to_col, color)


def move_piece_pawn(from_row, from_col, to_row, to_col, color):
    global en_passant_target

    if color == 'white':
        direction = 1
        start_row = 6
        end_row = 0
        en_passant_row = start_row - 1

    else:
        direction = -1
        start_row = 1
        end_row = 7
        en_passant_row = start_row + 1

    if to_row == end_row:
        if pieces[to_row][to_col] is None:
            pieces[from_row][from_col] = None
            switch_turn()  # Switch turn after pawn promotion
            return True
    if from_col == to_col:
        if from_row - to_row == direction:
            # Moving forward by one square
            if pieces[to_row][to_col] is None:
                return True
        elif abs(from_row - to_row) == 2 and from_row == start_row:
            en_passant_target = (en_passant_row, from_col)
            # Moving forward by two squares from starting position
            if pieces[to_row][to_col] is None:
                return True
    elif abs(from_col - to_col) == 1 and from_row - to_row == direction:

        # Capturing diagonally
        if (to_row, to_col) == en_passant_target:
            # Moving diagonally into the en passant target square
            if color == "white":
                pieces[to_row + 1][to_col] = None
            if color == "black":
                pieces[to_row - 1][to_col] = None
            # Remove the enemy pawn from the correct column
            en_passant_target = None
            return True
        elif pieces[to_row][to_col] and pieces[to_row][to_col].split('_')[0] != color:
            return True

    return False
