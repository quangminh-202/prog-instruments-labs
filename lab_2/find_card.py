import multiprocessing as mp
import logging
import matplotlib.pyplot as plt
from tqdm import tqdm #taqaddum
from typing import Optional, Union
import hashlib

CORES = mp.cpu_count()
logger = logging.getLogger()
logger.setLevel('INFO')

def check_card(main_card, hash, bins, last_numbers):
    for card in bins:
        card = f'{card}{main_card:06d}{last_numbers}'
        if hashlib.blake2s(card.encode()).hexdigest() == hash:
            return card
    return False

def processing_card(hash, bins, last_numbers, pools=CORES):
    arguments = []
    for i in range(1000000):
        arguments.append((i, hash, bins, last_numbers))
    with mp.Pool(processes=pools) as p:
        for res in p.starmap(check_card, tqdm(arguments, desc='processes :', ncols=120)):
            if res:
                p.terminate()
                return
    return None

def luna_algorithm(card_number):
    tmp = list(map(int, card_number))[::-1]
    for i in range(1, len(tmp), 2):
        tmp[i] *= 2
        if tmp[i] > 9:
            tmp[i] = tmp[i] % 10 + tmp[i] // 10
    return sum(tmp) % 10 == 0

def graphing_and_save(data, filename) -> None:
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel('Time for working, s')
    plt.xlabel('Processes')
    plt.title('Graph')
    pools, work_times = data.keys(), data.values()
    plt.bar(pools, work_times, width=0.5)
    plt.plot(
        range(1, len(work_times)+1),
        work_times,
        linestyle=":",
        color="black",
        marker="x",
        markersize=10,
    )
    plt.savefig(filename)
    logging.info(f'Result save to the file {filename} success.')