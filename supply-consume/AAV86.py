from math import ceil
import random
from random import sample
import numpy as np
import statistics

def compute_supply(n, total_iter):
    supply_pivots = []
    supply_interval_lens = []

    for k in range(0, total_iter):
        supply_interval_lens.append(n)
        pivots = ceil(pow(n, 1 / (total_iter - k)))
        supply_pivots.append(pivots)
        n = int(n / pivots)  # update for next round

    return supply_interval_lens, supply_pivots 


def AAV86_nodes(n, k, total_iter, supply_interval_lens, supply_pivots):
    if(n <= 1): return 1
    if(k == 1): 
      segment_size = n  
      edges_consumed = int(n*(n-1)/2)
      edges_supplied = supply_interval_lens[total_iter - k]
      print(f"[last iteration]\n clique consumed: {n}\n clique supplied: {supply_interval_lens[total_iter - k]}")
      # print(f"[last iteration] edges consumed: {edges_consumed}, edges supplied: {edges_supplied}")
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
    edges_consumed = p * (n - p) 
    if p > supply_pivots[total_iter - k]:
        supply_pivots[total_iter - k] = p
    edges_supplied = supply_pivots[total_iter - k] * supply_interval_lens[total_iter - k]
    print(f"[iteration {total_iter-k+1}]: partition {segment_sizes}\n biclique consumed: {p} * {n - p} \n biclique supplied: {supply_pivots[total_iter - k]} * {supply_interval_lens[total_iter - k]}")

    # print(f"[iteration {total_iter-k+1}]\n edges consumed: {edges_consumed}, edges supplied: {edges_supplied}\n segment sizes: {segment_sizes}, p: {p}\n supply next lens: {supply_interval_lens[total_iter - k + 1]}, supply_pivots: {supply_pivots[total_iter - k]}")

    # we can compute the supply on the fly: if consume exceeds, then find the smallest integer multiplier for supply on the fly 

    for seg in segment_sizes:
        # predict the next iteration: 
        # if seg is larger than supply_iterval_lens[next iter], 
        # then multiply that by a constant (find it using seg) and pass the changed one into the next iteration
        tmp_lens = supply_interval_lens
        if seg > tmp_lens[total_iter - k + 1]:
            const = ceil(seg / tmp_lens[total_iter - k + 1])
            tmp_lens[total_iter - k + 1] *= const
        nodes += AAV86_nodes(seg, k - 1, total_iter, tmp_lens, supply_pivots)

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


# number of elements 
n = 100

# number of iterations
total_iter = 3

# get supply, fixed before algorithm execution
supply_interval_lens, supply_pivots = compute_supply(n=100, total_iter=3)
print("supply_interval_lens: ", supply_interval_lens)
print("supply_pivots: ", supply_pivots)

# run simulation
AAV86_nodes(n=100, k=3, total_iter=3, supply_interval_lens=supply_interval_lens, supply_pivots=supply_pivots)

