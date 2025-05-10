import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from scipy.ndimage import binary_dilation, generate_binary_structure

# Simulation parameters
Nx, Ny = 600, 600
maze_width, maze_height = 20, 20 
scale_factor = 20

dx = dy = 3.0
c = 3.0
dt = 0.5
steps = 5000

alpha = c * dt / dx
if alpha >= 1 / np.sqrt(2):
    raise ValueError("Stability condition violated.")

# Generate maze
def generate_maze(width, height, sparsity=0.0):
    maze = np.ones((height * 2 + 1, width * 2 + 1), dtype=bool)
    visited = np.zeros((height, width), dtype=bool)

    def carve(x, y, prev_dir=None):
        visited[y, x] = True
        maze[y * 2 + 1, x * 2 + 1] = False

        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(dirs)

        for dx_, dy_ in dirs:
            nx, ny = x + dx_, y + dy_
            mx, my = x * 2 + 1 + dx_, y * 2 + 1 + dy_
            if 0 <= nx < width and 0 <= ny < height and not visited[ny, nx]:
                if prev_dir and (dx_, dy_) == prev_dir and random.random() < 0.5:
                    continue
                maze[my, mx] = False
                carve(nx, ny, (dx_, dy_))

    carve(0, 0)

    # Add sparsity: randomly remove walls
    if sparsity > 0.0:
        wall_positions = np.argwhere(maze == True)
        inner_walls = [pos for pos in wall_positions if 0 < pos[0] < maze.shape[0]-1 and 0 < pos[1] < maze.shape[1]-1]
        random.shuffle(inner_walls)
        to_clear = int(len(inner_walls) * sparsity)
        for y, x in inner_walls[:to_clear]:
            maze[y, x] = False

    return ~maze  # Invert so True = open path

# Create maze mask and upscale
maze = generate_maze(maze_width, maze_height)
maze_mask = np.kron(maze, np.ones((scale_factor, scale_factor), dtype=bool))
maze_mask = maze_mask[:Ny, :Nx]

def create_wave_mask(maze_mask):
    wave_mask = np.copy(maze_mask)
    reachable = np.zeros_like(maze_mask, dtype=bool)

    edges = [
        (0, slice(None)), (Ny-1, slice(None)),
        (slice(None), 0), (slice(None), Nx-1)
    ]

    for edge in edges:
        open_edge = np.argwhere(maze_mask[edge])
        for idx in open_edge:
            pos = [edge[0], edge[1]]
            if isinstance(pos[0], int):
                y, x = pos[0], idx[0]
            else:
                y, x = idx[0], pos[1]
            reachable[y, x] = True

    structure = generate_binary_structure(2, 1)
    prev = np.zeros_like(reachable)
    while not np.array_equal(reachable, prev):
        prev = reachable.copy()
        reachable |= binary_dilation(reachable, structure) & maze_mask

    return reachable

wave_mask = create_wave_mask(maze_mask)

# Coordinate grid
x = dx * (np.arange(Nx) - Nx // 2)
y = dy * (np.arange(Ny) - Ny // 2)
X, Y = np.meshgrid(x, y)

# Wave fields
u_prev = np.zeros((Ny, Nx))
u_curr = np.zeros((Ny, Nx))
u_next = np.zeros((Ny, Nx))

# Initial Gaussian pulse
sigma = 50.0
u_curr += np.exp(-((X)**2 + (Y)**2) / (2 * sigma**2)) * wave_mask

# Setup plot
masked_u = np.ma.masked_where(~wave_mask, u_curr)
cmap = plt.cm.plasma.copy()
cmap.set_bad(color='black')

extent = [x.min(), x.max(), y.min(), y.max()]
fig, ax = plt.subplots(facecolor='black')
ax.set_facecolor('black')

im = ax.imshow(masked_u, cmap='plasma', vmin=-0.1, vmax=0.1,
               extent=extent, origin='lower', animated=True)

# Draw maze
maze_outline = np.logical_not(maze_mask)
ax.contour(maze_outline.astype(float), levels=[0.5], colors='white',
           linewidths=0.5, extent=extent, origin='lower')

ax.axis('off')

# Update function
def update(frame):
    global u_prev, u_curr, u_next
    laplacian = (
        np.roll(u_curr, 1, axis=0) + np.roll(u_curr, -1, axis=0) +
        np.roll(u_curr, 1, axis=1) + np.roll(u_curr, -1, axis=1) -
        4 * u_curr
    ) / dx**2

    u_next = 2 * u_curr - u_prev + (c * dt)**2 * laplacian
    u_next *= wave_mask

    u_prev, u_curr = u_curr, u_next
    masked = np.ma.masked_where((~wave_mask) | (np.abs(u_curr) < 1e-4), u_curr)
    im.set_array(masked)

    return [im]

ani = animation.FuncAnimation(fig, update, frames=steps, interval=30, blit=False)
ani.save('wave_maze_escape.mp4', writer='ffmpeg', fps=30, dpi=300)

plt.show()
