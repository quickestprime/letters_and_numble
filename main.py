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

def sample_from_dict(dictionary):
    return random.choices(list(dictionary.keys()), weights=dictionary.values())[0]


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
                if complement in remaining_numbers:
                    return True, ('(' + str(number) + operation + str(complement) + ')')
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
                        exp_out = f"({str(number)}  + {operation} + {exp})" 
                        eval_exp_out = evaluate_arithmetic(exp_out)
                        return test, exp_out
                

    return False, None
    
   

numbers = [2,7,12,100,25,75]
target = 913
# print(pairwise_solve(numbers, target))
print(find_expression(numbers, target))


# def find_expression(numbers, target):
#     if target == 0:
#         return True, ''
#     if target in numbers:
#         return True, f'+ {str(target)}'
    
#     if True:
#         return None
    
#     elif len(numbers) > 0:
#         for number in numbers:
#             for operation in valid_operations:
                
#                 print(f"Attempting to solve the subproblem of generating {target} with {numbers}:")
#                 forward_operation = FORWARD_OPERATIONS[operation]
#                 if forward_operation(target, number):
#                     pass
#                 inverse = INVERSE_OPERATIONS[operation]
                
#                 new_target = inverse(target, number)
#                 new_numbers = [x for x in numbers if x != number]
                
#                 found, test_string = find_expression(new_numbers, new_target)
#                 print(f"Generated attempt: {str(number) + operation + test_string}")
#                 if found:
#                     return True, str(number) + operation + test_string

#     return False, 'No solution.'



def main():
    puzzle = generate_puzzle()
    if puzzle['n_bigs'] > 0:
        print(f"Your {puzzle['n_bigs']} bigs are: {puzzle['bigs']}")
    print(f"Your {puzzle['n_smalls']} smalls are: {puzzle['smalls']}")
    print(f"Target is: {puzzle['target']}" )
    solved = False
    while not solved:
        solve_attempt = input('Input solution (or type to q to quit): ')
        if solve_attempt == 'q':
            break
        solved = is_valid_solve(puzzle, solve_attempt)
        if solved:
            print('You got it!')
        else:
            print('Nope.')

# main()