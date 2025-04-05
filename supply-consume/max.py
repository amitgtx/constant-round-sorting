import numpy as np

def find_max_algorithm_S_top(arr):
    n = len(arr)
    p = int(2**0.25 * np.sqrt(n))  # Number of pivots
    pivots = np.random.choice(arr, p, replace=False)  # Select p pivots

    # Find max pivot
    p_max = max(pivots)

    # Find elements greater than p_max
    S_top = [x for x in arr if x > p_max]

    return len(S_top)

def simulate(n, trials=1000):
    u = np.sqrt(n) / (2 ** 0.25)
    ku_list = [u * k for k in range(1, 14)]
    supplied_edges = []
    consumed_edges = []
    
    for _ in range(trials):
        arr = list(np.random.rand(n))  # Generate n random numbers between 0 and 1
        s = find_max_algorithm_S_top(arr)
        consumed = s * (s - 1) / 2
        consumed_edges.append(consumed)
        # print("node consumed: ", s)

        # Find smallest ku ≥ s, else mark as fail
        supply = None
        for ku in ku_list:
            if s <= ku:
                supply = ku * (ku - 1) / 2
                # print("node supply: ", ku)
                break
        if supply is None:
            print("fail to cover, need to use backup")
            supply = n * (n - 1) / 2
        
        supplied_edges.append(supply)

    avg_supplied = sum(supplied_edges) / trials
    avg_consumed = sum(consumed_edges) / trials

    print(f"Average supplied edges: {avg_supplied:.2f}")
    print(f"Average consumed edges: {avg_consumed:.2f}")
    print(f"Ratio: {avg_supplied / avg_consumed:.2f}")

# Example usage
simulate(n=1000000, trials=100)

