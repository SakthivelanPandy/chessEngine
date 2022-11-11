class Board:
    def __init__(self):
        w_charset = {'k':'\u2654',                                              # Unicode charsets so that the board can be printed in the terminal with cool characters
                     'q':'\u2655',
                     'r':'\u2656',
                     'b':'\u2657',
                     'n':'\u2658',
                     'p':'\u2659'}
        b_charset = {'k':'\u265a',
                     'q':'\u265b',
                     'r':'\u265c',
                     'b':'\u265d',
                     'n':'\u265e',
                     'p':'\u265f'}
        
        pieceArrangement = ["r","n","b","q","k","b","n","r"]
        pawns = ["p" for p in range(8)]
        blank = ["." for i in range(8)]
        self.board_state = []
        self.board_state.append([b_charset[piece] for piece in pieceArrangement])
        self.board_state.append([b_charset[pawn] for pawn in pawns])
        for i in range(4):
            self.board_state.append(blank)
        self.board_state.append([w_charset[pawn] for pawn in pawns])                #Set before the piece arrangement so that the pawns are in the correct order
        self.board_state.append([w_charset[piece] for piece in pieceArrangement])
        
		
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