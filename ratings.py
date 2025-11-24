# ratings.py

import zstandard
import requests
import re
import io
from collections import Counter
import time
from multiprocessing import Process, Pool
import math

url = 'https://database.lichess.org/standard/lichess_db_standard_rated_2025-10.pgn.zst'

r = requests.get(url, stream=True)
dctx = zstandard.ZstdDecompressor()
add_new_entry = False

num = 0
total = 0

start = time.time()
beginning = start

with dctx.stream_reader(r.raw) as reader:
    stream = io.TextIOWrapper(reader, encoding='utf-8', errors='replace')
    for line in stream:
        line = line.strip()
        if line.startswith("[Result"):
            match = re.search(r'"(.*?)"', line)
            result = match.group(1)
            add_new_entry = False
        elif line.startswith("[WhiteElo"):
            match = re.search(r'"(.*?)"', line)
            white_elo = int(match.group(1))
        elif line.startswith("[BlackElo"):
            match = re.search(r'"(.*?)"', line)
            black_elo = int(match.group(1))
            add_new_entry = True
        
        if add_new_entry == True:
            if result == "1-0": # white win
                total += (white_elo - black_elo)
            elif result == "0-1": # black win
                total += (black_elo - white_elo)

            add_new_entry = False

            num += 1
            if num % 1000000 == 0:
                end = time.time()
                dur = end - start
                start = end
                print(f"{round(100 * num / 91549148, 2)} % completed. Last chunk took {round(dur,2)} seconds.") # we know the number of games just from the site. 

print(f"Average rating difference in wins was {round(total / num, 2)} ELO points.")

print(f"100 % Completed. Total Time was {round(end - beginning, 2)} seconds.")