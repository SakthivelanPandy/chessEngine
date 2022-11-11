from Board import Board
import re

def validate_format(user_input):
    lan = r"([KQNBR]?)([a-g][1-9])([x]?)([a-g][1-9])([KQNBR]?)"
    if re.search(lan, user_input):
       return re.split(lan, user_input)[1:-1]

def main():
  game_board = Board()
  print(game_board.create_board_string())
  print(validate_format("Bb4xc5"))


if __name__ == '__main__':
  main()