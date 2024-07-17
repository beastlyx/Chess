
class MoveLog:
    def __init__(self, board, piece, captured_piece, old_pos, new_pos, is_promotion, is_castle, is_enpassant, original_pawn):
        self.board = board
        self.piece = piece
        self.captured_piece = captured_piece
        self.old_pos = old_pos
        self.new_pos = new_pos
        self.is_promotion = is_promotion
        self.is_castle = is_castle
        self.is_enpassant = is_enpassant
        self.original_pawn = original_pawn
        self.column_coordinates = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.row_coordinates = ['8', '7', '6', '5', '4', '3', '2', '1']
        self.duplicate = self.check_for_duplicate_move()
        self.move = None
        self.log_move()

    def log_move(self):
        coordinate = self.piece.piece_coordinates
        old_row = self.row_coordinates[self.old_pos[0]]
        old_col = self.column_coordinates[self.old_pos[1]]
        new_col = self.column_coordinates[self.new_pos[1]]
        new_row = self.row_coordinates[self.new_pos[0]]
        capture = 'x' if self.captured_piece is not None else ''

        if self.piece.piece_type == 'pawn':
            self.log_move_pawn()
        elif self.piece.piece_type == 'king' and self.is_castle:
            self.log_move_castle()
        elif self.duplicate:
            other_position = self.check_same_move()
            if other_position[0] != self.old_pos[0]:
                self.move = f'{coordinate}{old_row}{capture}{new_col}{new_row}'
            else:
                self.move = f'{coordinate}{old_col}{capture}{new_col}{new_row}'
        else:
            self.move = f'{coordinate}{capture}{new_col}{new_row}'

    def log_move_pawn(self):
        if self.captured_piece is None:
            to_col = self.column_coordinates[self.new_pos[1]]
            to_row = self.row_coordinates[self.new_pos[0]]
            coordinate = self.piece.piece_coordinates
            if self.piece.piece_type == 'pawn':
                self.move = f'{to_col}{to_row}'
            else:
                self.move = f'{to_col}{to_row}={coordinate}'
        else:
            from_col = self.column_coordinates[self.old_pos[1]]
            to_col = self.column_coordinates[self.new_pos[1]]
            to_row = self.row_coordinates[self.new_pos[0]]
            coordinate = self.piece.piece_coordinates
            if self.piece.piece_type == 'pawn':
                if self.is_enpassant:
                    self.move = f'{from_col}x{to_col}{to_row}e/p'
                else:
                    self.move = f'{from_col}x{to_col}{to_row}'
            else:
                self.move = f'{from_col}x{to_col}{to_row}={coordinate}'

    def log_move_castle(self):
        # if self.is_castle and (self.new_pos[0] == 0 or self.new_pos[0] == 7):
        if self.new_pos[1] == 6:
            self.move = '0-0'
        else:
            self.move = '0-0-0'
        # else:


    def check_for_duplicate_move(self):
        other_piece_position = self.check_same_move()
        if other_piece_position is not None:
            other_piece = self.board.get_piece(other_piece_position[0], other_piece_position[1])
            if other_piece is not None:
                other_piece_moves = other_piece.set_legal_moves(self.board)
                current_piece_moves = self.piece.set_legal_moves(self.board)
                move_set = list(set(current_piece_moves) & set(other_piece_moves))
                if self.new_pos in move_set:
                    return True
        return False

    def check_same_move(self):
        if self.piece.piece_type == 'pawn':
            return
        old_pos = self.old_pos
        new_pos = self.new_pos
        for row in range(8):
            for col in range(8):
                dup_piece = self.board[row][col]
                if dup_piece is not None and dup_piece.piece_type == self.piece.piece_type:
                    if dup_piece.color == self.piece.color and new_pos != (row, col) and old_pos != (row, col):
                        return row, col
        return None

    def get_move(self):
        return self
