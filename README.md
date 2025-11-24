# mpcs-56430-final-project-shanemcv
MPCS 56430 Scientific Computing Final Project - Chess Database Analysis

# Core Questions for Analysis

## Are certain openings more popular at different rating levels? 
In order to answer this question, I used only the most recent file (for October, 2025) since the sample size is large enough to answer. I first found the raw number of times each opening was played by [ECO code](https://www.365chess.com/eco.php) in the month of October. Then, I added the ELO ratings for both the white and black players in the game and found the average. 

For each piece color, the best and worst 5 openings by rating level are plotted. 

## Are some openings gaining or losing popularity?
In order to analyze this, I used a multiprocessing routine to look at the October game files over a 10-year period with a 2-year gap. 

## Are any time controls gaining or losing popularity? 
In order to analyze this, I used a multiprocessing routine to look at the August game files over a 10-year period with a 2-year gap. 

## Does playing with white or black matter more at different rating levels? Has this changed over time?

## What is the average rating difference for the winning side? 


