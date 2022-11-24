from Board import *



def main():
  game_board = Board()
  print(game_board.get_space("a1"))
  print(game_board.create_board_string())

  k = king("w",game_board,"d3")
  print(k.gen_mov())


if __name__ == '__main__':
  main()