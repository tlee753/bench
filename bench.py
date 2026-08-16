import argparse
import multiprocessing as mp
import time


def calculate_primes(limit: int) -> int:
    """CPU-bound task: Count prime numbers up to `limit` using trial division."""
    count = 0
    for num in range(2, limit):
        is_prime = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


def worker_task(_: int) -> int:
    """Worker wrapper to execute workload chunk."""
    return calculate_primes(limit=100_000)


def run_benchmark(mode: str, iterations: int):
    total_cores = mp.cpu_count()
    print(f"Detected CPU Cores : {total_cores}")
    print(f"Benchmark Mode     : {mode.upper()}")
    print(f"Total Work Chunks  : {iterations}")
    print("-" * 40)
    print("Running benchmark... Please wait.")

    start_time = time.perf_counter()

    if mode == "single":
        # Run sequentially on a single thread
        results = [worker_task(i) for i in range(iterations)]
    else:
        # Run in parallel across all available CPU cores
        with mp.Pool(processes=total_cores) as pool:
            results = pool.map(worker_task, range(iterations))

    elapsed_time = time.perf_counter() - start_time
    score = (iterations / elapsed_time) * 1000

    print("-" * 40)
    print(f"Execution Time    : {elapsed_time:.3f} seconds")
    print(f"Benchmark Score   : {score:.2f} pts")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Vanilla Python CPU Benchmark Tool"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["single", "multi"],
        default="multi",
        help="Execution mode: 'single' core or 'multi' core (default: multi)",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=200,
        help="Number of workload chunks to execute (default: 200)",
    )

    args = parser.parse_args()
    run_benchmark(mode=args.mode, iterations=args.iterations)
