import random
import argparse

# Stone Paper Scissor
def stone_paper_scissor():
    list = ['stone', 'paper', 'scissor']
    w = 0
    l = 0
    dic = {'1': 'stone', '2': 'paper', '3': 'scissor'}
    print('WELCOME to the Game ©©')
    print('Your opponent has chosen something >>>, Choose one of the options to beat him ^•^')
    print('1 : stone')
    print('2 : paper')
    print('3 : scissor')
    while True:
        op1 = random.choice(list)
        userinpt = str(input('Choose your option: '))
        op2 = dic.get(userinpt)
        if not op2:
            print('Invalid option, please choose 1, 2, or 3.')
            continue
        if op2 == op1:
            print('Oops! It\'s a draw.')
        elif (op1 == 'scissor' and op2 == 'stone'):
            print('You won! Your opponent has chosen scissor.')
            w += 1
        elif (op1 == 'scissor' and op2 == 'paper'):
            print('You lose! Your opponent has chosen scissor.')
            l += 1
        elif (op1 == 'stone' and op2 == 'paper'):
            print('You won! Your opponent has chosen stone.')
            w += 1
        elif (op1 == 'stone' and op2 == 'scissor'):
            print('You lose! Your opponent has chosen stone.')
            l += 1
        elif (op1 == 'paper' and op2 == 'scissor'):
            print('You won! Your opponent has chosen paper.')
            w += 1
        elif (op1 == 'paper' and op2 == 'stone'):
            print('You lose! Your opponent has chosen paper.')
            l += 1
        print(f'Match won: {w}    Match lose: {l}')

# Number Guessing Game
def number_guessing_game():
    Gnumber = random.randint(1, 100)
    a = 0
    print(' # Welcome to the Number Guessing Game !!!!')
    print('I have selected a number between 1 to 100')
    data = []
    while True:
        userinp = input('Guess the number or quit(Q): ')
        if userinp == 'Q':
            print('             !!!!You cannot even complete this game !!!!')
            break
        try:
            userinp = int(userinp)
        except ValueError:
            print('Please enter a valid number or Q to quit.')
            continue
        a += 1
        data.append(userinp)
        if userinp == Gnumber:
            print(f'::::::::Hurray!! You have guessed the correct number ::::::::::: Attempts: {a}')
            print(f'Your entries are {data}')
            break
        elif userinp > Gnumber:
            print('Your guess is too big, guess a smaller number.')
        else:
            print('Your guess is too small, guess a bigger number.')
    else:
        print('                    ___________GAME OVER ____________')

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='Play a game from the command line.')
    parser.add_argument('game', choices=['number_guessing', 'stone_paper_scissor'], help='The game to play')
    args = parser.parse_args()

    if args.game == 'number_guessing':
        number_guessing_game()
    elif args.game == 'stone_paper_scissor':
        stone_paper_scissor()

if __name__ == "__main__":
    main()