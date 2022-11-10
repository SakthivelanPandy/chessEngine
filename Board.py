class Board:
	def __init__(self):
		l1 = ["R","N","B","Q","K","B","N","R"]
		p = ["p" for p in range(8)]
		blank = ["." for i in range(8)]
		self.board_state = []
		self.board_state.append(l1)
		self.board_state.append(p)
		for i in range(4):
			self.board_state.append(blank)
		self.board_state.append(p)
		self.board_state.append(l1)
		
	def create_board_string(self, flipped=False):
		output = ''
		if flipped:
			for row_index in range(len(self.board_state)):
				for piece_index in range(len(self.board_state[row_index])):
					output = output + self.board_state[row_index][piece_index] + " "
				output += "\n"
			output = output[::-1]
			return output
		for row_index in range(len(self.board_state)):
			for piece_index in range(len(self.board_state[row_index])):
				output = output + self.board_state[row_index][piece_index] + " "
			output += "\n"
		return output
		
	def get_board_string(self, flipped=False):
		return self.create_board_string(flipped)