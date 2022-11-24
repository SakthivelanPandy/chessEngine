from Board import *



def main():
  game_board = Board()
  print(game_board.create_board_string())
  game_board.move_piece("Nb1c3")
  print(game_board.create_board_string())
  print([i.pos for i in game_board.w_team])


if __name__ == '__main__':
  main()