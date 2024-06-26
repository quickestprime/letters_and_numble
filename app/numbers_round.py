import numpy as np
import random
import re



PROB_MASS_FOR_N_BIGS = {
    0 : 0.125,
    1 : 0.2,
    2 : 0.35,
    3 : 0.225,
    4 : 0.1
}

BIGS = [25, 50, 75, 100]
SMALLS = [1,2,3,4,5,6,7,8,9]

valid_operations = ['+','-','x','/']

FORWARD_OPERATIONS = {
    '+':np.add,
    '-':np.subtract,
    'x':np.multiply,
    '/':np.divide
}

INVERSE_OPERATIONS = {
    '+':np.subtract,
    '-':np.add,
    'x':np.divide,
    '/':np.multiply
}

def sample_from_dict(dictionary):
    return random.choices(list(dictionary.keys()), weights=dictionary.values())[0]

def difference_to_points(difference):
    if difference < 2:
        return 7
    if difference < 5:
        return 3
    else:
        return 0

def extract_numbers_and_operators(arithmetic_str):
    # Pattern to match integers or decimal numbers and arithmetic operators (+, -, *, /)
    pattern = r"(\d*\.\d+|\d+|[+\-*/])"
    # Find all matches in the input string
    matches = re.findall(pattern, arithmetic_str)
    return matches


def evaluate_arithmetic(expression):
    try:
        # Replace x with * to fit Python multiplication syntax
        expression = expression.replace('x', '*')
        # Use eval to evaluate the arithmetic expression
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {e}"

def generate_puzzle():
    target = random.randint(100, 1000)
    n_bigs = sample_from_dict(PROB_MASS_FOR_N_BIGS)
    puzzle_bigs = random.sample(BIGS, n_bigs)
    n_smalls = 6 - n_bigs
    puzzle_smalls = random.sample(SMALLS, n_smalls)
    
    return {
        'n_bigs' : n_bigs,
        'n_smalls' : n_smalls,
        'target' : target,
        'bigs' : puzzle_bigs,
        'smalls' : puzzle_smalls
    }

def is_valid_solve(puzzle, expression):
    return evaluate_arithmetic(expression) == puzzle['target']

def pairwise_solve(numbers,target):
    if len(numbers) == 1 or np.mod(target,1) != 0:
        return False, None
    for operation in valid_operations:
        for number in numbers: 
            remaining_numbers = [x for x in numbers if x!=number]
            inverse = INVERSE_OPERATIONS[operation]
            complement = inverse(target, number)
            if np.mod(complement, 1) == 0:
                complement = int(complement)
                if complement in remaining_numbers:
                    return True, ('(' + str(complement)  + operation +  str(number) + ')')
    return False, None

def find_expression(numbers, target):
    # if len(numbers) == 0:
    #      return False, None
    
    can_be_solved_pairwise, output = pairwise_solve(numbers,target)
    
    if can_be_solved_pairwise:
        return True, output
    
    else:
        for number in numbers:
            remaining_numbers = [x for x in numbers if x!=number]
            if len(remaining_numbers) > 1:
                for operation in valid_operations:
                    inverse = INVERSE_OPERATIONS[operation]
                    complement = inverse(target, number)
                    test, exp = find_expression(remaining_numbers, complement)
                    if test:
                        # print(exp, '=', complement)
                        if operation in ['x','/']:
                            exp_out = f"({exp}) {operation} {str(number)}" 
                        else:
                            exp_out = f"{exp} {operation} {str(number)}" 
                        return test, exp_out
                

    return False, None
    

def solve_puzzle(puzzle):
    distance_away = 0
    target = puzzle['target']
    upper = puzzle['target']
    lower = puzzle['target']
    numbers = puzzle['bigs'] + puzzle['smalls']
    solved = False
    while not solved:
        solved, solution = find_expression(numbers, target)
        if solved:
            return solution, distance_away, target
        else:
            distance_away += 1
            upper += 1
            lower -= 1
            solved, solution = find_expression(numbers, upper)
            if solved:
                return solution, distance_away, upper
            solved, solution = find_expression(numbers, lower)
            if solved:
                return solution, distance_away, lower

def show_answer(puzzle):
    solution, distance_away, solved_for = solve_puzzle(puzzle)
    if distance_away == 0:
        print(f"A solution was {solution}")
    else:
        print(f"You could only get within {distance_away} today.")
        print(f"You could make {solved_for} with: {solution}")          

def main():
    puzzle = generate_puzzle()
    if puzzle['n_bigs'] > 0:
        print(f"Your {puzzle['n_bigs']} bigs are: {puzzle['bigs']}")
    print(f"Your {puzzle['n_smalls']} smalls are: {puzzle['smalls']}")
    print(f"Target is: {puzzle['target']}" )
    solved = False
    player_max_score = 0
    while not solved:
        solve_attempt = input('Input solution (or type to q to quit): ')
        if solve_attempt == 'q':
            show_answer(puzzle)
            return 0
        solved = is_valid_solve(puzzle, solve_attempt)
        if solved:
            print('You got it! You scored 10 points.')
            return 10
        else:
            difference = np.abs(puzzle['target'] - evaluate_arithmetic(solve_attempt))
            points = difference_to_points(difference)
            if points > player_max_score:
                player_max_score = points
            feedback = input(f"You're off by {difference}. This will score you {points} points. Your best score up to now is {player_max_score}. Lock in this score? (y/n): ")
            if feedback == 'y':
                show_answer(puzzle)
                return points

if __name__ == '__main__':
    main()