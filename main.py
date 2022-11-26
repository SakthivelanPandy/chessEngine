from Board import *
import random, os



def main():
  game_board = Board()
  print(game_board.create_board_string())
  for i in range(50):
    print(game_board.check_for_check())
    move = input("Enter a move: ")
    game_board.move_piece(move)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(game_board.create_board_string(flipped=(i+1)%2))

  


if __name__ == '__main__':
  main()