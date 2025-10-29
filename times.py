import datetime
import requests
import json
#from config import API_KEY # Uncomment this line if you have a config.py with your API key
API_KEY = 0 # Placeholder API key for testing purposes

def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    if start_time >= end_time:
        raise ValueError("start_time must be earlier than end_time")
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]

def iss_passes(latitude, longitude):
    url = f"https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/{latitude}/{longitude}/0/5/50&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        passes = response.json().get("passes", [])
        passes_times = [
            (
                datetime.datetime.fromtimestamp(p["startUTC"], datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"),
                datetime.datetime.fromtimestamp(p["endUTC"], datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
            )
            for p in passes
        ]
        return passes_times
    else:
        return {"error": "Failed to retrieve data"}


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2) # This code should also check that low < high, but the test does not cover that case.
            high = min(end1, end2)
            if low < high:
                overlap_time.append((low, high))
    return overlap_time

if __name__ == "__main__":
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    print(compute_overlap_time(large, short))

    print("ISS Passes:")
    print(iss_passes(51.5074, -0.1278))  # Coordinates for London
