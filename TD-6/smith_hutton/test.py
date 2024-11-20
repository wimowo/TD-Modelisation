import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags, lil_matrix
from scipy.sparse.linalg import spsolve

# Parameters
Nx, Ny = 5, 5  # Grid resolution
Lx, Ly = 2, 1  # Domain size in x and y directions
Pe = 1  # Péclet number
alpha = 2  # Parameter for boundary condition

# Discretization
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)
x = np.linspace(-1, 1, Nx)
y = np.linspace(0, 1, Ny)


# Velocity field u = (ux, uy)
def velocity_field(x, y):
    ux = 2 * y * (1 - x ** 2)
    uy = -2 * x * (1 - y ** 2)
    return ux, uy


# Initialize concentration field
c = np.zeros((Nx, Ny))

# Build sparse matrix and right-hand side vector
A = lil_matrix((Nx * Ny, Nx * Ny))  # Sparse matrix in list of lists format for easy assignment
b = np.zeros(Nx * Ny)  # Right-hand side


# Helper function to map 2D indices to 1D
def idx(i, j):
    return i + j * Nx


# Boundary conditions and coefficients
for j in range(Ny):
    for i in range(Nx):
        p = idx(i, j)

        if j == 0:  # Bottom boundary (inlet condition)
            c[i, j] = 1 + np.tanh(alpha * (2 * x[i] + 1))
            A[p, p] = 1
            b[p] = c[i, j]

        elif j == Ny - 1:  # Top boundary
            A[p, p] = 1
            b[p] = 1 - np.tanh(alpha)

        elif i == Nx - 1:  # Right boundary (outlet, Neumann condition)
            A[p, p] = 3
            A[p, idx(i - 1, j)] = -4
            A[p, idx(i - 2, j)] = 1
            b[p] = 0  # Neumann condition (dc/dn = 0)

        elif i == 0:  # Left boundary
            A[p, p] = 1
            b[p] = 1 - np.tanh(alpha)

        else:  # Interior points
            # Get velocity field at (i, j)
            ux, uy = velocity_field(x[i], y[j])

            # Diffusion terms (central difference)
            A[p, idx(i, j)] = -2 / dx ** 2 - 2 / dy ** 2
            A[p, idx(i + 1, j)] = 1 / dx ** 2
            A[p, idx(i - 1, j)] = 1 / dx ** 2
            A[p, idx(i, j + 1)] = 1 / dy ** 2
            A[p, idx(i, j - 1)] = 1 / dy ** 2

            # Advection terms (upwind scheme)
            if ux > 0:
                A[p, idx(i, j)] += -ux / dx
                A[p, idx(i - 1, j)] += ux / dx
            else:
                A[p, idx(i, j)] += ux / dx
                A[p, idx(i + 1, j)] += -ux / dx

            if uy > 0:
                A[p, idx(i, j)] += -uy / dy
                A[p, idx(i, j - 1)] += uy / dy
            else:
                A[p, idx(i, j)] += uy / dy
                A[p, idx(i, j + 1)] += -uy / dy

# Convert matrix A to CSR format for efficient solving
A = A.tocsr()

# Solve the linear system A * c_flat = b
c_flat = spsolve(A, b)

# Reshape the solution into a 2D array
c_solution = c_flat.reshape((Nx, Ny))

# Plot the solution
plt.figure(figsize=(8, 4))
plt.contourf(x, y, c_solution.T, 20, cmap="viridis")
plt.colorbar(label="Concentration c")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Concentration Profile for Smith-Hutton Problem")
plt.show()
