
def display_matrix(m):

	print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in m]))

def comp(x, y):


	if (x < y):
		return 1
	else:
		return 0



def merge(A, B):

	count = 0

	## ROUND 1 : Compare the leaders of each group in A with the leader of each group in B

	comp_matrix = [[0 for _ in range(k * k + 1)] for _ in range(k * k + 2)]

	# Setting first row to be 1 by default, last row to be 0 by default, last column to be 1 by default
	for i in range(k * k): 
		comp_matrix[0][i] = 1
		comp_matrix[k * k + 1][i] = 0
		comp_matrix[i + 1][k * k] = 1

	# Setting top right and bottom right cells to be 1 and 0 respectively

	comp_matrix[0][k * k] = 1
	comp_matrix[k * k + 1][k * k] = 0


	for i in range(0, n, k):
		for j in range(0, n, k):
			comp_matrix[i // k + 1][j // k] = comp(A[i], B[j])
			count += 1

	print("COMP MATRIX")


	display_matrix(comp_matrix)



	## ROUND 2 : 


	last_one_row_index_for_each_B = [0 for _ in range(k * k + 1)]

	for j in range(k * k + 1):
		for i in range(0, k * k + 2):
			if(comp_matrix[i][j] == 1): last_one_row_index_for_each_B[j] = i


	print("LAST ONE ROW INDEX")

	print (last_one_row_index_for_each_B)


	g_star_matrix = [[0 for _ in range(k * k + 1)] for _ in range(k * k + 2)]

	for j in range(k * k):
		for i in range(last_one_row_index_for_each_B[j], last_one_row_index_for_each_B[j + 1] + 1):
			g_star_matrix[i][j] = 1


	# display_matrix(g_star_matrix)


	# g_star_matrix = g_star_matrix[1: k * k + 1]

	final_g_star_matrix = [[g_star_matrix[i + 1][j] for j in range(k * k)] for i in range(k * k)]

	# print("G STAR MATRIX")

	# display_matrix(g_star_matrix)
	# display_matrix(final_g_star_matrix)


	# This is a k^2 * k^2 matrix where each cell is itelf a k * k 
	g_star_comp_matrix = [[[[0 for _ in range(k)] for _ in range(k)] for _ in range(k * k)] for _ in range(k * k)]

	for i in range(k * k):
		for j in range(k * k):

			if(final_g_star_matrix[i][j] == 0): continue

			# Compare all elements in group i of A with all elements in group j of B

			for p in range(k):
				for q in range(k):
					# Compare the p^th element in group i of A with q^th element in group j of B and update rank
					x = A[i * k + p]
					y = B[j * k + q]
					c = comp(x, y)
					count += 1

					g_star_comp_matrix[i][j][p][q] = 1 - c



	## Find the rank of each elements in A group by group. The ranks of each element in B
	## can be directly inferred from the rank of each element in A since both a sorted individually.

	# Initializing the rank of each element in A and B
	rank_A = [0 for i in range(n)]

	rank_so_far = 0

	## Iterating over all groups in A
	for g in range(k * k):

		# This is the rank due to previous group elements in A
		starting_rank = g * k

		j = 0

		for i in range(k * k):

			if(final_g_star_matrix[g][i] == 1):

				j = i
				break

		# while(final_g_star_matrix[g][j + 1] == 0):
		# 	print("m : ", final_g_star_matrix[g][j + 1]) 
		# 	j += 1
		# 	print ("Check : ", g, j)


		starting_rank += j * k

		## Iterating over all groups in B
		for h in range(j, k * k):

			if(final_g_star_matrix[g][h] == 0): break

			for p in range(k):

				for q in range(k):

						rank_A[k * g + p] += g_star_comp_matrix[g][h][p][q]



		for p in range(k):

			rank_A[k * g + p] += (starting_rank + p)


		# rank_so_far = rank_A[k * g + (k - 1)] + 1



	rank_B = []

	j = 0

	for i in range(2 * n):

		if(j < n and i == rank_A[j]):

			j += 1
			continue

		rank_B.append(i)
	



	# print("RANK A : ", rank_A)
	# print("RANK B : ", rank_B)


	C = [0 for _ in range(2 * n)]


	for i in range(n):

		C[rank_A[i]] = A[i]
		C[rank_B[i]] = B[i]


	return C, count





import random 

k = 2

n = k ** 3


## Aim : Merge two sorted lists A and B, each of length n

t = 1

for _ in range(t):

	S = random.sample(range(2 * n), 2 * n)

	A = S[0:n]
	B = S[n:2 * n]

	A.sort()
	B.sort()

	C, count = merge(A, B)

	for i in range(2 * n):

		assert(C[i] == i)

	print("Comparsions = ", count)
	# print ("A = ", A)
	# print ("B = ", B)
	# print ("C = ", C)
