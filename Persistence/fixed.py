
import galois
import numpy as np


# Pretty-prints matrices.
def printer(A, split):
	m, n = A.shape

	for i in range(m):
		for j in range(n):
			if j == split: print("| ", end="")
			print(f"{A[i,j]} ", end="")
		print()



# Set the base field as Z/2Z; we'll change the field later.
F = galois.GF(2)

# Second and first boundary matrices.
B2 = F(np.array([
	[1,1,1,1,0,0,0,0,0],
	[0,0,1,0,1,1,1,0,0],
	[0,1,0,0,0,1,0,1,1]
]).T)

B1 = F(np.array([
	[1,1,0,0,0,0],
	[1,0,1,0,0,0],
	[0,1,0,1,0,0],
	[0,0,1,1,0,0],
	[0,1,0,0,1,0],
	[0,0,0,0,1,1],
	[0,0,0,1,0,1],
	[1,0,0,0,1,0],
	[0,0,1,0,0,1]
]).T)

# Compute the rank of the image. (We should know this by construction!)
irank = B2.shape[1] - np.where(~B2.row_reduce().any(axis=0))[0].shape[0]


# Compute a basis for the kernel of the first boundary matrix. Basis vectors are
# the row vectors of the adjoined matrix corresponding to zero rows in the (row-
# reduced) original.
augmented = F(np.concatenate([B1.T, F.Identity(B1.shape[1])], axis=1))
reduced = augmented.row_reduce()

# This indexing step finds the index of the lowest zero row in the original matrix.
# The index of the lowest zero row in the original matrix is also the index of
# the first (row) vector in the basis of the kernel.
low = np.where(~(reduced[:,:B1.shape[0]]).any(axis=1))[0][0]

kernel = reduced[low:,B1.shape[0]:].T


# Now we can compute the rank of ker(B1)/im(B2) by adjoining the kernel on the
# right of B2, then row-reducing, then applying rank-nullity.
augmented = F(np.concatenate([B2, kernel], axis=1))
reduced = augmented.row_reduce()

# This indexing step counts the rank of ker(B1)/im(B2) in a hacky way: since we
# know rank(im(B2)), we can just count the number of nonzero rows in the submatrix
# formed by throwing out the first rank(im(B2)) rows of the augmented matrix.
# These rows correspond directly to elements of ker(B1) that are *not* (linear
# combinations of) elements in im(B2), which form the basis for ker(B1)/im(B2),
# the first homology group.
rank = reduced[irank:,B2.shape[1]:].max(axis=1).sum()
