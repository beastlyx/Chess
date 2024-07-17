import pygame

from CheckConditions import CheckConditions
from UndoMove import UndoMove


class GamePieces:
    def __init__(self, row, col, color):
        self.legal_moves = []
        self.legal_captures = []
        self.img = None
        self.original_position = (row, col)
        self.position = (row, col)
        self.color = color
        self.piece_type = None
        self.piece_moved = False
        self.piece_coordinates = None
        self.id = None
        self.points = 0

    def get_image_path(self):
        return "Pieces/" + self.color + "_" + self.piece_type + ".png"

    def set_legal_moves(self, board):
        getattr(self, f"_calculate_{self.piece_type}_moves")(board)
        return self.legal_moves

    def get_legal_moves(self, board):
        getattr(self, f"_calculate_{self.piece_type}_moves")(board)
        return self.legal_moves

    def get_legal_captures(self, board):
        getattr(self, f"_calculate_{self.piece_type}_captures")(board)
        return self.legal_captures

    def validate_legal_moves(self, board):
        getattr(self, f'_validate_{self.piece_type}_moves')(board)
        return self.legal_moves


class Rook(GamePieces):
    def __init__(self, row, col, color, id=0):
        super().__init__(row, col, color)
        self.piece_type = 'rook'
        self.piece_coordinates = 'R'
        self.id = id
        self.img = pygame.image.load(self.get_image_path())
        self.points = 5

    def _calculate_rook_moves(self, board):
        row, col = self.position
        if not self.piece_moved and self.position != self.original_position:
            self.piece_moved = True
        left_horizontal = []
        for i in range(1, 8):
            if 0 <= col - i < 8:
                if board.get_piece(row, col - i) is None:
                    left_horizontal.append((row, col - i))
                elif board.get_piece(row, col - i).color != self.color:
                    left_horizontal.append((row, col - i))
                    break
                else:
                    break
        right_horizontal = []
        for i in range(1, 8):
            if 0 <= col + i < 8:
                if board.get_piece(row, col + i) is None:
                    right_horizontal.append((row, col + i))
                elif board.get_piece(row, col + i).color != self.color:
                    right_horizontal.append((row, col + i))
                    break
                else:
                    break
        vertical_top = []
        for i in range(1, 8):
            if 0 <= row - i < 8:
                if board.get_piece(row - i, col) is None:
                    vertical_top.append((row - i, col))
                elif board.get_piece(row - i, col).color != self.color:
                    vertical_top.append((row - i, col))
                    break
                else:
                    break
        vertical_down = []
        for i in range(1, 8):
            if 0 <= row + i < 8:
                if board.get_piece(row + i, col) is None:
                    vertical_down.append((row + i, col))
                elif board.get_piece(row + i, col).color != self.color:
                    vertical_down.append((row + i, col))
                    break
                else:
                    break

        self.legal_moves = left_horizontal + right_horizontal + vertical_top + vertical_down

    def _calculate_rook_captures(self, board):
        captures = []
        for move in self.legal_moves:
            if board.get_piece(move[0], move[1]) is not None and board.get_piece(move[0], move[1]).color != self.color:
                captures.append((move[0], move[1]))
        self.legal_captures = captures

    def _validate_rook_moves(self, board):
        moves = []
        for move in self.legal_moves:
            if not CheckConditions(board, self, move).validate_move():
                moves.append(move)
            UndoMove(board).undo()
        self.legal_moves = moves


class Knight(GamePieces):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.piece_type = 'knight'
        self.piece_coordinates = 'N'
        self.img = pygame.image.load(self.get_image_path())
        self.points = 3

    def _calculate_knight_moves(self, board):
        row, col = self.position
        moves = [[row - 2, col - 1], [row - 1, col - 2], [row + 1, col - 2], [row + 2, col - 1],
                 [row + 2, col + 1], [row + 1, col + 2], [row - 1, col + 2], [row - 2, col + 1]]
        knight_moves = []
        for move in moves:
            if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                if board.get_piece(move[0], move[1]) is None:
                    knight_moves.append((move[0], move[1]))
                elif board.get_piece(move[0], move[1]).color != self.color:
                    knight_moves.append((move[0], move[1]))
        self.legal_moves = knight_moves

    def _calculate_knight_captures(self, board):
        captures = []
        for move in self.legal_moves:
            if board.get_piece(move[0], move[1]) is not None and board.get_piece(move[0], move[1]).color != self.color:
                captures.append((move[0], move[1]))
        self.legal_captures = captures

    def _validate_knight_moves(self, board):
        moves = []
        for move in self.legal_moves:
            if not CheckConditions(board, self, move).validate_move():
                moves.append(move)
            UndoMove(board).undo()
        self.legal_moves = moves


class Bishop(GamePieces):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.piece_type = 'bishop'
        self.piece_coordinates = 'B'
        self.img = pygame.image.load(self.get_image_path())
        self.points = 3

    def _calculate_bishop_moves(self, board):
        row, col = self.position
        top_left_diagonal = []
        for i in range(1, 8):
            if 0 <= col - i < 8 and 0 <= row - i < 8:
                if board.get_piece(row - i, col - i) is None:
                    top_left_diagonal.append((row - i, col - i))
                elif board.get_piece(row - i, col - i).color != self.color:
                    top_left_diagonal.append((row - i, col - i))
                    break
                else:
                    break
        bottom_left_diagonal = []
        for i in range(1, 8):
            if 0 <= col - i < 8 and 0 <= row + i < 8:
                if board.get_piece(row + i, col - i) is None:
                    bottom_left_diagonal.append((row + i, col - i))
                elif board.get_piece(row + i, col - i).color != self.color:
                    bottom_left_diagonal.append((row + i, col - i))
                    break
                else:
                    break
        top_right_diagonal = []
        for i in range(1, 8):
            if 0 <= col + i < 8 and 0 <= row - i < 8:
                if board.get_piece(row - i, col + i) is None:
                    top_right_diagonal.append((row - i, col + i))
                elif board.get_piece(row - i, col + i).color != self.color:
                    top_right_diagonal.append((row - i, col + i))
                    break
                else:
                    break
        bottom_right_diagonal = []
        for i in range(1, 8):
            if 0 <= col + i < 8 and 0 <= row + i < 8:
                if board.get_piece(row + i, col + i) is None:
                    bottom_right_diagonal.append((row + i, col + i))
                elif board.get_piece(row + i, col + i).color != self.color:
                    bottom_right_diagonal.append((row + i, col + i))
                    break
                else:
                    break
        self.legal_moves = top_left_diagonal + top_right_diagonal + bottom_left_diagonal + bottom_right_diagonal

    def _calculate_bishop_captures(self, board):
        captures = []
        for move in self.legal_moves:
            if board.get_piece(move[0], move[1]) is not None and board.get_piece(move[0], move[1]).color != self.color:
                captures.append((move[0], move[1]))
        self.legal_captures = captures

    def _validate_bishop_moves(self, board):
        moves = []
        for move in self.legal_moves:
            if not CheckConditions(board, self, move).validate_move():
                moves.append(move)
            UndoMove(board).undo()
        self.legal_moves = moves


class Pawn(GamePieces):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.piece_type = 'pawn'
        self.piece_coordinates = ''
        self.img = pygame.image.load(self.get_image_path())
        self.points = 1

    def _calculate_pawn_moves(self, board):
        row, col = self.position
        pawn_moves = []
        # check for en passant for white
        if (row == 3 and self.color == 'white') or (row == 4 and self.color == 'black'):
            log = board.get_log()[-1]
            if log.piece.piece_type == 'pawn' and log.piece.color != self.color and abs(log.old_pos[0] - log.new_pos[0]) == 2 and log.new_pos[0] == self.position[0]:
                if self.color == 'white':
                    pawn_moves.append((log.piece.position[0] - 1, log.piece.position[1]))
                else:
                    pawn_moves.append((log.piece.position[0] + 1, log.piece.position[1]))
        if self.color == "white":
            if 0 <= row - 1 < 8 and board.get_piece(row - 1, col) is None:
                pawn_moves.append((row - 1, col))
            if row == 6 and board.get_piece(row - 1, col) is None and board.get_piece(row - 2, col) is None:
                pawn_moves.append((row - 2, col))
            # Capture moves for the white pawn
            if 0 <= row - 1 < 8 and 0 <= col - 1 < 8 and board.get_piece(row - 1, col - 1) is not None and board.get_piece(row - 1, col - 1).color != self.color:
                pawn_moves.append((row - 1, col - 1))
            if 0 <= row - 1 < 8 and 0 <= col + 1 < 8 and board.get_piece(row - 1, col + 1) is not None and board.get_piece(row - 1, col + 1).color != self.color:
                pawn_moves.append((row - 1, col + 1))
        else:
            if 0 <= row + 1 < 8 and board.get_piece(row + 1, col) is None:
                pawn_moves.append((row + 1, col))
            if row == 1 and board.get_piece(row + 1, col) is None and board.get_piece(row + 2, col) is None:
                pawn_moves.append((row + 2, col))
            # Capture moves for the black pawn
            if 0 <= row + 1 < 8 and 0 <= col - 1 < 8 and board.get_piece(row + 1, col - 1) is not None and board.get_piece(row + 1, col - 1).color != self.color:
                pawn_moves.append((row + 1, col - 1))
            if 0 <= row + 1 < 8 and 0 <= col + 1 < 8 and board.get_piece(row + 1, col + 1) is not None and board.get_piece(row + 1, col + 1).color != self.color:
                pawn_moves.append((row + 1, col + 1))
        self.legal_moves = pawn_moves

    def _calculate_pawn_captures(self, board):
        captures = []
        for move in self.legal_moves:
            if move[0] == self.position[0]:
                continue
            elif 0 <= move[0] < 8 and 0 <= move[1] < 8:
                if board.get_piece(move[0], move[1]) is not None and board.get_piece(move[0], move[1]).color != self.color:
                    captures.append((move[0], move[1]))
            self.legal_captures = captures

    def _validate_pawn_moves(self, board):
        moves = []
        for move in self.legal_moves:
            if not CheckConditions(board, self, move).validate_move():
                moves.append(move)
            UndoMove(board).undo()
        self.legal_moves = moves


class Queen(GamePieces):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.piece_type = 'queen'
        self.piece_coordinates = 'Q'
        self.img = pygame.image.load(self.get_image_path())
        self.points = 9

    def _calculate_queen_moves(self, board):
        row, col = self.position
        top_left_diagonal = []
        for i in range(1, 8):
            if 0 <= col - i < 8 and 0 <= row - i < 8:
                if board.get_piece(row - i, col - i) is None:
                    top_left_diagonal.append((row - i, col - i))
                elif board.get_piece(row - i, col - i).color != self.color:
                    top_left_diagonal.append((row - i, col - i))
                    break
                else:
                    break

        bottom_left_diagonal = []
        for i in range(1, 8):
            if 0 <= col - i < 8 and 0 <= row + i < 8:
                if board.get_piece(row + i, col - i) is None:
                    bottom_left_diagonal.append((row + i, col - i))
                elif board.get_piece(row + i, col - i).color != self.color:
                    bottom_left_diagonal.append((row + i, col - i))
                    break
                else:
                    break

        top_right_diagonal = []
        for i in range(1, 8):
            if 0 <= col + i < 8 and 0 <= row - i < 8:
                if board.get_piece(row - i, col + i) is None:
                    top_right_diagonal.append((row - i, col + i))
                elif board.get_piece(row - i, col + i).color != self.color:
                    top_right_diagonal.append((row - i, col + i))
                    break
                else:
                    break

        bottom_right_diagonal = []
        for i in range(1, 8):
            if 0 <= col + i < 8 and 0 <= row + i < 8:
                if board.get_piece(row + i, col + i) is None:
                    bottom_right_diagonal.append((row + i, col + i))
                elif board.get_piece(row + i, col + i).color != self.color:
                    bottom_right_diagonal.append((row + i, col + i))
                    break
                else:
                    break

        left_horizontal = []
        for i in range(1, 8):
            if 0 <= col - i < 8:
                if board.get_piece(row, col - i) is None:
                    left_horizontal.append((row, col - i))
                elif board.get_piece(row, col - i).color != self.color:
                    left_horizontal.append((row, col - i))
                    break
                else:
                    break

        right_horizontal = []
        for i in range(1, 8):
            if 0 <= col + i < 8:
                if board.get_piece(row, col + i) is None:
                    right_horizontal.append((row, col + i))
                elif board.get_piece(row, col + i).color != self.color:
                    right_horizontal.append((row, col + i))
                    break
                else:
                    break

        vertical_top = []
        for i in range(1, 8):
            if 0 <= row - i < 8:
                if board.get_piece(row - i, col) is None:
                    vertical_top.append((row - i, col))
                elif board.get_piece(row - i, col).color != self.color:
                    vertical_top.append((row - i, col))
                    break
                else:
                    break

        vertical_down = []
        for i in range(1, 8):
            if 0 <= row + i < 8:
                if board.get_piece(row + i, col) is None:
                    vertical_down.append((row + i, col))
                elif board.get_piece(row + i, col).color != self.color:
                    vertical_down.append((row + i, col))
                    break
                else:
                    break
        self.legal_moves = top_left_diagonal + top_right_diagonal + bottom_left_diagonal + bottom_right_diagonal + left_horizontal + right_horizontal + vertical_top + vertical_down

    def _calculate_queen_captures(self, board):
        captures = []
        for move in self.legal_moves:
            if board.get_piece(move[0], move[1]) is not None and board.get_piece(move[0], move[1]).color != self.color:
                captures.append((move[0], move[1]))
        self.legal_captures = captures

    def _validate_queen_moves(self, board):
        moves = []
        for move in self.legal_moves:
            if not CheckConditions(board, self, move).validate_move():
                moves.append(move)
            UndoMove(board).undo()
        self.legal_moves = moves

class King(GamePieces):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.piece_type = 'king'
        self.piece_coordinates = 'K'
        self.img = pygame.image.load(self.get_image_path())

    def _calculate_king_moves(self, board):
        row, col = self.position
        if not self.piece_moved and self.position != self.original_position:
            self.piece_moved = True
        king_moves = [(row + i, col + j) for i in range(-1, 2) for j in range(-1, 2) if 0 <= row + i < 8 and 0 <= col + j < 8 and (i != 0 or j != 0) and
                      (board[row + i][col + j] is None or board[row + i][col + j].color != self.color)]
        # Add castling as a valid move if king and either rook did not move
        if not self.piece_moved:
            if self.color == 'white':
                if (board.get_piece(7, 5) is None and board.get_piece(7, 6) is None and board.get_piece(7, 7) is not None and board.get_piece(7, 7).piece_type == 'rook'
                        and not board.get_piece(7, 7).piece_moved):
                    if not CheckConditions(board, self).king_in_check_castle(((7, 6), (7, 5))):
                        # can castle to the right
                        king_moves.append((7, 5))
                        king_moves.append((7, 6))
                if (board.get_piece(7, 3) is None and board.get_piece(7, 2) is None and board.get_piece(7, 1) is None and board.get_piece(7, 0) is not None and
                        board.get_piece(7, 0).piece_type == 'rook' and not board.get_piece(7, 0).piece_moved):
                    if not CheckConditions(board, self).king_in_check_castle(((7, 3), (7, 2), (7, 1))):
                        king_moves.append((7, 3))
                        king_moves.append((7, 2))
            elif self.color == 'black':
                if (board.get_piece(0, 5) is None and board.get_piece(0, 6) is None and board.get_piece(0, 7) is not None and board.get_piece(0, 7).piece_type == 'rook'
                        and not board.get_piece(0, 7).piece_moved):
                    # can castle to the right if not in path of a check
                    if not CheckConditions(board, self).king_in_check_castle(((0, 6), (0, 5))):
                        king_moves.append((0, 5))
                        king_moves.append((0, 6))
                if (board.get_piece(0, 3) is None and board.get_piece(0, 2) is None and board.get_piece(0, 1) is None and board.get_piece(0, 0) is not None and
                        board.get_piece(0, 0).piece_type == 'rook' and not board.get_piece(0, 0).piece_moved):
                    if not CheckConditions(board, self).king_in_check_castle(((0, 3), (0, 2), (0, 1))):
                        king_moves.append((0, 3))
                        king_moves.append((0, 2))
        self.legal_moves = king_moves

    def _calculate_king_captures(self, board):
        captures = []
        for move in self.legal_moves:
            if board.get_piece(move[0], move[1]) is not None and board.get_piece(move[0], move[1]).color != self.color:
                captures.append((move[0], move[1]))
        self.legal_captures = captures

    def _validate_king_moves(self, board):
        moves = []
        for move in self.legal_moves:
            if not CheckConditions(board, self, move).validate_move():
                moves.append(move)
            UndoMove(board).undo()
        self.legal_moves = moves
