# src/statistics/changepoints.py

import numpy as np
import pandas as pd
import ruptures as rpt
from ruptures.exceptions import BadSegmentationParameters

def detect_level_shifts(series, model="l2", penalty=3, min_size=30):
    """
    Detect level shifts (mean changes) using ruptures library.

    Parameters
    ----------
    series : pd.Series or np.array
        Input time series data.
    model : str, optional
        Model used by ruptures ('l2' recommended for mean shifts), default is 'l2'.
    penalty : int or float, optional
        Penalty value influencing the number of changepoints detected (higher penalty = fewer shifts).
    min_size : int, optional
        Minimum number of observations between detected changepoints.

    Returns
    -------
    list[int]
        Indices of detected level shifts (excluding the last index).
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

