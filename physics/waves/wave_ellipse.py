import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
Nx, Ny = 600, 600  # Grid size
dx = dy = 3.0      # Spatial resolution
c = 3.0            # Wave speed
dt = 0.5           # Time step
steps = 5000       # Number of time steps

# Stability condition
alpha = c * dt / dx
if alpha >= 1 / np.sqrt(2):
    raise ValueError("Stability condition violated: reduce dt or increase dx.")

# Create coordinate grid centered at (0, 0)
x = dx * (np.arange(Nx) - Nx // 2)
y = dy * (np.arange(Ny) - Ny // 2)
X, Y = np.meshgrid(x, y)

# Define elliptical mask
a = 850  # semi-major axis length (x-direction)
b = 650  # semi-minor axis length (y-direction)
mask = (X**2 / a**2 + Y**2 / b**2) <= 1

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
contour = ax.contour(X, Y, mask.astype(float), levels=[0.5], colors='white', linewidths=0.8)
#ax.set_title("2D Wave Propagation in an Elliptical Domain", color='white')
ax.axis('off')

def update(frame):
    global u_prev, u_curr, u_next
    # Compute Laplacian using finite differences
    laplacian = (
        np.roll(u_curr, 1, axis=0) + np.roll(u_curr, -1, axis=0) +
        np.roll(u_curr, 1, axis=1) + np.roll(u_curr, -1, axis=1) -
        4 * u_curr
    ) / dx**2

    u_next = 2 * u_curr - u_prev + (c * dt)**2 * laplacian
    u_next *= mask
    u_prev, u_curr = u_curr, u_next
  
    im.set_array(np.ma.masked_where(~mask, u_curr))
    return [im]

ani = animation.FuncAnimation(fig, update, frames=steps, interval=30, blit=False)
ani.save('wave_ellipse.mp4', writer='ffmpeg', fps=30, dpi=300)

plt.show()
