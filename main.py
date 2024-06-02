import number_round as nr
import letters_round as lr

import warnings
warnings.filterwarnings('ignore')

break_char = '*'
break_string = ''.join([break_char for _ in range(30)])

def main():
    print(break_string)
    print('Starting with the letters round:')
    print(break_string)
    letter_score = lr.main()
    print(break_string)
    print('Moving on to the numbers round:')
    number_score = nr.main()
    print(break_string)
    total_score = letter_score + number_score
    print(break_string)
    print(f'Well done! You scored {total_score} points.')
main()