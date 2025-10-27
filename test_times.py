from times import compute_overlap_time, time_range
import pytest
import yaml

def load_fixtures():
    with open("fixture.yml", "r") as f:
        data = yaml.safe_load(f)
    cases = []
    for item in data:
        for name, case in item.items():
            range1 = case["time_range_1"]
            range2 = case["time_range_2"]
            expected = [tuple(e) for e in case["expected"]] if case["expected"] else []
            cases.append((range1, range2, expected))
    return cases

@pytest.mark.parametrize("range1, range2, expected", load_fixtures())
def test_overlap(range1, range2, expected):
    r1 = time_range(range1["start"], range1["end"], range1["intervals"], range1["gap"])
    r2 = time_range(range2["start"], range2["end"], range2["intervals"], range2["gap"])
    result = compute_overlap_time(r1, r2)
    assert result == expected

def test_invalid_time_range():
    with pytest.raises(ValueError):
        time_range("2022-01-01 12:00:00", "2022-01-01 10:00:00")
