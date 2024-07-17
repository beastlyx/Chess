
class UndoMove:
    def __init__(self, board):
        self.board = board
        self.move_log = self.board.get_log()
        self.last_move = self.move_log.pop()

        self.board.undone_moves.add_move(self.last_move)

        self.piece = self.last_move.piece
        self.old_pos = self.last_move.old_pos
        self.new_pos = self.last_move.new_pos
        self.captured_piece = self.last_move.captured_piece

        self.is_promotion = self.last_move.is_promotion
        self.is_castle = self.last_move.is_castle
        self.is_enpassant = self.last_move.is_enpassant
        self.original_pawn = self.last_move.original_pawn

        self.distinguish = self.last_move.duplicate

    def undo(self):
        if self.is_castle:
            # kingside castle undo
            if self.new_pos[1] == 6:
                rook = self.board.get_piece(self.new_pos[0], self.new_pos[1] - 1)
                self.board[self.new_pos[0]][7] = rook
                self.board[self.new_pos[0]][self.new_pos[1] - 1] = None
                rook.position = (self.new_pos[0], 7)
            else:
                rook = self.board.get_piece(self.new_pos[0], self.new_pos[1] + 1)
                self.board[self.new_pos[0]][0] = rook
                self.board[self.new_pos[0]][self.new_pos[1] + 1] = None
                rook.position = (self.new_pos[0], 0)

            self.board[self.old_pos[0]][self.old_pos[1]] = self.piece
            self.board[self.new_pos[0]][self.new_pos[1]] = None
            self.piece.position = (self.old_pos[0], self.old_pos[1])
            rook.piece_moved = False
            self.piece.piece_moved = False

        elif self.is_promotion:
            self.board[self.new_pos[0]][self.new_pos[1]] = self.captured_piece
            self.board[self.old_pos[0]][self.old_pos[1]] = self.original_pawn
            if self.original_pawn is not None:
                self.original_pawn.position = (self.old_pos[0], self.old_pos[1])
            if self.captured_piece is not None:
                self.captured_piece.position = (self.new_pos[0], self.new_pos[1])

        elif self.is_enpassant:
            # Correctly restoring the captured pawn
            self.board[self.old_pos[0]][self.old_pos[1]] = self.piece
            self.board[self.new_pos[0]][self.new_pos[1]] = None
            self.piece.position = self.old_pos

            captured_row = self.old_pos[0]
            captured_col = self.new_pos[1]
            self.board[captured_row][captured_col] = self.captured_piece
            self.captured_piece.position = (captured_row, captured_col)

        else:
            self.board[self.new_pos[0]][self.new_pos[1]] = self.captured_piece
            self.board[self.old_pos[0]][self.old_pos[1]] = self.piece

            self.piece.position = (self.old_pos[0], self.old_pos[1])
            if self.captured_piece is not None:
                self.captured_piece.position = (self.new_pos[0], self.new_pos[1])

        self.piece.legal_moves = self.piece.set_legal_moves(self.board)
        self.piece.legal_captures = self.piece.get_legal_captures(self.board)

        if self.piece.piece_type == 'rook':
            count = 0
            for attr in self.move_log:
                if attr.piece.piece_type == 'rook' and attr.piece.id == self.piece.id:
                    count += 1
            if count == 0:
                self.piece.piece_moved = False

        if self.piece.piece_type == 'king':
            if self.piece.color == 'white':
                self.board.white_king_position = self.old_pos
            else:
                self.board.black_king_position = self.old_pos
