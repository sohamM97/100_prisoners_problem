import random
from typing import List


NUM_DRAWERS = 10
ALLOWED_DRAWER_OPENS = 5


def get_drawers() -> List[int]:
    drawers = list(range(1,NUM_DRAWERS+1))
    random.shuffle(drawers)
    return drawers


def try_to_reach_number(prisoner_num: int, drawers: int):
    print(f"Here goes prisoner {prisoner_num} trying to free himself.")
    opened_drawer_num = 1

    for i in range(ALLOWED_DRAWER_OPENS):

        print(f"Iteration {i+1}...")
        print(f"Opening drawer {opened_drawer_num}...")
        prisoner_num_in_drawer = drawers[opened_drawer_num-1]
        print(f"Prisoner num found in drawer: {prisoner_num_in_drawer}")

        if prisoner_num == prisoner_num_in_drawer:
            print(f"Prisoner {prisoner_num} is free!")
            return

        opened_drawer_num = prisoner_num_in_drawer

    print(f"{ALLOWED_DRAWER_OPENS} iterations over. "
          f"Prisoner {prisoner_num} couldn't free himself. R.I.P prisoner {prisoner_num}")


if __name__ == '__main__':
    drawers = get_drawers()
    print("Drawers: ", drawers)
    try_to_reach_number(1, drawers)
