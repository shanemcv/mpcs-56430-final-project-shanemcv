import zstandard
import requests
import re
import io
from collections import Counter
import time
from multiprocessing import Process, Pool
import math

year_month = re.compile(r'_(\d{4}-\d{2})\.pgn')

def round_down_to_hundreds(number):
  return math.floor(number / 100) * 100

def find_pop(url):
    
    r = requests.get(url, stream=True)
    dctx = zstandard.ZstdDecompressor()
    opening_counts = Counter()
    tc_counts = Counter()
    black_wins = Counter()
    black_losses = Counter()
    black_draws = Counter()
    white_wins = Counter()
    white_losses = Counter()
    white_draws = Counter()

    match = year_month.search(url)
    ym = match.group(1)
    print(ym)

    add_new_entry = False

    num = 0

    start = time.time()
    beginning = start

    with dctx.stream_reader(r.raw) as reader:
        stream = io.TextIOWrapper(reader, encoding='utf-8', errors='replace')
        for line in stream:
            line = line.strip()

            # This is for winning proportion data
            if line.startswith("[Result"):
                match = re.search(r'"(.*?)"', line)
                result = match.group(1)
                add_new_entry = False
            elif line.startswith("[WhiteElo"):
                match = re.search(r'"(.*?)"', line)
                white_elo = round_down_to_hundreds(int(match.group(1))) # round down to a hundred-bucket so we can more expediently find trends
            elif line.startswith("[BlackElo"):
                add_new_entry = True
                match = re.search(r'"(.*?)"', line)
                black_elo = round_down_to_hundreds(int(match.group(1)))
            
            if add_new_entry == True:
                if result == "1-0": # white win
                    white_wins[white_elo] += 1
                    black_losses[black_elo] += 1
                elif result == "0-1": # black win
                    black_wins[black_elo] += 1
                    white_losses[white_elo] += 1
                else: # draw or abandoned (count as draw)
                    black_draws[black_elo] += 1
                    white_draws[white_elo] += 1

                add_new_entry = False


            # This is for opening popularity data
            if line.startswith("[ECO"):
                match = re.search(r'"(.*?)"', line)
                eco = match.group(1)
                opening_counts[eco] += 1
                num += 1
                if num % 1000000 == 0:
                    end = time.time()
                    dur = end - start
                    start = end
                    print(f"{num} completed for {ym}. Last chunk took {round(dur,2)} seconds.") # we know the number of games just from the site.

            # This is for time control data
            elif line.startswith("[TimeControl"):
                match = re.search(r'"(.*?)"', line)
                tc = match.group(1)
                tc_counts[tc] += 1

            



    total = sum(opening_counts.values())
    opening_proportions = Counter() # as a percentage
    for opening in opening_counts:
        opening_proportions[opening] = round((opening_counts[opening] / total) * 100, 3)

    tc_total = sum(tc_counts.values())
    tc_proportions = Counter() # again, as percentage
    for tc in tc_counts:
        tc_proportions[tc] = round((tc_counts[tc] / tc_total) * 100, 3)

    black_win_proportions = Counter()
    white_win_proportions = Counter()
    black_draw_proportions = Counter()
    white_draw_proportions = Counter()

    for rating_bucket in black_wins:
        tot = black_wins[rating_bucket] + black_losses[rating_bucket] + black_draws[rating_bucket]
        black_win_proportions[rating_bucket] = round((black_wins[rating_bucket] / tot) * 100, 3)
        black_draw_proportions[rating_bucket] = round((black_draws[rating_bucket] / tot) * 100, 3)

    for rating_bucket in white_wins:
        tot = white_wins[rating_bucket] + white_losses[rating_bucket] + white_draws[rating_bucket]
        white_win_proportions[rating_bucket] = round((white_wins[rating_bucket] / tot) * 100, 3)
        white_draw_proportions[rating_bucket] = round((white_draws[rating_bucket] / tot) * 100, 3)

    print(f"100 % Completed for {ym}. Total Time was {round(end - beginning, 2)} seconds.")

    print(f"Opening popularity in {ym}:")
    print(opening_proportions)

    print(f"Time Control popularity in {ym}:")
    print(tc_proportions)

    print(f"Win and draw proportion data in {ym}:")
    print("White win proportions:")
    print(white_win_proportions)
    print("White draw proportions:")
    print(white_draw_proportions)
    print("Black win proportions:")
    print(black_win_proportions)
    print("Black draw proportions:")
    print(black_draw_proportions)


if __name__ == '__main__':

    urls = ['https://database.lichess.org/standard/lichess_db_standard_rated_2025-10.pgn.zst',
        'https://database.lichess.org/standard/lichess_db_standard_rated_2023-10.pgn.zst']
    ''',
        'https://database.lichess.org/standard/lichess_db_standard_rated_2021-10.pgn.zst',
        'https://database.lichess.org/standard/lichess_db_standard_rated_2019-10.pgn.zst',
        'https://database.lichess.org/standard/lichess_db_standard_rated_2017-10.pgn.zst',
        'https://database.lichess.org/standard/lichess_db_standard_rated_2015-10.pgn.zst'
        ]
    '''
    processes = []

    with Pool(processes=2) as pool: # use a pool to run for 3 worker processes to improve runtime
        pool.map(find_pop, urls)
    
    