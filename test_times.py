from times import compute_overlap_time, time_range
import pytest

def test_given_input():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    result = compute_overlap_time(large, short)
    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
    assert result == expected

def test_no_overlap():
    range1 = time_range("2022-01-01 08:00:00", "2022-01-01 09:00:00")
    range2 = time_range("2022-01-01 10:00:00", "2022-01-01 11:00:00")
    result = compute_overlap_time(range1, range2)
    expected = []
    assert result == expected

def test_many_intervals():
    range1 = time_range("2022-01-01 08:00:00", "2022-01-01 12:00:00", 4)
    range2 = time_range("2022-01-01 09:15:00", "2022-01-01 11:45:00", 3)
    result = compute_overlap_time(range1, range2)
    expected = [('2022-01-01 09:15:00', '2022-01-01 10:00:00'),
                ('2022-01-01 10:00:00', '2022-01-01 10:05:00'),
                ('2022-01-01 10:05:00', '2022-01-01 10:55:00'), 
                ('2022-01-01 10:55:00', '2022-01-01 11:00:00'), 
                ('2022-01-01 11:00:00', '2022-01-01 11:45:00')]
    print("Result:", result)
    assert result == expected

def test_edge_case_overlap():
    range1 = time_range("2022-01-01 08:00:00", "2022-01-01 10:00:00")
    range2 = time_range("2022-01-01 10:00:00", "2022-01-01 12:00:00")
    result = compute_overlap_time(range1, range2)
    expected = []
    assert result == expected

def test_invalid_time_range():
    with pytest.raises(ValueError):
        time_range("2022-01-01 12:00:00", "2022-01-01 10:00:00")
