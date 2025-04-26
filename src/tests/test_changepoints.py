#src/tests/test_changepoints.py

import numpy as np
import pandas as pd
from src.statistics.changepoints import detect_level_shifts

def test_detect_level_shifts_with_known_shift():
    # Simulate series with clear shift at index 100
    np.random.seed(42)
    series = pd.Series(np.concatenate([
        np.random.normal(loc=0, scale=1, size=100),
        np.random.normal(loc=10, scale=1, size=100)
    ]))

    shifts = detect_level_shifts(series, penalty=5)
    
    assert len(shifts) == 1, f"Expected 1 shift, got {len(shifts)}"
    assert 95 <= shifts[0] <= 105, f"Shift detection inaccurate: found at {shifts[0]}"

def test_detect_level_shifts_no_shift():
    # Simulate stationary series (no shifts)
    np.random.seed(42)
    series = pd.Series(np.random.normal(loc=0, scale=1, size=200))
    
    shifts = detect_level_shifts(series, penalty=5)
    
    assert len(shifts) == 0, f"Expected no shifts, got {len(shifts)}"

def test_detect_level_shifts_short_series():
    # Short series less than min_size
    series = pd.Series([1, 2, 1, 2, 1])

    shifts = detect_level_shifts(series, penalty=1, min_size=10)
    
    assert len(shifts) == 0, f"Expected no shifts for short series, got {len(shifts)}"

if __name__ == "__main__":
    test_detect_level_shifts_with_known_shift()
    test_detect_level_shifts_no_shift()
    test_detect_level_shifts_short_series()
    print("All changepoint tests passed successfully!")
