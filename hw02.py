import logging
import concurrent.futures
from time import time
from multiprocessing import Pool, cpu_count


logging.basicConfig(level=logging.INFO)


def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        execution_time = end_time - start_time
        logging.info(
            f" Execution time of {func.__name__}: {execution_time * 1000.0} ms"
        )
        return result

    return wrapper


def factorize(*number: tuple[int]) -> list[list[int]]:
    """
    Factorize a number and return its divisors.
    """
    result: list[list[int]] = []
    for n in number:
        divisor: list[int] = []
        for i in range(1, n + 1):
            if n % i == 0:
                divisor.append(i)
        result.append(divisor)
    return result


@timing
def multiprocessing_factorize(*numbers: tuple[int]) -> list[list[int]]:
    """
    Factorize a list of numbers using multiprocessing.
    """
    cpu = cpu_count()
    with Pool(processes=cpu) as pool:
        result = pool.map(factorize, numbers)
    return result


@timing
def concurrent_factorise(*numbers: tuple[int]) -> list[list[int]]:
    """
    Factorize a list of numbers using concurrent.futures.
    """
    cpu = cpu_count()
    with concurrent.futures.ProcessPoolExecutor(cpu) as executor:
        result = executor.map(factorize, numbers)
    return result


if __name__ == "__main__":
    factorize_list = (128, 255, 99999, 10651060)

    start_time = time()
    a, b, c, d = factorize(*factorize_list)
    execution_time = time() - start_time
    logging.info(f" Execution time of factorize: {execution_time * 1000.0} ms")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]

    a, b, c, d = multiprocessing_factorize(*factorize_list)

    a, b, c, d = concurrent_factorise(*factorize_list)
