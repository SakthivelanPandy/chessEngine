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
        
        self.w_charset = w_charset #needed to do this for code later on
        self.b_charset = b_charset

        self.turn = True # True = white, False = black
        
        pieceArrangement = ["r","n","b","q","k","b","n","r"]
        pawns = ["p" for p in range(8)]
        blank = ["." for i in range(8)]
        self.board_state = [[] for i in range(8)]
        self.board_state[0] = [b_charset[piece] for piece in pieceArrangement]
        self.board_state[1] = [b_charset[pawn] for pawn in pawns]
        for i in range(4):
            self.board_state[i+2] = [".",".",".",".",".",".",".","."]
        self.board_state[6] = [w_charset[pawn] for pawn in pawns]            #Set before the piece arrangement so that the pawns are in the correct order
        self.board_state[7] = [w_charset[piece] for piece in pieceArrangement]

        wp1 = pawn("w",self,"a2")
        wp2 = pawn("w",self,"b2")
        wp3 = pawn("w",self,"c2")
        wp4 = pawn("w",self,"d2")
        wp5 = pawn("w",self,"e2")
        wp6 = pawn("w",self,"f2")
        wp7 = pawn("w",self,"g2")
        wp8 = pawn("w",self,"h2")
        wr1 = rook("w",self,"a1")
        wr2 = rook("w",self,"h1")
        wn1 = knight("w",self,"b1")
        wn2 = knight("w",self,"g1")
        wb1 = bishop("w",self,"c1")
        wb2 = bishop("w",self,"f1")
        wq = queen("w",self,"d1")
        wk = king("w",self,"e1")

        bp1 = pawn("b",self,"a7")
        bp2 = pawn("b",self,"b7")
        bp3 = pawn("b",self,"c7")
        bp4 = pawn("b",self,"d7")
        bp5 = pawn("b",self,"e7")
        bp6 = pawn("b",self,"f7")
        bp7 = pawn("b",self,"g7")
        bp8 = pawn("b",self,"h7")
        br1 = rook("b",self,"a8")
        br2 = rook("b",self,"h8")
        bn1 = knight("b",self,"b8")
        bn2 = knight("b",self,"g8")
        bb1 = bishop("b",self,"c8")
        bb2 = bishop("b",self,"f8")
        bq = queen("b",self,"d8")
        bk = king("b",self,"e8")

        self.w_team = [wp1,wp2,wp3,wp4,wp5,wp6,wp7,wp8,wr1,wr2,wn1,wn2,wb1,wb2,wq,wk]
        self.b_team = [bp1,bp2,bp3,bp4,bp5,bp6,bp7,bp8,br1,br2,bn1,bn2,bb1,bb2,bq,bk]

        
        
		
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
    
    def return_moves(self):
        if self.turn:
            return sum([piece.gen_mov() for piece in self.w_team],[])
        return sum([piece.gen_mov() for piece in self.b_team],[])
    
    def validate_move(self,move):
        if move in self.return_moves():
            return True
        return False
    
    def move_piece(self,move):
        if self.validate_move(move):
            start,capture,end,promotion = re.split(r"([a-g][1-9])([x]?)([a-g][1-9])([KQNBR]?)",move)[1:-1]
            if self.turn:
                for piece in self.w_team:
                    if piece.pos == start:
                        piece_to_move = piece
                piece_to_move.pos = end
                alphabet = "abcdefgh"
                self.board_state[2][alphabet.index(end[0])] = piece_to_move.char
                self.board_state[int(start[1])-1][alphabet.index(start[0])] = "."
                print(int(end[1])-1,alphabet.index(end[0]))
                

                if capture:
                    for piece in self.b_team:
                        if piece.pos == end:
                            self.b_team.remove(piece)
                            break
                if promotion:
                    self.w_team.remove(piece)
                    if promotion == "Q":
                        self.w_team.append(queen("w",self,end))
                    elif promotion == "R":
                        self.w_team.append(rook("w",self,end))
                    elif promotion == "B":
                        self.w_team.append(bishop("w",self,end))
                    elif promotion == "N":
                        self.w_team.append(knight("w",self,end))
                    else:
                        self.w_team.append(queen("w",self,end))
                
            self.turn = not self.turn
            return True
        return False

    def get_space(self,string):
        let,num = string[0],string[1]
        alphabet = "abcdefgh"
        return self.board_state[int(num)-1][alphabet.index(let)] #returns the piece at the given space, pretty self explanatory



class pieces:
    def __init__(self,colour,board,pos):
        self.colour = colour
        self.board = board
        self.pos = pos
        self.taken = False
        self.b_chars = ["♖", "♘", "♗", "♕", "♔", "♙" ] #this is needed because of the stupid way i wrote the move generation
        self.w_chars = ["♜", "♞", "♝", "♛", "♚", "♟" ]

    def __str__(self):
        return self.char

    def check_in_bounds(self,move):
        if len(move) == 2 and move[0] in "abcdefgh" and move[1] in "12345678":
            return True
        else:
            return False
        
    def check_if_unobstructed(self,start,end):
        alphabet = "abcdefgh"
        if start[0] == end[0]:#if on the same row
            for i in range(int(start[1])+1,int(end[1])):
                if self.board.get_space(start[0]+str(i)) != ".":
                    return False
        elif start[1] == end[1]:#if on the same column
            for i in range(alphabet.index(start[0])+1,alphabet.index(end[0])):
                if self.board.get_space(i+start[1]) != ".":
                    return False
        else:#if moving diagonally
            start = alphabet[alphabet.index(start[0])+1]+str(int(start[1])+1)
            while start != end:
                if self.board.get_space(start) != ".":
                    return False
                start = alphabet[alphabet.index(start[0])+1]+str(int(start[1])+1)
        return True

class pawn(pieces):
    def __init__(self,colour,board,pos):
        super().__init__(colour,board,pos)
        self.char = "\u2659" if colour == "b" else "\u265f"

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
    def __init__(self, colour, board, pos):
        super().__init__(colour,board, pos)
        self.char = "\u2656" if self.colour == "b" else "\u265C"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = []
        for i in range(1,8):#moving right
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
        for i in range(1,8):#moving left
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
        for i in range(1,8):#moving up
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
        for i in range(1,8):#moving down
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
    def __init__(self, colour, board, pos):
        super().__init__(colour,board,pos)
        self.char = "\u2657" if self.colour == "b" else "\u265D"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = []
        for i in range(1,8): #you can gather how this works
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
    def __init__(self, colour,board,pos):
        super().__init__(colour, board,pos)
        self.char = "\u2655" if self.colour == "b" else "\u265B"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = []
        for i in range(1,8): #you can gather how this works
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
    def __init__(self,colour,board,pos):
        super().__init__(colour,board,pos)
        self.char = "\u2658" if self.colour == "b" else "\u265E"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = []#once again, you should be able to gather how this works. there was probably a much wasier way of doing all this, but this is what ive got for you.
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
    def __init__(self,colour,board,pos):
        super().__init__(colour,board,pos)
        self.char = "\u2654" if self.colour == "b" else "\u265A"
        self.op_team = self.b_chars if self.colour == "w" else self.w_chars

    def gen_mov(self):
        moves = [] #for now, the king can move into check. what i plan on doing is chekcing if the king is in check  after any move, and if it is, then the move is not valid. this way,we will only have to check for check once, and not anywhere else.
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
