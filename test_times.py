from times import compute_overlap_time, time_range
import pytest


@pytest.mark.parametrize("range1, range2, expected", [
    (
        {"start": "2010-01-12 10:00:00", "end": "2010-01-12 12:00:00", "intervals": 1, "gap": 0},
        {"start": "2010-01-12 10:30:00", "end": "2010-01-12 10:45:00", "intervals": 2, "gap": 60},
        [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
    ),
    (
        {"start": "2022-01-01 08:00:00", "end": "2022-01-01 09:00:00", "intervals": 1, "gap": 0},
        {"start": "2022-01-01 10:00:00", "end": "2022-01-01 11:00:00", "intervals": 1, "gap": 0},
        []
    ),
    (
        {"start": "2022-01-01 08:00:00", "end": "2022-01-01 12:00:00", "intervals": 4, "gap": 0},
        {"start": "2022-01-01 09:15:00", "end": "2022-01-01 11:45:00", "intervals": 3, "gap": 0},
        [
            ('2022-01-01 09:15:00', '2022-01-01 10:00:00'),
            ('2022-01-01 10:00:00', '2022-01-01 10:05:00'),
            ('2022-01-01 10:05:00', '2022-01-01 10:55:00'),
            ('2022-01-01 10:55:00', '2022-01-01 11:00:00'),
            ('2022-01-01 11:00:00', '2022-01-01 11:45:00')
        ]
    ),
    (
        {"start": "2022-01-01 08:00:00", "end": "2022-01-01 10:00:00", "intervals": 1, "gap": 0},
        {"start": "2022-01-01 10:00:00", "end": "2022-01-01 12:00:00", "intervals": 1, "gap": 0},
        []
    )
])
def test_overlap(range1, range2, expected):
    r1 = time_range(range1["start"], range1["end"], range1["intervals"], range1["gap"])
    r2 = time_range(range2["start"], range2["end"], range2["intervals"], range2["gap"])
    result = compute_overlap_time(r1, r2)
    assert result == expected

def test_invalid_time_range():
    with pytest.raises(ValueError):
        time_range("2022-01-01 12:00:00", "2022-01-01 10:00:00")
