import random
from typing import List
from copy import deepcopy

NUM_DRAWERS = 100
ALLOWED_DRAWER_OPENS = 50


def get_drawers() -> List[int]:
    drawers = list(range(1,NUM_DRAWERS+1))
    return drawers


def get_drawers_with_numbers() -> List[int]:
    drawers = get_drawers()
    drawers_with_numbers = deepcopy(drawers)
    random.shuffle(drawers_with_numbers)
    return drawers_with_numbers


def try_to_free_prisoner(prisoner_num: int, drawers_with_numbers: int) -> bool:
    print(f"Here goes prisoner {prisoner_num} trying to free himself.")
    opened_drawer_num = 1

    for i in range(ALLOWED_DRAWER_OPENS):

        print(f"Iteration {i+1}...")
        print(f"Opening drawer {opened_drawer_num}...")
        prisoner_num_in_drawer = drawers_with_numbers[opened_drawer_num-1]
        print(f"Prisoner num found in drawer: {prisoner_num_in_drawer}")

        if prisoner_num == prisoner_num_in_drawer:
            print(f"Prisoner {prisoner_num} is free!")
            return True

        opened_drawer_num = prisoner_num_in_drawer

    print(f"{ALLOWED_DRAWER_OPENS} iterations over. "
          f"Prisoner {prisoner_num} couldn't free himself. R.I.P prisoner {prisoner_num} :(")
    return False


def free_all_prisoners(drawers_with_numbers):

    is_prisoner_free = {}

    # number of prisoners = number of drawers
    for prisoner_num in range(1, NUM_DRAWERS+1):
        is_prisoner_free[prisoner_num] = try_to_free_prisoner(prisoner_num, drawers_with_numbers)
        print()

    print(is_prisoner_free)

    are_all_prisoners_free = all(is_prisoner_free.values())
    return are_all_prisoners_free


if __name__ == '__main__':
    drawers = get_drawers()
    drawers_with_numbers = get_drawers_with_numbers()
    print("Numbers: ", drawers)
    print("Drawers: ", drawers_with_numbers)
    print()
    are_all_prisoners_free = free_all_prisoners(drawers_with_numbers)
    if are_all_prisoners_free:
        print("All prisoners are free! :)")
    else:
        print("Not all prisoners managed to escape. Any who was left alive has also been killed. "
              "R.I.P all prisoners :(")