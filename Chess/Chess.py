import sys
import pygame

from Board import Board
from CapturedPieces import CapturedPieces
from CheckConditions import CheckConditions
from UndoMove import UndoMove

BOARD_OFFSET_X = 200
BOARD_OFFSET_Y = 100
SQUARE_SIZE = 50


class Chess:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        # img1 = pygame.image.load('Pieces/400x300.png')
        # self.img1_rect = pygame.transform.smoothscale(img1, (800, 600))
        # img2 = pygame.image.load('Pieces/533x400.jpg')
        # self.img2_rect = pygame.transform.smoothscale(img2, (800, 600))
        # img3 = pygame.image.load('Pieces/667x500.png')
        # self.img3_rect = pygame.transform.smoothscale(img3, (800, 600))
        # img4 = pygame.image.load('Pieces/1200x900.png')
        # self.img4_rect = pygame.transform.smoothscale(img4, (800, 600))
        # img5 = pygame.image.load('Pieces/5.jpg')
        # self.img5_rect = pygame.transform.smoothscale(img5, (800, 600))
        pygame.display.set_caption("Chess")
        self.bg_color = (255, 255, 255)
        self.board_color = (236, 218, 185)
        self.board_color_2 = (174, 138, 104)
        # self.board_color = (255, 255, 255)
        # self.board_color_2 = (128,128,128)
        self.board = Board(self)
        self.legal_moves = []
        self.legal_captures = []
        self.selected_piece = None
        self.white_move = True
        self.captured_piece = CapturedPieces(self)

    def run_game(self):
        # pygame.font.init()
        # font = pygame.font.Font(None, 32)
        # text_surface = font.render("White to Move", True, (0, 0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        if not self.board.move_log:
                            break
                        move = self.board.move_log[-1]
                        if move.captured_piece is not None:
                            self.captured_piece.undo_captured_piece(move.captured_piece)
                        UndoMove(self.board).undo()
                        self.selected_piece = None
                        self.legal_moves = []
                        self.white_move = not self.white_move
                    elif event.key == pygame.K_r:
                        self.board.undone_moves.redo_move(self.board)
                        self.selected_piece = None
                        self.legal_moves = []
                        self.white_move = not self.white_move
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row = (y - BOARD_OFFSET_Y) // SQUARE_SIZE
                    col = (x - BOARD_OFFSET_X) // SQUARE_SIZE
                    if 0 <= row < 8 and 0 <= col < 8:
                        if self.selected_piece and (row, col) in self.legal_moves:
                            if self.white_move and self.selected_piece.color == 'black':
                                self.selected_piece = None
                                break
                            elif not self.white_move and self.selected_piece.color == 'white':
                                self.selected_piece = None
                                break
                            self.board.move_piece(self.selected_piece, (row, col))#, self.legal_captures)
                            self.selected_piece.position = (row, col)
                            self.white_move = not self.white_move
                            # king_color = 'white' if self.selected_piece.color == 'black' else 'black'
                            # king_location = self.board.get_king_position(king_color)
                            # if CheckConditions(self.board, self.board[king_location[0]][king_location[1]]).checkmate() is None:
                            #     if self.white_move:
                            #         text = 'White to move'
                            #         text_surface = font.render(text, True, (0, 0, 0))
                            #     else:
                            #         text = 'Black to move'
                            #         text_surface = font.render(text, True, (0, 0, 0))
                            # elif CheckConditions(self.board, self.board[king_location[0]][king_location[1]]).checkmate() == 'checkmate':
                            #     text = 'checkmate'
                            #     text_surface = font.render(text, True, (0, 0, 0))
                            # else:
                            #     text = 'stalemate'
                            #     text_surface = font.render(text, True, (0, 0, 0))
                            self.captured_piece.capture_piece(self.board.get_log()[-1])
                            self.selected_piece = None
                            self.legal_moves = []
                            self.legal_captures = []
                            self.board.undone_moves.reset_moves()
                        else:
                            self.selected_piece = None
                            self.select_piece(row, col)
            self.screen.fill(self.bg_color)
            # self.screen.blit(self.img2_rect, (0,0))
            # self.screen.fill(self.img2_rect)
            # self.screen.fill(self.img3_rect)
            # self.screen.fill(self.img4_rect)
            pygame.draw.rect(self.screen, self.board_color, pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_OFFSET_X, BOARD_OFFSET_X))
            position1 = BOARD_OFFSET_X
            position2 = BOARD_OFFSET_Y

            for i in range(8):
                for j in range(8):
                    # temp_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    if j % 2 == 0:
                        # temp_surface.fill((*self.board_color, 150))
                        # self.screen.blit(temp_surface, (position1, position2))
                        pygame.draw.rect(self.screen, self.board_color, pygame.Rect(position1, position2, SQUARE_SIZE, SQUARE_SIZE))
                    else:
                        # temp_surface.fill((*self.board_color_2, 150))
                        # self.screen.blit(temp_surface, (position1, position2))
                        pygame.draw.rect(self.screen, self.board_color_2, pygame.Rect(position1, position2, SQUARE_SIZE, SQUARE_SIZE))
                    position1 += SQUARE_SIZE
                position1 = BOARD_OFFSET_X
                position2 += SQUARE_SIZE
                temp_color = self.board_color
                self.board_color = self.board_color_2
                self.board_color_2 = temp_color
            position1 = BOARD_OFFSET_X
            position2 = BOARD_OFFSET_Y

            for i in range(8):
                for j in range(8):
                    if self.board[i][j] is not None:
                        piece = self.board[i][j]
                        piece_position = (position1 + SQUARE_SIZE // 2 - piece.img.get_width() // 2, position2 + SQUARE_SIZE // 2 - piece.img.get_height() // 2)
                        self.screen.blit(piece.img, piece_position)
                    position1 += SQUARE_SIZE
                position1 = BOARD_OFFSET_X
                position2 += SQUARE_SIZE

            for move in self.legal_moves:
                if self.selected_piece is not None and self.selected_piece.piece_type == 'pawn':
                    if self.board[move[0]][move[1]] is None and move[1] != self.selected_piece.position[1]:
                        row = move[0] + 1 if self.selected_piece.color == 'white' else move[0] - 1
                        position1 = BOARD_OFFSET_X + move[1] * SQUARE_SIZE
                        position2 = BOARD_OFFSET_Y + (row) * SQUARE_SIZE
                        piece_position = (position1 + SQUARE_SIZE // 2 - self.selected_piece.img.get_width() // 2,
                                          position2 + SQUARE_SIZE // 2 - self.selected_piece.img.get_height() // 2)
                        self.screen.blit(pygame.image.load("Pieces/glow.png"), piece_position)
                        self.screen.blit(self.board[row][move[1]].img, piece_position)
                if self.selected_piece is not None and self.board[move[0]][move[1]] is None:
                    if (self.white_move and self.selected_piece.color == 'white') or (not self.white_move and self.selected_piece.color == 'black'):
                        pygame.draw.circle(self.screen, (192, 192, 192), (move[1] * SQUARE_SIZE + BOARD_OFFSET_X + 25, move[0] * SQUARE_SIZE + BOARD_OFFSET_Y + 25), 10)
                elif self.board[move[0]][move[1]] is not None and self.selected_piece is not None and self.board[move[0]][move[1]].color != self.selected_piece.color:
                    if (self.white_move and self.selected_piece.color == 'white') or (not self.white_move and self.selected_piece.color == 'black'):
                        position1 = BOARD_OFFSET_X
                        position2 = BOARD_OFFSET_Y
                        for i in range(8):
                            for j in range(8):
                                if (i, j) == move:
                                    piece = self.board[i][j]
                                    piece_position = (position1 + SQUARE_SIZE // 2 - piece.img.get_width() // 2, position2 + SQUARE_SIZE // 2 - piece.img.get_height() // 2)
                                    self.screen.blit(pygame.image.load("Pieces/glow.png"), piece_position)
                                    self.screen.blit(piece.img, piece_position)
                                position1 += SQUARE_SIZE
                            position1 = BOARD_OFFSET_X
                            position2 += SQUARE_SIZE

            # self.screen.blit(text_surface, (250, 550))
            # if self.board.get_log():
            #     self.captured_piece.capture_piece(self.board.get_log()[-1])
            self.captured_piece.display_white_captured_spots()
            self.captured_piece.display_black_captured_spots()
            pygame.display.flip()

    def select_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece is not None:
            if (self.white_move and piece.color == 'white') or (not self.white_move and piece.color == 'black'):
                self.selected_piece = piece
                piece.set_legal_moves(self.board)
                self.legal_moves = self.selected_piece.validate_legal_moves(self.board)
                self.legal_captures = self.selected_piece.get_legal_captures(self.board)
        else:
            if self.selected_piece is None:
                self.legal_moves = []
                self.legal_captures = []

    def get_board(self):
        return self.board


if __name__ == '__main__':
    ai = Chess()
    ai.run_game()
