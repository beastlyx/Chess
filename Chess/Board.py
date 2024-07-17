import sys
import pygame

from GamePieces import Rook, Bishop, Knight, Queen, King, Pawn
from MoveLog import MoveLog
from BoardState import BoardState

class Board:
    def __init__(self, chess=None):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.move_log = []
        self.chess = chess
        self.black_king_position = (0, 4)
        self.white_king_position = (7, 4)
        self.test = False
        self.undone_moves = BoardState()

        rook_black_1 = Rook(0, 0, "black", '1b')
        rook_white_1 = Rook(7, 0, "white", '1w')
        rook_black_2 = Rook(0, 7, "black", '2b')
        rook_white_2 = Rook(7, 7, "white", '2w')

        bishop_black_1 = Bishop(0, 2, "black")
        bishop_white_1 = Bishop(7, 2, "white")
        bishop_black_2 = Bishop(0, 5, "black")
        bishop_white_2 = Bishop(7, 5, "white")

        knight_black_1 = Knight(0, 1, "black")
        knight_white_1 = Knight(7, 1, "white")
        knight_black_2 = Knight(0, 6, "black")
        knight_white_2 = Knight(7, 6, "white")

        queen_black = Queen(0, 3, "black")
        queen_white = Queen(7, 3, "white")

        king_black = King(0, 4, "black")
        king_white = King(7, 4, "white")

        self.board[0][0] = rook_black_1
        self.board[0][1] = knight_black_1
        self.board[0][2] = bishop_black_1
        self.board[0][3] = queen_black
        self.board[0][4] = king_black
        self.board[0][5] = bishop_black_2
        self.board[0][6] = knight_black_2
        self.board[0][7] = rook_black_2

        for i in range(8):
            self.board[1][i] = Pawn(1, i, "black")
            self.board[6][i] = Pawn(6, i, "white")

        self.board[7][0] = rook_white_1
        self.board[7][1] = knight_white_1
        self.board[7][2] = bishop_white_1
        self.board[7][3] = queen_white
        self.board[7][4] = king_white
        self.board[7][5] = bishop_white_2
        self.board[7][6] = knight_white_2
        self.board[7][7] = rook_white_2

    def __getitem__(self, item):
        return self.board[item]

    def __setitem__(self, key, value):
        self.board[key] = value

    def make_move(self, game_piece, from_pos, new_pos, is_promotion, is_castle, is_enpassant, original_pawn):
        curr_row, curr_col = from_pos
        captured_piece = self.board[new_pos[0]][new_pos[1]]
        if is_enpassant:
            if game_piece.color == 'white':
                captured_piece = self.board[new_pos[0] + 1][new_pos[1]]
                self.board[new_pos[0] + 1][new_pos[1]] = None
            else:
                captured_piece = self.board[new_pos[0] - 1][new_pos[1]]
                self.board[new_pos[0] - 1][new_pos[1]] = None
        self.board[curr_row][curr_col] = None
        self.board[new_pos[0]][new_pos[1]] = None
        self.board[new_pos[0]][new_pos[1]] = game_piece
        game_piece.position = (new_pos[0], new_pos[1])
        if game_piece.piece_type == 'king':
            if game_piece.color == 'white':
                self.white_king_position = new_pos
            else:
                self.black_king_position = new_pos

        if is_castle and game_piece.piece_type == 'rook':
            return
        self.move_log.append(MoveLog(self.get_board(), game_piece, captured_piece, from_pos, new_pos, is_promotion, is_castle, is_enpassant, original_pawn))

    def move_piece(self, game_piece, new_pos, test=False): #, legal_captures, test=False):
        self.test = test
        # if self.board[new_pos[0]][new_pos[1]] is None or (self.board[new_pos[0]][new_pos[1]] is not None and (new_pos[0], new_pos[1]) in legal_captures):
        if game_piece.piece_type == 'pawn':
            self.move_pawn(game_piece, new_pos)
        elif game_piece.piece_type == 'king' and not game_piece.piece_moved:
            self.move_king(game_piece, new_pos)
        else:
            self.make_move(game_piece, game_piece.position, new_pos, False, False, False, None)

    def move_pawn(self, game_piece, new_pos):
        row, col = game_piece.position
        # white promotion
        if game_piece.color == 'white' and new_pos[0] == 0:
            original_pawn = self.board[row][col]
            self.board[row][col] = None
            new_piece = self.handle_pawn_promotion(new_pos)
            self.make_move(new_piece, (row, col), new_pos, True, False, False, original_pawn)
        # black promotion to queen
        elif game_piece.color == 'black' and new_pos[0] == 7:
            original_pawn = self.board[row][col]
            self.board[row][col] = None
            new_piece = self.handle_pawn_promotion(new_pos)
            self.make_move(new_piece, (row, col), new_pos, True, False, False, original_pawn)
        # white en passant capture
        elif game_piece.color == 'white' and row == 3 and self.board[new_pos[0]][new_pos[1]] is None:
            if new_pos == (row - 1, col - 1) or new_pos == (row - 1, col + 1):
                self.make_move(game_piece, (row, col), new_pos, False, False, True, None)
            else:
                self.make_move(game_piece, (row, col), new_pos, False, False, False, None)
        # black en passant capture
        elif game_piece.color == 'black' and row == 4 and self.board[new_pos[0]][new_pos[1]] is None:
            if new_pos == (row + 1, col - 1) or new_pos == (row + 1, col + 1):
                self.make_move(game_piece, (row, col), new_pos, False, False, True, None)
            else:
                self.make_move(game_piece, (row, col), new_pos, False, False, False, None)
        else:
            self.make_move(game_piece, (row, col), new_pos, False, False, False, None)

    def move_king(self, game_piece, new_pos):
        curr_row, curr_col = game_piece.position
        is_castling = abs(curr_col - new_pos[1]) == 2

        if is_castling:
            # Kingside castling
            if new_pos[1] > curr_col:
                rook_initial_pos = (curr_row, 7)
                rook_final_pos = (new_pos[0], new_pos[1] - 1)
            # Queenside castling
            else:
                rook_initial_pos = (curr_row, 0)
                rook_final_pos = (new_pos[0], new_pos[1] + 1)
            rook = self[rook_initial_pos[0]][rook_initial_pos[1]]
            # king's move
            self.make_move(game_piece, game_piece.position, new_pos, False, True, False, None)
            # rook's move
            self.make_move(rook, rook_initial_pos, rook_final_pos, False, True, False, None)
        else:
            # Regular king move
            self.make_move(game_piece, game_piece.position, new_pos, False, False, False, None)

    def display_promotion_box(self, new_pos):
        row, col = new_pos
        color = 'white' if row == 0 else 'black'
        BOARD_OFFSET_X = 200
        BOARD_OFFSET_Y = 100
        SQUARE_SIZE = 50

        vertical_pos = BOARD_OFFSET_Y-75 if color == 'white' else BOARD_OFFSET_Y+400
        horizontal_pos = (BOARD_OFFSET_X + (SQUARE_SIZE * (col + 1)) - 150)

        box_position = (horizontal_pos, vertical_pos)
        original_box_img = pygame.image.load("Pieces/box.png") if color == 'white' else pygame.transform.rotate(pygame.image.load("Pieces/box.png"), 180)
        box_img = pygame.transform.smoothscale(original_box_img, (250, 75))

        queen_img = pygame.image.load("Pieces/white_queen.png") if color == 'white' else pygame.image.load("Pieces/black_queen.png")
        rook_img = pygame.image.load('Pieces/white_rook.png') if color == 'white' else pygame.image.load('Pieces/black_rook.png')
        bishop_img = pygame.image.load("Pieces/white_bishop.png") if color == 'white' else pygame.image.load("Pieces/black_bishop.png")
        knight_img = pygame.image.load("Pieces/white_knight.png") if color == 'white' else pygame.image.load("Pieces/black_knight.png")

        self.chess.screen.blit(box_img, box_position)
        images = [queen_img, rook_img, bishop_img, knight_img]

        for i in range(4):
            x = 22 + box_position[0] + (i * 55)
            y = box_position[1] + 8 if color == 'white' else box_position[1] + 24
            self.chess.screen.blit(images[i], (x, y))

        pygame.display.update()

    def handle_pawn_promotion(self, new_pos):
        if self.test:
            return Queen(new_pos[0], new_pos[1], 'white' if new_pos[0] == 0 else 'black')
        self.display_promotion_box(new_pos)

        row, col = new_pos
        color = 'white' if row == 0 else 'black'

        selected_piece = None

        BOARD_OFFSET_X = 200
        BOARD_OFFSET_Y = 100
        SQUARE_SIZE = 50

        vertical_pos = BOARD_OFFSET_Y - 75 if color == 'white' else BOARD_OFFSET_Y + 400
        horizontal_pos = (BOARD_OFFSET_X + (SQUARE_SIZE * (col + 1)) - 150)

        # vertical_pos = 225 if color == 'white' else 700
        # horizontal_pos = (400 + (50 * (col + 1)) - 150)
        top_margin = 8 if color == 'white' else 24

        while not selected_piece:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i in range(4):
                        piece_x_start = horizontal_pos + 22 + (i * 55)
                        piece_y_start = vertical_pos + top_margin
                        piece_x_end = piece_x_start + 45
                        piece_y_end = piece_y_start + 45
                        if piece_x_start <= x <= piece_x_end and piece_y_start <= y <= piece_y_end:
                            selected_piece = i + 1
                            break
        piece = None
        if selected_piece == 1:
            piece = Queen(new_pos[0], new_pos[1], color)
        elif selected_piece == 2:
            piece = Rook(new_pos[0], new_pos[1], color)
        elif selected_piece == 3:
            piece = Bishop(new_pos[0], new_pos[1], color)
        elif selected_piece == 4:
            piece = Knight(new_pos[0], new_pos[1], color)
        return piece

    def get_king_position(self, color):
        return self.white_king_position if color == 'white' else self.black_king_position

    def get_board(self):
        return self

    def get_piece(self, row, col):
        return self[row][col]

    def get_log(self):
        return self.move_log

    def set_turn(self):
        self.chess.white_move = not self.chess.white_move
