
# Full working pins and check logic that removes any moves from valid moves that either put king in check, or dont protect king in check.
class CheckConditions:
    def __init__(self, board, piece, move=None):
        self.piece = piece
        self.move = move
        self.board = board
        self.king_position = self.board.get_king_position(self.piece.color)

    def validate_move(self):
        self.board.move_piece(self.piece, self.move, test=True)#, self.piece.get_legal_captures(self.board), test=True)
        self.king_position = self.board.get_king_position(self.piece.color)
        return self.king_in_check()

    def king_in_check(self):
        moves = self.get_opponent_moves()
        if self.king_position in moves:
            return True
        return False

    def get_opponent_moves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] is not None and self.board[row][col].piece_type != 'king' and self.board[row][col].color != self.piece.color:
                    moves.extend(self.board[row][col].get_legal_moves(self.board))
        return moves

    def king_in_check_castle(self, king_path):
        moves = self.get_opponent_moves()
        for path in king_path:
            if path in moves or self.king_position in moves:
                return True
        return False

    def get_player_moves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] is not None and self.board[row][col].color == self.piece.color:
                    self.board[row][col].get_legal_moves(self.board)
                    moves.extend(self.board[row][col].validate_legal_moves(self.board))
        return moves

    def checkmate(self):
        if not self.get_player_moves() and self.king_in_check():
            return 'checkmate'
        elif not self.get_player_moves() and not self.king_in_check():
            return 'stalemate'
        return


# look into logic about what causes a draw in chess
#
# According to the rules of chess, a game can end in a draw under several conditions:
#
# Insufficient material: This happens when neither player has enough pieces to be able to checkmate the other. For example,
# if only two kings remain, neither player can force a checkmate, so the game is a draw.
#
    def count_pieces(self):
        white_count = 0
        black_count = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col] is not None:
                    if self.board[row][col].color == 'white':
                        white_count += 1
                    else:
                        black_count += 1
        if black_count == white_count and black_count == 1:
            return True
        return False

# Threefold repetition: This rule states that the game is a draw if the same position occurs three times, not necessarily consecutively,
# with the same player to move each time. The positions don't need to be repeated sequentially, and they can span multiple turns.
#
# Fifty-move rule: If during the last 50 consecutive moves by each player, no pawn has moved and there has been no capture, a player can
# claim a draw.
#
# Mutual agreement: Both players may simply agree to a draw, ending the game.
#
# Fivefold repetition or Seventy-five-move rule: Similar to threefold repetition and fifty-move rule but respectively need positions
# repeated five times or happening 75 turns without capture or pawn moves. These rules automatically end the game in a draw without requiring
# a claim by a player.
#
# Implementing all these rules into a computer program can be a challenge, especially correctly tracking the three/fivefold
# repetition and the fifty/seventy-five-move rule, but it's absolutely possible! You'll need a way to keep track of the entire game
# state after each move, including the positions of all pieces and whose turn it is, so you can detect repeated positions and moves
# without a pawn moving or a piece being captured.


# # fix move log logic
