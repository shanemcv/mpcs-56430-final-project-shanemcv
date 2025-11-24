from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

# Choose from 2021
white_winrates = Counter({3300: 100.0, 3200: 94.828, 3100: 72.788, 3000: 62.998, 2900: 60.691, 2800: 58.013, 2700: 56.274, 2600: 55.698, 2500: 54.911, 2400: 54.435, 2300: 53.647, 2200: 52.533, 2100: 51.458, 2000: 50.606, 1900: 50.26, 1800: 49.81, 1600: 49.508, 1700: 49.481, 1400: 49.283, 1300: 49.006, 1200: 48.732, 1500: 48.584, 1100: 48.31, 1000: 48.066, 900: 46.75, 800: 44.781, 700: 41.912, 600: 33.322})
black_winrates = Counter({3300: 85.714, 3100: 66.262, 3000: 60.699, 3200: 57.143, 2900: 55.973, 2800: 53.283, 2700: 51.88, 2600: 50.974, 2500: 50.529, 2400: 50.133, 2300: 49.564, 2200: 48.792, 2100: 48.045, 2000: 47.281, 1900: 47.016, 1800: 46.66, 1600: 46.374, 1700: 46.35, 1400: 46.216, 1300: 45.753, 1500: 45.717, 1200: 45.532, 1100: 45.175, 1000: 44.932, 900: 43.742, 800: 41.924, 700: 39.23, 600: 32.067})

diff = {rating: round(white_winrates[rating] - black_winrates[rating], 2)
        for rating in white_winrates.keys() | black_winrates.keys()}

print(diff)

ratings = sorted(diff.keys())
ratings = [r for r in ratings if r < 3000] # cut off at 3000 due to sample size concerns
values = [diff[r] for r in ratings]

plt.plot(ratings, values, marker='o')
plt.xlabel("Rating")
plt.ylabel("White Win % − Black Win %")
plt.title("White Advantage by Rating")
plt.grid(True)
plt.savefig('winratesdiff.png')
plt.close()