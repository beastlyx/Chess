import pygame

BOARD_OFFSET_X_WHITE = 75
BOARD_OFFSET_X_BLACK = 625
BOARD_OFFSET_Y = 100
SQUARE_SIZE = 50


class CapturedPieces:
    def __init__(self, chess):
        self.white_pieces = [
            [{'Q': None}],
            [{'R': None}, {'R': None}],
            [{'B': None}, {'B': None}],
            [{'N': None}, {'N': None}],
            [{'': None}, {'': None}],
            [{'': None}, {'': None}],
            [{'': None}, {'': None}],
            [{'': None}, {'': None}]
        ]

        self.black_pieces = [
            [{'Q': None}],
            [{'R': None}, {'R': None}],
            [{'B': None}, {'B': None}],
            [{'N': None}, {'N': None}],
            [{'': None}, {'': None}],
            [{'': None}, {'': None}],
            [{'': None}, {'': None}],
            [{'': None}, {'': None}]
        ]

        self.chess = chess
        self.screen = self.chess.screen

    def display_white_captured_spots(self):
        for index, pieces in enumerate(self.white_pieces):
            for inner_index, piece in enumerate(pieces):
                for key, value in piece.items():
                    if value is not None:
                        piece_x_position = inner_index * SQUARE_SIZE + BOARD_OFFSET_X_WHITE + 25 - value.img.get_width() // 2
                        piece_y_position = index * SQUARE_SIZE + BOARD_OFFSET_Y + 25 - value.img.get_height() // 2
                        self.screen.blit(value.img, (piece_x_position, piece_y_position))
                    else:
                        pygame.draw.circle(self.screen, (192, 192, 192), (inner_index * SQUARE_SIZE + BOARD_OFFSET_X_WHITE + 25, index * SQUARE_SIZE + BOARD_OFFSET_Y + 25), 10)

    def display_black_captured_spots(self):
        for index, pieces in enumerate(self.black_pieces):
            for inner_index, piece in enumerate(pieces):
                for key, value in piece.items():
                    if value is not None:
                        piece_x_position = inner_index * SQUARE_SIZE + BOARD_OFFSET_X_BLACK + 25 - value.img.get_width() // 2
                        piece_y_position = index * SQUARE_SIZE + BOARD_OFFSET_Y + 25 - value.img.get_height() // 2
                        self.screen.blit(value.img, (piece_x_position, piece_y_position))
                    else:
                        if index == 0:
                            pygame.draw.circle(self.screen, (192, 192, 192), (inner_index * SQUARE_SIZE + BOARD_OFFSET_X_BLACK + 75, index * SQUARE_SIZE + BOARD_OFFSET_Y + 25), 10)
                        else:
                            pygame.draw.circle(self.screen, (192, 192, 192), (inner_index * SQUARE_SIZE + BOARD_OFFSET_X_BLACK + 25, index * SQUARE_SIZE + BOARD_OFFSET_Y + 25), 10)

    def capture_piece(self, move):
        if move.captured_piece is None:
            return
        color = move.captured_piece.color
        coordinate = move.captured_piece.piece_coordinates
        arr = self.black_pieces if color == 'black' else self.white_pieces
        for pieces in reversed(arr):
            for piece in reversed(pieces):
                for key, value in piece.items():
                    if value is None and key == coordinate:
                        piece[key] = move.captured_piece
                        return

    def undo_captured_piece(self, captured_piece):
        if captured_piece is None:
            return
        color = captured_piece.color
        coordinate = captured_piece.piece_coordinates
        arr = self.black_pieces if color == 'black' else self.white_pieces
        for pieces in arr:
            for piece in pieces:
                for key, value in piece.items():
                    if value is not None and key == coordinate:
                        piece[key] = None
                        return
