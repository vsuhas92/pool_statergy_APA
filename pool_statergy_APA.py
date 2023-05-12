"""
This script will help to build a strategy of possible combinations of players for APA Pool team
1. Run the script
2. Press 8 or 9 to select pool format from the main menu
3. Press number to select player
4. Press q to save and return to main menu
5. Press r to change previously selected player

"""

import numpy as np
import os
from colorama import Fore


def clear_console():
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for Linux and Mac
        os.system('clear')


def allCombinations(team: dict, maxpoints, current_combination=[], res: list = []):
    """
    Recursion
    """
    if maxpoints >= 0:
        if len(current_combination) == 5:
            res.append(current_combination)
            return

    if maxpoints < 0:
        return

    for key in team:
        new_max = maxpoints - team[key]
        rem_team = team.copy()
        del rem_team[key]
        allCombinations(rem_team, new_max, current_combination + [key], res)

    return res


def check(combination, *args):
    """
    :param combination: list a single possible combinations
    :param args: arg of player already played
    :return: Bool- True if the combination matches the columns in the args
    """
    check_list = []
    if len(args) == 0:
        check_list.append(True)

    for i, arg in enumerate(args):
        if combination[i] == arg:
            check_list.insert(i, True)
        else:
            check_list.insert(i, False)

    # all() and the list of boolean values
    return all(check_list)


def print_options(team, res, x: int, *args):
    """
    :param team: Full team
    :param res: list all possible combinations
    :param x: No of player already played
    :param args: arg of player already played
    :return: Player name of the selection or 'r' or 'q'
    """

    # new list created based on args- filtering rows with matching already played users
    options = []
    for combination in res:
        if check(combination, *args):
            options.append(combination[x - 1])

    # Create a list of unique names after filter already played columns out
    match_options = np.unique(options)

    # Calculation remaining skill level
    rem_skill_level = 23
    for arg in args:
        rem_skill_level -= team[arg]
    print(f"Choose player for {x} Match player({rem_skill_level})")

    # Print options
    for i, option in enumerate(match_options):
        print(f'|{i + 1}|\t{option}')

    user_input = input("Select Option:")
    if user_input == 'r':
        return 'r'
    if user_input == 'q':
        return 'q'
    player = int(user_input)

    clear_console()

    # Player Name based of user selection
    player_name = match_options[player - 1]

    # Print Played players
    print("+----------------------------------------------+")
    print(f"Played", end=': ')
    for player in args:
        print(player, end=' -- ')
    print(player_name)
    print("+----------------------------------------------+")

    return player_name


def user_guide(team, result, order: list = []):
    """
    User interface of the script

    :param team: Full team
    :param result: list all possible combinations
    :param order: list of Already played players order
    :return: list of new order as per the selections mafe by the user
    """
    while True:

        # Initialization
        if len(order) > 0:
            first = order[0]
        else:
            first = print_options(team, result, 1)
            if first == 'q':
                return order
            order.insert(0, first)
        while True:
            if len(order) > 1:
                second = order[1]
            else:
                second = print_options(team, result, 2, first)
                if second == 'r':
                    order.pop(0)
                    break
                elif second == 'q':
                    return order
                order.insert(1, second)
            while True:
                if len(order) > 2:
                    third = order[2]
                else:
                    third = print_options(team, result, 3, first, second)
                    if third == 'r':
                        order.pop(1)
                        break
                    elif third == 'q':
                        return order
                    order.insert(2, third)
                while True:
                    if len(order) > 3:
                        fourth = order[3]
                    else:
                        fourth = print_options(team, result, 4, first, second, third)
                        if fourth == 'r':
                            order.pop(2)
                            break
                        elif fourth == 'q':
                            return order
                        order.insert(3, fourth)
                    while True:
                        if len(order) > 4:
                            fifth = order[4]
                        else:
                            fifth = print_options(team, result, 5, first, second, third, fourth)
                            if fifth == 'r':
                                order.pop(3)
                                break
                            elif fifth == 'q':
                                return order
                            # order.insert(4, fifth)


def played(played):
    """
    :param played: list of players already selected
    :return: None, Print the list in the Example format
    Eg:- Played: Suhas -- Kat
    """
    if len(played) > 0:
        print(f"Played:", end=' ')
        for i, player in enumerate(played):
            print(player, end=' ')
            if i != len(played) - 1:
                print(' -- ', end='')
        print('\n')


team_9ball = {'Howard': 7, 'Bobby': 6, 'Renee': 5, 'Kat': 4, 'Suhas': 4, 'Ellen': 3, 'Pam': 2, 'Meghan': 1}
team_8ball = {'Howard': 6, 'Bobby': 6, 'Renee': 5, 'Kat': 4, 'Suhas': 4, 'Ellen': 4, 'Pam': 3, 'Meghan': 2}

# Run all possible options with skill levels and max points
result_9 = allCombinations(team=team_9ball, maxpoints=23)
result_8 = allCombinations(team=team_8ball, maxpoints=23)

# Memory of the order
eight_order = []
nine_order = []

while True:
    clear_console()
    print(Fore.LIGHTMAGENTA_EX + f'8ball: ', end='')
    played(eight_order)

    print(Fore.LIGHTGREEN_EX + f'9ball: ', end='')
    played(nine_order)
    print(Fore.RESET)

    format_pool = input("8ball or 9ball?")  # User Input to choose pool format

    if format_pool == '8':
        print(Fore.LIGHTMAGENTA_EX + "----8 BALL----\n")  # color
        eight_order = user_guide(team_8ball, result_8, eight_order)
    elif format_pool == '9':
        print(Fore.LIGHTGREEN_EX + "----9 BALL----\n")  # color
        nine_order = user_guide(team_9ball, result_9, nine_order)