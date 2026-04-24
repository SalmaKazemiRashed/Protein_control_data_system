import numpy as np
import time

## This is for just a random synthetic protein scattering data
def generate_data():
    angle = np.random.uniform(0, 180)

    # Protein-like scattering curve
    intensity = 1000 * np.exp(-((angle - 60) ** 2) / 400)

    # Noise
    intensity += np.random.normal(0, 40)

    # Inject anomaly
    if np.random.rand() < 0.05:
        intensity += np.random.uniform(500, 1200)

    return {
        "angle": float(angle),
        "intensity": float(intensity),
        "timestamp": time.time()
    }