from Board import Board



def main():
  game_board = Board()
  print(game_board.get_space("a1"))
  print(game_board.create_board_string())


if __name__ == '__main__':
  main()