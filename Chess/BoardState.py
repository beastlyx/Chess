class BoardState:
	def __init__(self):
		self.move_log = []
	
	def add_move(self, move):
		self.move_log.insert(0, move)

	def get_undone_moves(self):
		return self
		
	def redo_move(self, board):
		if not self.move_log:
			return
		redo = self.move_log.pop(0)
		board.move_piece(redo.piece, redo.new_pos)#, redo.piece.get_legal_captures(board))
		# if redo.captured_piece is not None:
		# 	board[redo.new_pos[0]][redo.new_pos[1]] = redo.captured_piece

		
	def reset_moves(self):
		self.move_log = []
# figure out a way to save the state of the board via the move log function, so for each move undone, it can be re-undone here
