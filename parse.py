import zstandard
import requests
import re
import io
from collections import Counter
import time
print("imported")

'''
line = "[WhiteElo \"2100\"]"
match = re.search(r'"(.*?)"', line)
if match:
    print(match.group(1))

'''

# Get October database. This is 29.9 GB so we'll stream it
url = 'https://database.lichess.org/standard/lichess_db_standard_rated_2025-10.pgn.zst'

r = requests.get(url, stream=True)
dctx = zstandard.ZstdDecompressor()
add_new_entry = False

opening_counts = Counter()
opening_white_elo = Counter()
opening_black_elo = Counter()
num = 0

start = time.time()
beginning = start

with dctx.stream_reader(r.raw) as reader:
    stream = io.TextIOWrapper(reader, encoding='utf-8', errors='replace')
    for line in stream:
        line = line.strip()
        if line.startswith("[WhiteElo"):
            add_new_entry = False
            match = re.search(r'"(.*?)"', line)
            white_elo = int(match.group(1))
        elif line.startswith("[BlackElo"):
            match = re.search(r'"(.*?)"', line)
            black_elo = int(match.group(1))
        elif line.startswith("[ECO"): # [ECO to just get the code, [Opening to get full name
            add_new_entry = True
            match = re.search(r'"(.*?)"', line)
            eco = match.group(1)
            opening_counts[eco] += 1
            opening_white_elo[eco] += white_elo
            opening_black_elo[eco] += black_elo
            num += 1
            if num % 1000000 == 0:
                end = time.time()
                dur = end - start
                start = end
                print(f"{round(100 * num / 91549148, 2)} % completed. Last chunk took {round(dur,2)} seconds.") # we know the number of games just from the site. 

print(f"100 % Completed. Total Time was {round(end - beginning, 2)} seconds.")
print(opening_counts)
print(opening_white_elo)
print(opening_black_elo)