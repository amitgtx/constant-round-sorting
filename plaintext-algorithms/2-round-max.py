def find_max_partitioned(arr, num_partitions):
    """
    Find the maximum element in an array using partitioned pairwise comparisons.
    
    Args:
        arr: List of comparable elements
        num_partitions: Number of partitions to divide the array into
    
    Returns:
        The maximum element in the array
    """
    if not arr:
        return None
    
    if len(arr) == 1:
        return arr[0]
    
    n = len(arr)
    
    # Step 1: Partition n elements into p partitions
    partitions = create_partitions(arr, num_partitions)
    
    # Step 2: For each partition, find the maximum using pairwise comparisons
    partition_maxes = []
    
    for i, partition in enumerate(partitions):
        print(f"Processing partition {i + 1}: {partition}")
        
        if len(partition) == 1:
            partition_max = partition[0]
        else:
            # Find max in this partition using pairwise comparison ranking
            partition_max = find_max_by_ranking(partition)
        
        partition_maxes.append(partition_max)
        print(f"Partition {i + 1} max: {partition_max}")
    
    print(f"\nPartition maxes: {partition_maxes}")
    
    # Step 3: Find the overall max from partition maxes using pairwise comparisons
    if len(partition_maxes) == 1:
        overall_max = partition_maxes[0]
    else:
        overall_max = find_max_by_ranking(partition_maxes)
    
    return overall_max


def create_partitions(arr, num_partitions):
    """
    Divide array into approximately equal partitions.
    
    Args:
        arr: Input array to partition
        num_partitions: Number of partitions desired
    
    Returns:
        List of partitions (sublists)
    """
    n = len(arr)
    # Ensure we don't have more partitions than elements
    num_partitions = min(num_partitions, n)
    
    partitions = []
    partition_size = n // num_partitions
    remainder = n % num_partitions
    
    start_idx = 0
    for i in range(num_partitions):
        # Distribute remainder elements among first few partitions
        current_size = partition_size + (1 if i < remainder else 0)
        end_idx = start_idx + current_size
        
        partitions.append(arr[start_idx:end_idx])
        start_idx = end_idx
    
    return partitions


def find_max_by_ranking(elements):
    """
    Find maximum element using pairwise comparison and ranking aggregation.
    
    For each element a_i, we count how many elements it's greater than or equal to.
    The element with the highest rank (beats the most other elements) is the maximum.
    
    Args:
        elements: List of elements to find max from
    
    Returns:
        The maximum element
    """
    if not elements:
        return None
    
    if len(elements) == 1:
        return elements[0]
    
    print(f"  Finding max in: {elements}")
    
    # For each element, calculate its rank based on pairwise comparisons
    ranks = []
    
    for i, element in enumerate(elements):
        rank = 0
        comparisons = []
        
        # Compare element with every other element
        for j, other_element in enumerate(elements):
            if i != j:
                # Pairwise comparison: element >= other_element
                comparison_result = element >= other_element
                comparisons.append(f"{element} >= {other_element}: {comparison_result}")
                
                # If element is greater than or equal to other_element, increment rank
                if comparison_result:
                    rank += 1
        
        ranks.append(rank)
        print(f"    Element {element}: rank = {rank}")
        print(f"      Comparisons: {comparisons}")
    
    # Find the element with the highest rank
    max_rank = max(ranks)
    max_index = ranks.index(max_rank)
    
    print(f"    Max element: {elements[max_index]} (rank: {max_rank})")
    return elements[max_index]


# Example usage and testing
if __name__ == "__main__":
    # Test case 1: Simple array
    print("=== Test Case 1 ===")
    test_array_1 = [3, 7, 1, 9, 4, 6, 2]
    result_1 = find_max_partitioned(test_array_1, 3)
    print(f"Input: {test_array_1}")
    print(f"Maximum found: {result_1}")
    print(f"Expected: {max(test_array_1)}")
    print()
    
    # Test case 2: Array with duplicates
    print("=== Test Case 2 ===")
    test_array_2 = [5, 2, 9, 2, 9, 1]
    result_2 = find_max_partitioned(test_array_2, 2)
    print(f"Input: {test_array_2}")
    print(f"Maximum found: {result_2}")
    print(f"Expected: {max(test_array_2)}")
    print()
    
    # Test case 3: Single partition (equivalent to normal pairwise comparison)
    print("=== Test Case 3 ===")
    test_array_3 = [8, 3, 5, 1]
    result_3 = find_max_partitioned(test_array_3, 1)
    print(f"Input: {test_array_3}")
    print(f"Maximum found: {result_3}")
    print(f"Expected: {max(test_array_3)}")