from Board import *
import random, os



def main():
  game_board = Board()
  print(game_board.create_board_string())
  for i in range(50):
    r = random.choice(game_board.return_moves())
    game_board.move_piece(r)
    print(game_board.create_board_string())
    input()
    os.system('cls' if os.name == 'nt' else 'clear')

  


if __name__ == '__main__':
  main()