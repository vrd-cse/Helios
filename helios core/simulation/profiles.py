import numpy as np
from config import TOTAL_HOURS
np.random.seed(42)  # For reproducibility   
def generate_profiles():
    hours = np.arange(TOTAL_HOURS)
    solar = np.maximum(0 , 25*np.sin((hours - 6) * np.pi / 12)) 
    demand = 20 + 10 *np.sin((hours - 18) * np.pi/12) + 10 * np.random.rand(TOTAL_HOURS)
    return hours , solar,demand
