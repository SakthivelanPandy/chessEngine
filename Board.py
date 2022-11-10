class Board:
    def __init__(self):
        pieces = ["r","n","b","q","k","b","n","r"]
        pawns = ["p" for p in range(8)]
        blank = ["." for i in range(8)]
        self.board_state = []
        self.board_state.append(pieces)
        self.board_state.append(pawns)
        for i in range(4):
            self.board_state.append(blank)
        self.board_state.append([pawn.upper() for pawn in pawns])
        self.board_state.append([piece.upper() for piece in pieces])
		
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