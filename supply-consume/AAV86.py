from math import ceil
import random
from random import sample
import numpy as np
import statistics

def AAV86_nodes(n, k, total_iter, supply_interval_lens, supply_pivots):
    if(n <= 1): return 1
    if(k == 1): 
      segment_size = n  
      edges_consumed = int(n*(n-1)/2)
      edges_supplied = supply_interval_lens[total_iter - k]
      print(f"[last iteration] edges consumed: {edges_consumed}, edges supplied: {edges_supplied}")
      return n 

    p = ceil(pow(n, 1.0/k))

    # We want so split n into p parts
    num_pivots = p - 1
    nodes = n

    # Sampling p - 1 pivot locations
    m = sorted(sample(range(n), num_pivots)) # 4 7 8
    segment_sizes = [m[0] - 0]

    for i in range(num_pivots - 1):
        segment_sizes.append(m[i + 1] - m[i] - 1)

    segment_sizes.append(n - 1 - m[num_pivots - 1])

    # biclique 
    # print("iteration ", total_iter - k + 1)
    # print("segment sizes (nodes):", segment_sizes)
   
    edges_consumed = p * (n - p) 

    edges_supplied = supply_interval_lens[total_iter - k] * supply_pivots[total_iter - k]

    print(f"[iteration {total_iter-k+1}]\n edges consumed: {edges_consumed}, edges supplied: {edges_supplied}\n segment sizes: {segment_sizes}, p: {p}\n supply next lens: {supply_interval_lens[total_iter - k + 1]}, supply_pivots: {supply_pivots[total_iter - k]}")

    for seg in segment_sizes:
        nodes += AAV86_nodes(seg, k - 1, total_iter, supply_interval_lens, supply_pivots)

    return nodes


def AAV86_edges(n, k):

    if(n <= 1): return 1
    if(k == 1): return (n * (n - 1) / 2)

    p = ceil(pow(n, 1.0/k))

    # We want so split n into p parts
    num_pivots = p - 1

    # nodes = n
    comp = (n - num_pivots) * num_pivots + (num_pivots) * (num_pivots - 1) / 2

    # Sampling p - 1 pivot locations
    m = sorted(sample(range(n), num_pivots)) # 4 7 8

    # sample([0, 1, ..., 9], 3) : 7, 4, 8
    # [0, 1, ... , 9] : [0, 3], [5, 6], [], [9]

    segment_sizes = [m[0] - 0]

    for i in range(num_pivots - 1):
        segment_sizes.append(m[i + 1] - m[i] - 1)

    segment_sizes.append(n - 1 - m[num_pivots - 1])

    for seg in segment_sizes:
        comp += AAV86_edges(seg, k - 1)

    return comp


# estimate the waste ratio for 3-iteration AAV
# first iteration: picking p pivots, pairwise compare, fixed graph, no need to simulate
# second iteration: biclique, where left set is p pivots and right set is n-p elements, fixed graph, no need to simulate
# third iteration: each partition consumes a clique. We need to know the estimated size



# estimate the waste ratio for 4-iteration AAV



# estimate the waste ratio for 5-iteration AAV


def compute_supply(n, total_iter):
    supply_pivots = []
    supply_interval_lens = []

    for k in range(0, total_iter):
        supply_interval_lens.append(n)
        pivots = ceil(pow(n, 1 / (total_iter - k)))
        supply_pivots.append(pivots)
        n = int(n / pivots)  # update for next round

    return supply_interval_lens, supply_pivots 



n = 100
total_iter = 3
supply_interval_lens, supply_pivots = compute_supply(n=100, total_iter=3)
print("supply_interval_lens: ", supply_interval_lens)
print("supply_pivots: ", supply_pivots)

AAV86_nodes(n=100, k=3, total_iter=3, supply_interval_lens=supply_interval_lens, supply_pivots=supply_pivots)

# pass in an array to AAV86_nodes function such that we know for iteration i 
# which supply we use, instead of calculating that inside the function

