import numbers
import random
import time
from copy import deepcopy

from tqdm import tqdm

NUM_PRISONERS = 100
ALLOWED_DRAWER_OPENS = 50
SIMULATION_RUNS = 1000


class Drawer:

    def __init__(self, number: int, prisoner_number: int) -> None:
        self.number = number
        self.prisoner_number = prisoner_number

    def _get_drawer_numbers(self, number_of_drawers: int) -> list[int]:
        drawers = list(range(1, number_of_drawers+1))
        return drawers

    def _get_drawers_with_numbers(self, number_of_drawers: int) -> list[int]:
        drawers = self._get_drawers(number_of_drawers)
        drawers_with_numbers = deepcopy(drawers)
        random.shuffle(drawers_with_numbers)
        return drawers_with_numbers

    @classmethod
    def set_all_drawers(cls, number_of_drawers: int) -> list['Drawer']:
        drawer_numbers = list(range(1, number_of_drawers+1))
        prisoner_numbers = deepcopy(drawer_numbers)
        random.shuffle(prisoner_numbers)
        return [
            cls(
                number=drawer_numbers[i], prisoner_number=prisoner_numbers[i]
            ) for i in range(number_of_drawers)
        ]


class Prisoner:

    def __init__(self, number) -> None:
        self.number = number

    def try_to_free(self, drawers: list[Drawer], num_allowed_drawer_opens: int) -> bool:
         # print(f"Here goes prisoner {prisoner_num} trying to free himself.")
        opened_drawer_num = self.number

        for _ in range(num_allowed_drawer_opens):
            # print(f"Iteration {i+1}...")
            # print(f"Opening drawer {opened_drawer_num}...")
            prisoner_num_in_drawer = drawers[opened_drawer_num-1].prisoner_number
            # print(f"Prisoner num found in drawer: {prisoner_num_in_drawer}")

            if self.number == prisoner_num_in_drawer:
                # print(f"Prisoner {prisoner_num} is free!")
                return True

            opened_drawer_num = prisoner_num_in_drawer

        # print(f"{ALLOWED_DRAWER_OPENS} iterations over. "
        #      f"Prisoner {prisoner_num} couldn't free himself. R.I.P prisoner {prisoner_num} :(")
        return False

    @classmethod
    def set_all_prisoners(cls, number_of_prisoners: int) -> list['Prisoner']:
        return [Prisoner(number=x) for x in range(1, number_of_prisoners+1)]


class Simulator:

    def __init__(self, number_of_prisoners: int, num_allowed_drawer_opens: int) -> None:

        self.drawers = Drawer.set_all_drawers(number_of_drawers=number_of_prisoners)
        self.prisoners = Prisoner.set_all_prisoners(number_of_prisoners=number_of_prisoners)
        self.num_allowed_drawer_opens = num_allowed_drawer_opens

    def free_all_prisoners(self):
        is_prisoner_free = {}

        for prisoner in self.prisoners:
            is_prisoner_free[prisoner.number] = prisoner.try_to_free(
                self.drawers, self.num_allowed_drawer_opens
            )
            # print()

        # print(is_prisoner_free)

        are_all_prisoners_free = all(is_prisoner_free.values())
        return are_all_prisoners_free

    def simulate_one_run(self) -> bool:
        are_all_prisoners_free = self.free_all_prisoners()
        if are_all_prisoners_free:
            # print("All prisoners are free! :)")
            return True
        else:
            # print("Not all prisoners managed to escape. "
            #       "Any who was left alive has also been killed. "
            #       "R.I.P all prisoners :(")
            return False

    @classmethod
    def run_sequential(
        cls,
        number_of_runs: int,
        number_of_prisoners: int,
        num_allowed_drawer_opens: int
    ):
        simulation_results = []

        start = time.time()
        for _ in tqdm(range(number_of_runs)):
            # print(f"------------ Run {i+1} ----------------")
            simulator = cls(
                number_of_prisoners=number_of_prisoners,
                num_allowed_drawer_opens=num_allowed_drawer_opens
            )
            simulation_results.append(simulator.simulate_one_run())
        end = time.time()

        time_taken = end - start

        escape_chance = (simulation_results.count(True)/len(simulation_results))*100
        print(f"Simulations: {number_of_runs}, "
              f"Escape chance: {escape_chance: .2f}%, "
              f"Execution time: {time_taken: .2f} s")


if __name__ == '__main__':
    simulator = Simulator.run_sequential(
        number_of_runs=SIMULATION_RUNS,
        number_of_prisoners=NUM_PRISONERS,
        num_allowed_drawer_opens=ALLOWED_DRAWER_OPENS
    )