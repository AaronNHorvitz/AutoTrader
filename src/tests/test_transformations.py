# src/tests/test_transformations.py

import numpy as np
import pandas as pd
from src.statistics.transformations import (
    check_positive,
    log_transform,
    difference,
    log_difference,
)

# Test check_positive with positive series (should pass without error).
def test_check_positive():
    positive_series = pd.Series([1, 2, 3])
    negative_series = pd.Series([1, -1, 2])
    zero_series = pd.Series([1, 0, 2])

    check_positive(positive_series)

    for series in [negative_series, zero_series]:
        try:
            check_positive(series)
        except ValueError as e:
            assert str(e) == "Series must contain only positive values."
        else:
            assert False, "check_positive failed to detect non-positive values."


# Test log_transform correctness.
def test_log_transform():
    series = pd.Series([1, np.e, np.e**2])
    result = log_transform(series)
    expected = pd.Series([0, 1, 2])
    assert np.allclose(result, expected, atol=1e-5), "log_transform function incorrect."


# Test log_transform with non-positive input (should raise error).
def test_log_transform_with_non_positive_values():
    series = pd.Series([1, 0, 2])
    try:
        log_transform(series)
    except ValueError as e:
        assert str(e) == "Series must contain only positive values."
    else:
        assert False, "log_transform did not raise ValueError for non-positive input."


# Test basic difference functionality.
def test_difference():
    series = pd.Series([1, 3, 6, 10])
    result = difference(series)
    expected = pd.Series([2, 3, 4], index=[1, 2, 3])
    assert np.allclose(result, expected), "difference function incorrect."


# Test difference with specified periods.
def test_difference_with_periods():
    series = pd.Series([1, 2, 4, 7, 11])
    result = difference(series, periods=2)
    expected = pd.Series([3, 5, 7], index=[2, 3, 4])
    assert np.allclose(result, expected), "difference function with periods incorrect."


# Test log_difference functionality.
def test_log_difference():
    series = pd.Series([1, np.e, np.e**2, np.e**3])
    result = log_difference(series)
    expected = pd.Series([1.0, 1.0, 1.0], index=[1, 2, 3])
    assert np.allclose(result, expected), "log_difference function incorrect."


# Test log_difference with non-positive input.
def test_log_difference_non_positive():
    series = pd.Series([1, 0, 2])
    try:
        log_difference(series)
    except ValueError as e:
        assert str(e) == "Series must contain only positive values."
    else:
        assert False, "log_difference did not raise ValueError for non-positive input."


# Test log_difference on a short series (single-value series).
def test_log_difference_short_series():
    series = pd.Series([100])
    result = log_difference(series)
    assert result.empty, "log_difference with single-value series should return empty."


if __name__ == "__main__":
    test_check_positive()
    test_log_transform()
    test_log_transform_with_non_positive_values()
    test_difference()
    test_difference_with_periods()
    test_log_difference()
    test_log_difference_non_positive()
    test_log_difference_short_series()
    print("✅ All transformation tests passed successfully!")
