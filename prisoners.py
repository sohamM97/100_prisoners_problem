import concurrent.futures
import random
import time
from copy import deepcopy
from enum import Enum

from tqdm import tqdm


class RunMode(Enum):
    SEQUENTIAL = "sequential"
    MULTIPROCESSING = "multiprocessing"
    MULTITHREADING = "multithreading"


NUM_PRISONERS = 100
ALLOWED_DRAWER_OPENS = 50
SIMULATION_RUNS = 100000
NUM_PARALLEL_EXECUTIONS = 100
RUN_MODE = RunMode.MULTITHREADING


class Drawer:
    def __init__(self, number: int, prisoner_number: int) -> None:
        self.number = number
        self.prisoner_number = prisoner_number

    @classmethod
    def set_all_drawers(cls, number_of_drawers: int) -> list["Drawer"]:
        drawer_numbers = list(range(1, number_of_drawers + 1))
        prisoner_numbers = deepcopy(drawer_numbers)
        random.shuffle(prisoner_numbers)
        return [
            cls(number=drawer_numbers[i], prisoner_number=prisoner_numbers[i])
            for i in range(number_of_drawers)
        ]


class Prisoner:
    def __init__(self, number) -> None:
        self.number = number
        self.is_free = False

    def try_to_free(self, drawers: list[Drawer], num_allowed_drawer_opens: int) -> None:
        # print(f"Here goes prisoner {prisoner_num} trying to free himself.")
        opened_drawer_num = self.number

        for _ in range(num_allowed_drawer_opens):
            # print(f"Iteration {i+1}...")
            # print(f"Opening drawer {opened_drawer_num}...")
            prisoner_num_in_drawer = drawers[opened_drawer_num - 1].prisoner_number
            # print(f"Prisoner num found in drawer: {prisoner_num_in_drawer}")

            if self.number == prisoner_num_in_drawer:
                # print(f"Prisoner {prisoner_num} is free!")
                self.is_free = True
                return

            opened_drawer_num = prisoner_num_in_drawer

        # print(f"{ALLOWED_DRAWER_OPENS} iterations over. "
        #      f"Prisoner {prisoner_num} couldn't free himself. R.I.P prisoner {prisoner_num} :(")

    @classmethod
    def set_all_prisoners(cls, number_of_prisoners: int) -> list["Prisoner"]:
        return [Prisoner(number=x) for x in range(1, number_of_prisoners + 1)]


class Simulator:
    def __init__(self, number_of_prisoners: int, num_allowed_drawer_opens: int) -> None:

        self.drawers = Drawer.set_all_drawers(number_of_drawers=number_of_prisoners)
        self.prisoners = Prisoner.set_all_prisoners(
            number_of_prisoners=number_of_prisoners
        )
        self.num_allowed_drawer_opens = num_allowed_drawer_opens

    def free_all_prisoners(self):
        for prisoner in self.prisoners:
            prisoner.try_to_free(self.drawers, self.num_allowed_drawer_opens)
            # print()

        are_all_prisoners_free = all([prisoner.is_free for prisoner in self.prisoners])
        return are_all_prisoners_free

    @classmethod
    def simulate_one_run(
        cls, number_of_prisoners: int, num_allowed_drawer_opens: int
    ) -> bool:
        simulator = cls(number_of_prisoners, num_allowed_drawer_opens)
        return simulator.free_all_prisoners()

    @classmethod
    def run_sequential(
        cls,
        number_of_runs: int,
        number_of_prisoners: int,
        num_allowed_drawer_opens: int,
    ):
        simulation_results = []

        for _ in tqdm(range(number_of_runs)):
            # print(f"------------ Run {i+1} ----------------")
            simulation_results.append(
                cls.simulate_one_run(
                    number_of_prisoners=number_of_prisoners,
                    num_allowed_drawer_opens=num_allowed_drawer_opens,
                )
            )

        return simulation_results

    @classmethod
    def run_parallel_with_multiprocessing(
        cls,
        number_of_runs: int,
        number_of_prisoners: int,
        num_allowed_drawer_opens: int,
        number_of_processes: int,
    ):
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=number_of_processes
        ) as executor:
            simulation_results = executor.map(
                cls.simulate_one_run,
                [number_of_prisoners] * number_of_runs,
                [num_allowed_drawer_opens] * number_of_runs,
            )

        return list(simulation_results)

    @classmethod
    def run_parallel_with_multithreading(
        cls,
        number_of_runs: int,
        number_of_prisoners: int,
        num_allowed_drawer_opens: int,
        number_of_threads: int,
    ):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=number_of_threads
        ) as executor:
            simulation_results = executor.map(
                cls.simulate_one_run,
                [number_of_prisoners] * number_of_runs,
                [num_allowed_drawer_opens] * number_of_runs,
            )

        return list(simulation_results)

    @classmethod
    def run(
        cls,
        mode: RunMode,
        number_of_runs: int,
        number_of_prisoners: int,
        num_allowed_drawer_opens: int,
        num_parallel_executions: int,
    ):

        start = time.time()
        print(f"Running simulations with mode: {mode}...")
        if mode == RunMode.SEQUENTIAL:
            simulation_results = cls.run_sequential(
                number_of_runs, number_of_prisoners, num_allowed_drawer_opens
            )
        elif mode == RunMode.MULTIPROCESSING:
            simulation_results = cls.run_parallel_with_multiprocessing(
                number_of_runs,
                number_of_prisoners,
                num_allowed_drawer_opens,
                num_parallel_executions,
            )
        elif mode == RunMode.MULTITHREADING:
            simulation_results = cls.run_parallel_with_multithreading(
                number_of_runs,
                number_of_prisoners,
                num_allowed_drawer_opens,
                num_parallel_executions,
            )
        end = time.time()

        time_taken = end - start

        escape_chance = (simulation_results.count(True) / len(simulation_results)) * 100
        print(
            f"Simulations completed: {len(simulation_results)}, "
            f"Escape chance: {escape_chance: .2f}%, "
            f"Execution time: {time_taken: .4f}s"
        )


if __name__ == "__main__":
    simulator = Simulator.run(
        mode=RUN_MODE,
        number_of_runs=SIMULATION_RUNS,
        number_of_prisoners=NUM_PRISONERS,
        num_allowed_drawer_opens=ALLOWED_DRAWER_OPENS,
        num_parallel_executions=NUM_PARALLEL_EXECUTIONS,
    )
