import asyncio
from sys import argv
from math import sqrt
from time import time

# this will check if a number is prime asynchronously
async def check_if_prime_async(number : int) -> bool:
    if number == 2: return True
    if number % 2 == 0 or number % 5 == 0: return False
    # the plus 1 is because the python range class is exclusive
    for i in range(3, sqrt(number).__round__() + 1, 2):
        if number % i == 0:
            return False
    return True

# generator function that yields a potential prime number
def potential_primes_generator() -> int:
    number : int = 3
    while True:
        yield number
        number += 2

async def main() -> None:
    # cmd args for the number of async tasks
    target_prime_position = int(argv[1])
    number_of_async_tasks = int(argv[2])
    
    # generator function for potentially prime numbers
    potential_primes = potential_primes_generator()

    # found primes list and target prime variable
    found_primes = []
    target_prime = 0

    # add the only even prime to the list number 2
    found_primes.append(2)

    # print starting message
    print(f"calculating prime number : {target_prime_position} -> {number_of_async_tasks} async check_if_prime tasks")
    print(f"calculating...")

    # start timer
    time_elapsed = None
    start_time = time()
    
    while True:

        # start x number of tasks testing prime numbers depending on the cmd args
        tested_numbers_tasks = []
        async with asyncio.TaskGroup() as tg:
            for _ in range(number_of_async_tasks):
                potential_prime = next(potential_primes)
                tested_numbers_tasks.append((potential_prime , tg.create_task(check_if_prime_async(potential_prime))))

        # each of the tasks should have a potential prime and a task that contains the answer to if it is prime or not
        for result_tuple in tested_numbers_tasks:
            if await result_tuple[1]:
                found_primes.append(result_tuple[0])

        # once the list of found primes is the size of the 
        if found_primes.__len__() >= target_prime_position:
            time_elapsed = time() - start_time
            print("sorting found primes list...")
            found_primes.sort()
            target_prime = found_primes[target_prime_position - 1]
            break

    # result message
    print(f"prime number {target_prime_position} = {target_prime}")
    print(f"time elapsed : {time_elapsed} seconds")

# start main
asyncio.run(main())