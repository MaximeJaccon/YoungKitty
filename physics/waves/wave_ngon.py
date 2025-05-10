import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.path import Path

# Simulation parameters
Nx, Ny = 600, 600  # Grid size
dx = dy = 3.0      # Spatial resolution
c = 3.0            # Wave speed
dt = 0.5           # Time step
steps = 20000       # Number of time steps

# Stability condition
alpha = c * dt / dx
if alpha >= 1 / np.sqrt(2):
    raise ValueError("Stability condition violated: reduce dt or increase dx.")

# Create coordinate grid centered at (0, 0)
x = dx * (np.arange(Nx) - Nx // 2)
y = dy * (np.arange(Ny) - Ny // 2)
X, Y = np.meshgrid(x, y)

# Function to create an n-gon mask
def create_ngon_mask(n, radius, X, Y):
    """Creates a boolean mask for a regular n-gon centered at (0, 0)."""
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    vertices = np.stack((radius * np.cos(angles), radius * np.sin(angles)), axis=1)
    path = Path(vertices)
    points = np.stack((X.flatten(), Y.flatten()), axis=1)
    mask_flat = path.contains_points(points)
    return mask_flat.reshape(X.shape), vertices

# Parameters for the polygon
n = 6         # Number of polygon sides (change this to any integer >= 3)
radius = 850  # Radius from center to vertex
mask, vertices = create_ngon_mask(n, radius, X, Y)

# Initialize wave fields
u_prev = np.zeros((Ny, Nx))
u_curr = np.zeros((Ny, Nx))
u_next = np.zeros((Ny, Nx))

# Initial disturbance: Gaussian at the center
sigma = 10.0
u_curr += np.exp(-((X)**2 + (Y)**2) / (2 * sigma**2)) * mask

# Prepare for animation
masked_u = np.ma.masked_where(~mask, u_curr)
cmap = plt.cm.viridis.copy()
cmap.set_bad(color='black')

extent = [x.min(), x.max(), y.min(), y.max()]
fig, ax = plt.subplots(facecolor='black')
ax.set_facecolor('black')
im = ax.imshow(masked_u, cmap=cmap, vmin=-0.1, vmax=0.1,
               extent=extent, origin='lower', animated=True)

# Draw polygon boundary
polygon = plt.Polygon(vertices, edgecolor='white', fill=False, linewidth=0.8)
ax.add_patch(polygon)
ax.axis('off')

# Update function for animation
def update(frame):
    global u_prev, u_curr, u_next
    # Compute Laplacian using finite differences
    laplacian = (
        np.roll(u_curr, 1, axis=0) + np.roll(u_curr, -1, axis=0) +
        np.roll(u_curr, 1, axis=1) + np.roll(u_curr, -1, axis=1) -
        4 * u_curr
    ) / dx**2

    # Update wave equation
    u_next = 2 * u_curr - u_prev + (c * dt)**2 * laplacian
    u_next *= mask
    u_prev, u_curr = u_curr, u_next

    im.set_array(np.ma.masked_where(~mask, u_curr))
    return [im]

# Run animation
ani = animation.FuncAnimation(fig, update, frames=steps, interval=30, blit=False)
ani.save('wave_hexagon.mp4', writer='ffmpeg', fps=30, dpi=300)

plt.show()
