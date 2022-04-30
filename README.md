# Travelling Salesman Problem Approximation Algorithm
## Made by Callum Pritchard
## Part of University of York - Computer Science
---
Enjoy, don't break anything!

## Overview
- Requirements can be found within requirements.txt
- Python 3.8 required 
- Run `main.py` for a GUI version and `testing.py` for a bulk run headless version.

## Datasets
TSPLIB datasets are found within `dataset/`.

## Graphs
Random graphs and notable graphs are saved within `graphs/`.

These are not easily loaded so not expected for marking, just a note that they exist.

## Results
Results can be found within `statistics/`

## Running GUI
`pip -r requirements.txt`  
`python main.py`

## Running Headless (bulk testing)
Constants at the top of the file can be edited for different behaviour, relevant comments can be found within the file.
Prims algorithm is disabled for TSPLIB testing for time reasons, there is no override.

By default tsplib will not run on files with over 2000 cities for performance reasons. There is an override for this named `BIGREDBUTTON` as I imagine your PC will go nuclear. Set to `True` to allow the larger 85900 city graph and others to execute.
