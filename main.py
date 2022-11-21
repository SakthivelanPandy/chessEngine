from Board import Board, pieces, pawn



def main():
  game_board = Board()
  print(game_board.get_space("a1"))
  print(game_board.create_board_string())

  p = pawn("w",game_board,"a7")
  print(p.gen_mov())


if __name__ == '__main__':
  main()