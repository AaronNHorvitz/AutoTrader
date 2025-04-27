# src/statistics/changepoints.py

import numpy as np
import pandas as pd
import ruptures as rpt
from ruptures.exceptions import BadSegmentationParameters

def detect_level_shifts(series, model="l2", penalty=3, min_size=30):
    """
    Detect level shifts (changepoints) in a time series using the ruptures library.

    Parameters
    ----------
    series : pd.Series or np.array
        Input time series data for detecting level shifts.

    model : {'l1', 'l2', 'rbf', 'linear', 'normal'}, optional, default='l2'
        The cost model used by ruptures to detect shifts:
        - 'l1': Robust to outliers, based on absolute deviations.
        - 'l2': Detects shifts in the mean, using squared deviations (recommended for mean shifts).
        - 'rbf': Detects shifts in the distribution (useful for variance or general distributional shifts).
        - 'linear': Detects shifts in linear trends.
        - 'normal': Detects shifts assuming a normal distribution (both mean and variance).

    penalty : int or float, optional, default=3
        Penalty value controlling sensitivity to changes:
        - Higher penalty → fewer detected changepoints.
        - Lower penalty → more sensitivity, more shifts detected.

    min_size : int, optional, default=30
        The minimum number of observations between consecutive changepoints.

    Returns
    -------
    list[int]
        Indices of detected level shifts, excluding the final index (series endpoint).

    Examples
    --------
    >>> from src.statistics.changepoints import detect_level_shifts
    >>> import pandas as pd
    >>> series = pd.Series([1]*50 + [10]*50)
    >>> detect_level_shifts(series, model='l2', penalty=5)
    [50]

    Notes
    -----
    Adjusting the `penalty` and `min_size` parameters can help fine-tune the detection process:
    - A lower `penalty` captures subtle shifts but may introduce false positives.
    - A higher `penalty` reduces false positives but might miss genuine shifts.
    """
    if len(series) < min_size:
        # Series is too short for detection
        return []

    try:
        algo = rpt.Pelt(model=model, min_size=min_size)
        detected_points = algo.fit(series.values).predict(pen=penalty)
        return detected_points[:-1]  # Exclude end-point
    except BadSegmentationParameters:
        # Handle cases where segmentation isn't possible
        return []

