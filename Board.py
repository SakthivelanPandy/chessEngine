import re

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
        
        self.w_charset = w_charset
        self.b_charset = b_charset
        
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
        if not flipped:
            for row_index in range(len(self.board_state)):
                for piece_index in range(len(self.board_state[row_index])):
                    output = output + self.board_state[7-row_index][piece_index] + " "
                output += "\n"
            #output = output[::-1]
            return output
        for row_index in range(len(self.board_state)):
            for piece_index in range(len(self.board_state[row_index])):
                output = output + self.board_state[row_index][piece_index] + " "
            output += "\n"
        return output
		
    def get_board_string(self, flipped=False):
        return self.create_board_string(flipped)
    
    def validate_format(self,user_input):
         lan = r"([KQNBR]?)([a-g][1-9])([x]?)([a-g][1-9])([KQNBR]?)" #checks for valid long algebraic notation
         if re.search(lan, user_input):
              return re.split(lan, user_input)[1:-1] #returns components of move: piece, start, capture, end, promotion
         
    def validate_move(self, user_input,turn):
         user_input_formatted = self.validate_format(user_input)
         if not user_input_formatted:
             return False
         
         char_set = self.w_charset if turn == "w" else self.b_charset
	
         piece = user_input_formatted[0].lower() or "p" #if no piece is specified, assume pawn
         start = user_input_formatted[1]
         capture = bool(user_input_formatted[2])
         end = user_input_formatted[3]
         promotion = user_input_formatted[4]

         if self.get_space(start) == char_set[piece]:
                return True #haven't finished this function yet

    def get_space(self,string):
        let,num = string[0],string[1]
        alphabet = "abcdefgh"
        return self.board_state[int(num)-1][alphabet.index(let)]



class pieces:
    def __init__(self,colour,board,pos):
        self.colour = colour
        self.board = board
        self.pos = pos
        self.taken = False
        self.b_chars = ["♖", "♘", "♗", "♕", "♔", "♙" ]
        self.w_chars = ["♜", "♞", "♝", "♛", "♚", "♟" ]

    def check_in_bounds(self,move):
        if move[0] in "abcdefgh" and move[1] in "12345678":
            return True
        else:
            return False
        
    def check_if_unobstructed(self,start,end):
        alphabet = "abcdefgh"
        if start[0] == end[0]:
            for i in range(int(start[1])+1,int(end[1])):
                if self.board.get_space(start[0]+str(i)) != ".":
                    return False
        elif start[1] == end[1]:
            for i in range(alphabet.index(start[0])+1,alphabet.index(end[0])):
                if self.board.get_space(i+start[1]) != ".":
                    return False
        else:
            start = alphabet[alphabet.index(start[0])+1]+str(int(start[1])+1)
            while start != end:
                if self.board.get_space(start) != ".":
                    return False
                start = alphabet[alphabet.index(start[0])+1]+str(int(start[1])+1)
        return True

class pawn(pieces):
    def __init__(self,colour,board,pos):
        super().__init__(colour,board,pos)
        self.char = "\u2659" if colour == "w" else "\u265f"

    def gen_mov(self): #brace yourself for this. i wrote this myself, which is why its so messy. if you can tidy this up, please do. even i dont want to look at it.
        moves = []
        if self.colour == "w":
            if self.pos[1] == "2":
                #if on starting row, can move 2 spaces, if unobstructed
                moves.append(self.pos+self.pos[0]+"3") if self.board.get_space(self.pos[0]+"3") == "." else None
                moves.append(self.pos+self.pos[0]+"4") if self.board.get_space(self.pos[0]+"4") == "."  and self.board.get_space(self.pos[0]+"3") == "." else None
            else:
                if self.board.get_space(self.pos[0]+str(int(self.pos[1])+1)) == ".":
                    #if the space in front is empty, can move there
                    if self.pos[1] == "7":
                         for i in ["Q","R","B","N"]:
                             moves.append(self.pos + self.pos[0]+str(int(self.pos[1])+1)) #if on the last row, can promote to any peice
                    else:
                        moves.append(self.pos + self.pos[0]+str(int(self.pos[1])+1))
            if self.check_in_bounds(chr(ord(self.pos[0])+1)+str(int(self.pos[1])+1)):
                if self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])+1)) in self.b_chars : #capture right
                    if self.pos[1] == "7":
                            for i in ["Q","R","B","N"]:
                                moves.append(self.pos + "x" + chr(ord(self.pos[0])+1)+str(int(self.pos[1])+1) + i) #can promote to any piece
                    else:
                        moves.append(self.pos + "x" + chr(ord(self.pos[0])+1)+str(int(self.pos[1])+1))
            if self.check_in_bounds(chr(ord(self.pos[0])-1)+str(int(self.pos[1])+1)):
                if self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])+1)) in self.b_chars: #capture left
                    if self.pos[1] == "7":
                            for i in ["Q","R","B","N"]:
                                moves.append(self.pos + "x" + chr(ord(self.pos[0])-1)+str(int(self.pos[1])+1) + i) #can promote to any peice
                    else:
                        moves.append(self.pos + "x" + chr(ord(self.pos[0])-1)+str(int(self.pos[1])+1))
        else: #same, but for black
            if self.pos[1] == "7":
                moves.append(self.pos+self.pos[0]+"6") if self.board.get_space(self.pos[0]+"6") == "." else None
                moves.append(self.pos+self.pos[0]+"5") if self.board.get_space(self.pos[0]+"5") == "."  and self.board.get_space(self.pos[0]+"6") == "." else None
            else:
                if self.board.get_space(self.pos[0]+str(int(self.pos[1])-1)) == ".": #if the space in front is empty, can move there
                    if self.pos[1] == "2":
                         for i in ["Q","R","B","N"]:
                             moves.append(self.pos + self.pos[0]+str(int(self.pos[1])-1))
                    else:
                        moves.append(self.pos + self.pos[0]+str(int(self.pos[1])-1))
            if self.check_in_bounds(chr(ord(self.pos[0])+1)+str(int(self.pos[1])-1)):
                if self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])-1)) in self.w_chars: #capture right
                    if self.pos[1] == "2":
                            for i in ["Q","R","B","N"]:
                                moves.append(self.pos + "x" + chr(ord(self.pos[0])+1)+str(int(self.pos[1])-1) + i)
                    else:
                        moves.append(self.pos + "x" + chr(ord(self.pos[0])+1)+str(int(self.pos[1])-1))
            if self.check_in_bounds(chr(ord(self.pos[0])-1)+str(int(self.pos[1])-1)):
                if self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])-1)) in self.w_chars: #capture left
                    if self.pos[1] == "2":
                            for i in ["Q","R","B","N"]:
                                moves.append(self.pos + "x" + chr(ord(self.pos[0])-1)+str(int(self.pos[1])-1) + i)
                    else:
                        moves.append(self.pos + "x" + chr(ord(self.pos[0])-1)+str(int(self.pos[1])-1))
        return moves
        #what this is meant to do is generate all the possible moves for a peice, in LAN format. This means we need to keep track of all the peices on the board as objects.7
    #have fun deciphering this mess, Alan. I've commnented it just like you wanted me to. doing this for the other peices will be a lot easier, as they they are not different for black and white, and cannot promote. the king and checks will be a mess to code though.

class rook(pieces):
    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.char = "\u2656" if self.colour == "w" else "\u265C"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = []
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])+i)+self.pos[1]):
                if self.board.get_space(chr(ord(self.pos[0])+i)+self.pos[1]) == ".":
                    moves.append("R" + self.pos + chr(ord(self.pos[0])+i)+self.pos[1])
                elif self.board.get_space(chr(ord(self.pos[0])+i)+self.pos[1]) in self.op_team:
                    moves.append("R" + self.pos + "x" + chr(ord(self.pos[0])+i)+self.pos[1])
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])-i)+self.pos[1]):
                if self.board.get_space(chr(ord(self.pos[0])-i)+self.pos[1]) == ".":
                    moves.append("R" + self.pos + chr(ord(self.pos[0])-i)+self.pos[1])
                elif self.board.get_space(chr(ord(self.pos[0])-i)+self.pos[1]) in self.op_team:
                    moves.append("R" + self.pos + "x" + chr(ord(self.pos[0])-i)+self.pos[1])
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(self.pos[0]+str(int(self.pos[1])+i)):
                if self.board.get_space(self.pos[0]+str(int(self.pos[1])+i)) == ".":
                    moves.append("R" + self.pos + self.pos[0]+str(int(self.pos[1])+i))
                elif self.board.get_space(self.pos[0]+str(int(self.pos[1])+i)) in self.op_team:
                    moves.append("R" + self.pos + "x" + self.pos[0]+str(int(self.pos[1])+i))
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(self.pos[0]+str(int(self.pos[1])-i)):
                if self.board.get_space(self.pos[0]+str(int(self.pos[1])-i)) == ".":
                    moves.append("R" + self.pos + self.pos[0]+str(int(self.pos[1])-i))
                elif self.board.get_space(self.pos[0]+str(int(self.pos[1])-i)) in self.op_team:
                    moves.append("R" + self.pos + "x" + self.pos[0]+str(int(self.pos[1])-i))
                    break
                else:
                    break
            else:
                break
        return moves
    
class bishop(pieces):
    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.char = "\u2657" if self.colour == "w" else "\u265D"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = []
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i)):
                if self.board.get_space(chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i)) == ".":
                    moves.append("B" + self.pos + chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i))
                elif self.board.get_space(chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i)) in self.op_team:
                    moves.append("B" + self.pos + "x" + chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i))
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i)):
                if self.board.get_space(chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i)) == ".":
                    moves.append("B" + self.pos + chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i))
                elif self.board.get_space(chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i)) in self.op_team:
                    moves.append("B" + self.pos + "x" + chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i))
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i)):
                if self.board.get_space(chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i)) == ".":
                    moves.append("B" + self.pos + chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i))
                elif self.board.get_space(chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i)) in self.op_team:
                    moves.append("B" + self.pos + "x" + chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i))
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i)):
                if self.board.get_space(chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i)) == ".":
                    moves.append("B" + self.pos + chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i))
                elif self.board.get_space(chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i)) in self.op_team:
                    moves.append("B" + self.pos + "x" + chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i))
                    break
                else:
                    break
            else:
                break
        return moves
    
class queen(pieces):
    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.char = "\u2655" if self.colour == "w" else "\u265B"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = []
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i)):
                if self.board.get_space(chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i)) == ".":
                    moves.append("Q" + self.pos + chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i))
                elif self.board.get_space(chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i)) in self.op_team:
                    moves.append("Q" + self.pos + "x" + chr(ord(self.pos[0])+i)+str(int(self.pos[1])+i))
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i)):
                if self.board.get_space(chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i)) == ".":
                    moves.append("Q" + self.pos + chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i))
                elif self.board.get_space(chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i)) in self.op_team:
                    moves.append("Q" + self.pos + "x" + chr(ord(self.pos[0])-i)+str(int(self.pos[1])-i))
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i)):
                if self.board.get_space(chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i)) == ".":
                    moves.append("Q" + self.pos + chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i))
                elif self.board.get_space(chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i)) in self.op_team:
                    moves.append("Q" + self.pos + "x" + chr(ord(self.pos[0])+i)+str(int(self.pos[1])-i))
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i)):
                if self.board.get_space(chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i)) == ".":
                    moves.append("Q" + self.pos + chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i))
                elif self.board.get_space(chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i)) in self.op_team:
                    moves.append("Q" + self.pos + "x" + chr(ord(self.pos[0])-i)+str(int(self.pos[1])+i))
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])+i)+self.pos[1]):
                if self.board.get_space(chr(ord(self.pos[0])+i)+self.pos[1]) == ".":
                    moves.append("Q" + self.pos + chr(ord(self.pos[0])+i)+self.pos[1])
                elif self.board.get_space(chr(ord(self.pos[0])+i)+self.pos[1]) in self.op_team:
                    moves.append("Q" + self.pos + "x" + chr(ord(self.pos[0])+i)+self.pos[1])
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(chr(ord(self.pos[0])-i)+self.pos[1]):
                if self.board.get_space(chr(ord(self.pos[0])-i)+self.pos[1]) == ".":
                    moves.append("Q" + self.pos + chr(ord(self.pos[0])-i)+self.pos[1])
                elif self.board.get_space(chr(ord(self.pos[0])-i)+self.pos[1]) in self.op_team:
                    moves.append("Q" + self.pos + "x" + chr(ord(self.pos[0])-i)+self.pos[1])
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(self.pos[0]+str(int(self.pos[1])+i)):
                if self.board.get_space(self.pos[0]+str(int(self.pos[1])+i)) == ".":
                    moves.append("Q" + self.pos + self.pos[0]+str(int(self.pos[1])+i))
                elif self.board.get_space(self.pos[0]+str(int(self.pos[1])+i)) in self.op_team:
                    moves.append("Q" + self.pos + "x" + self.pos[0]+str(int(self.pos[1])+i))
                    break
                else:
                    break
            else:
                break
        for i in range(1,8):
            if self.check_in_bounds(self.pos[0]+str(int(self.pos[1])-i)):
                if self.board.get_space(self.pos[0]+str(int(self.pos[1])-i)) == ".":
                    moves.append("Q" + self.pos + self.pos[0]+str(int(self.pos[1])-i))
                elif self.board.get_space(self.pos[0]+str(int(self.pos[1])-i)) in self.op_team:
                    moves.append("Q" + self.pos + "x" + self.pos[0]+str(int(self.pos[1])-i))
                    break
                else:
                    break
            else:
                break
        return moves
    
class knight(pieces):
    def __init__(self,colour,pos,board):
        super().__init__(colour,pos,board)
        self.char = "\u2658" if self.colour == "w" else "\u265E"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = []
        if self.check_in_bounds(chr(ord(self.pos[0])+1)+str(int(self.pos[1])+2)):
            if self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])+2)) == ".":
                moves.append("N" + self.pos + chr(ord(self.pos[0])+1)+str(int(self.pos[1])+2))
            elif self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])+2)) in self.op_team:
                moves.append("N" + self.pos + "x" + chr(ord(self.pos[0])+1)+str(int(self.pos[1])+2))
        if self.check_in_bounds(chr(ord(self.pos[0])+1)+str(int(self.pos[1])-2)):
            if self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])-2)) == ".":
                moves.append("N" + self.pos + chr(ord(self.pos[0])+1)+str(int(self.pos[1])-2))
            elif self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])-2)) in self.op_team:
                moves.append("N" + self.pos + "x" + chr(ord(self.pos[0])+1)+str(int(self.pos[1])-2))
        if self.check_in_bounds(chr(ord(self.pos[0])-1)+str(int(self.pos[1])+2)):
            if self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])+2)) == ".":
                moves.append("N" + self.pos + chr(ord(self.pos[0])-1)+str(int(self.pos[1])+2))
            elif self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])+2)) in self.op_team:
                moves.append("N" + self.pos + "x" + chr(ord(self.pos[0])-1)+str(int(self.pos[1])+2))
        if self.check_in_bounds(chr(ord(self.pos[0])-1)+str(int(self.pos[1])-2)):
            if self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])-2)) == ".":
                moves.append("N" + self.pos + chr(ord(self.pos[0])-1)+str(int(self.pos[1])-2))
            elif self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])-2)) in self.op_team:
                moves.append("N" + self.pos + "x" + chr(ord(self.pos[0])-1)+str(int(self.pos[1])-2))
        if self.check_in_bounds(chr(ord(self.pos[0])+2)+str(int(self.pos[1])+1)):
            if self.board.get_space(chr(ord(self.pos[0])+2)+str(int(self.pos[1])+1)) == ".":
                moves.append("N" + self.pos + chr(ord(self.pos[0])+2)+str(int(self.pos[1])+1))
            elif self.board.get_space(chr(ord(self.pos[0])+2)+str(int(self.pos[1])+1)) in self.op_team:
                moves.append("N" + self.pos + "x" + chr(ord(self.pos[0])+2)+str(int(self.pos[1])+1))
        if self.check_in_bounds(chr(ord(self.pos[0])+2)+str(int(self.pos[1])-1)):
            if self.board.get_space(chr(ord(self.pos[0])+2)+str(int(self.pos[1])-1)) == ".":
                moves.append("N" + self.pos + chr(ord(self.pos[0])+2)+str(int(self.pos[1])-1))
            elif self.board.get_space(chr(ord(self.pos[0])+2)+str(int(self.pos[1])-1)) in self.op_team:
                moves.append("N" + self.pos + "x" + chr(ord(self.pos[0])+2)+str(int(self.pos[1])-1))
        if self.check_in_bounds(chr(ord(self.pos[0])-2)+str(int(self.pos[1])+1)):
            if self.board.get_space(chr(ord(self.pos[0])-2)+str(int(self.pos[1])+1)) == ".":
                moves.append("N" + self.pos + chr(ord(self.pos[0])-2)+str(int(self.pos[1])+1))
            elif self.board.get_space(chr(ord(self.pos[0])-2)+str(int(self.pos[1])+1)) in self.op_team:
                moves.append("N" + self.pos + "x" + chr(ord(self.pos[0])-2)+str(int(self.pos[1])+1))
        if self.check_in_bounds(chr(ord(self.pos[0])-2)+str(int(self.pos[1])-1)):
            if self.board.get_space(chr(ord(self.pos[0])-2)+str(int(self.pos[1])-1)) == ".":
                moves.append("N" + self.pos + chr(ord(self.pos[0])-2)+str(int(self.pos[1])-1))
            elif self.board.get_space(chr(ord(self.pos[0])-2)+str(int(self.pos[1])-1)) in self.op_team:
                moves.append("N" + self.pos + "x" + chr(ord(self.pos[0])-2)+str(int(self.pos[1])-1))
        return moves
    
class king(pieces):
    def __init__(self,colour,pos,board):
        super().__init__(colour,pos,board)
        self.char = "\u2654" if self.colour == "w" else "\u265A"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = []
        if self.check_in_bounds(chr(ord(self.pos[0])+1)+str(int(self.pos[1]))):
            if self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1]))) == ".":
                moves.append("K" + self.pos + chr(ord(self.pos[0])+1)+str(int(self.pos[1])))
            elif self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1]))) in self.op_team:
                moves.append("K" + self.pos + "x" + chr(ord(self.pos[0])+1)+str(int(self.pos[1])))
        if self.check_in_bounds(chr(ord(self.pos[0])-1)+str(int(self.pos[1]))):
            if self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1]))) == ".":
                moves.append("K" + self.pos + chr(ord(self.pos[0])-1)+str(int(self.pos[1])))
            elif self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1]))) in self.op_team:
                moves.append("K" + self.pos + "x" + chr(ord(self.pos[0])-1)+str(int(self.pos[1])))
        if self.check_in_bounds(chr(ord(self.pos[0]))+str(int(self.pos[1])+1)):
            if self.board.get_space(chr(ord(self.pos[0]))+str(int(self.pos[1])+1)) == ".":
                moves.append("K" + self.pos + chr(ord(self.pos[0]))+str(int(self.pos[1])+1))
            elif self.board.get_space(chr(ord(self.pos[0]))+str(int(self.pos[1])+1)) in self.op_team:
                moves.append("K" + self.pos + "x" + chr(ord(self.pos[0]))+str(int(self.pos[1])+1))
        if self.check_in_bounds(chr(ord(self.pos[0]))+str(int(self.pos[1])-1)):
            if self.board.get_space(chr(ord(self.pos[0]))+str(int(self.pos[1])-1)) == ".":
                moves.append("K" + self.pos + chr(ord(self.pos[0]))+str(int(self.pos[1])-1))
            elif self.board.get_space(chr(ord(self.pos[0]))+str(int(self.pos[1])-1)) in self.op_team:
                moves.append("K" + self.pos + "x" + chr(ord(self.pos[0]))+str(int(self.pos[1])-1))
        if self.check_in_bounds(chr(ord(self.pos[0])+1)+str(int(self.pos[1])+1)):
            if self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])+1)) == ".":
                moves.append("K" + self.pos + chr(ord(self.pos[0])+1)+str(int(self.pos[1])+1))
            elif self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])+1)) in self.op_team:
                moves.append("K" + self.pos + "x" + chr(ord(self.pos[0])+1)+str(int(self.pos[1])+1))
        if self.check_in_bounds(chr(ord(self.pos[0])+1)+str(int(self.pos[1])-1)):
            if self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])-1)) == ".":
                moves.append("K" + self.pos + chr(ord(self.pos[0])+1)+str(int(self.pos[1])-1))
            elif self.board.get_space(chr(ord(self.pos[0])+1)+str(int(self.pos[1])-1)) in self.op_team:
                moves.append("K" + self.pos + "x" + chr(ord(self.pos[0])+1)+str(int(self.pos[1])-1))
        if self.check_in_bounds(chr(ord(self.pos[0])-1)+str(int(self.pos[1])+1)):
            if self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])+1)) == ".":
                moves.append("K" + self.pos + chr(ord(self.pos[0])-1)+str(int(self.pos[1])+1))
            elif self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])+1)) in self.op_team:
                moves.append("K" + self.pos + "x" + chr(ord(self.pos[0])-1)+str(int(self.pos[1])+1))
        if self.check_in_bounds(chr(ord(self.pos[0])-1)+str(int(self.pos[1])-1)):
            if self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])-1)) == ".":
                moves.append("K" + self.pos + chr(ord(self.pos[0])-1)+str(int(self.pos[1])-1))
            elif self.board.get_space(chr(ord(self.pos[0])-1)+str(int(self.pos[1])-1)) in self.op_team:
                moves.append("K" + self.pos + "x" + chr(ord(self.pos[0])-1)+str(int(self.pos[1])-1))
        return moves
