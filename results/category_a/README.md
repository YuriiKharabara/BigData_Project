# Category A Results

This directory contains the results of various API calls for Category A. Each subdirectory represents a specific API endpoint and contains the results of different parameter values.

### Explanation of Each Subdirectory

Each subdirectory corresponds to a specific parameter value (`n`) used in the API call. Within each subdirectory, there are multiple images showing the results of the API call with that parameter.

### get_hourly_aggregated_stats

- **param_n_0**: Results for `{ "n": 0 }` - Empty results.
  - `image.png`: Snapshot of the empty result.
- **param_n_1**: Results for `{ "n": 1 }` - Last 1 hour.
  - `image.png`: Snapshot of the result for the last 1 hour.
- **param_n_3**: Results for `{ "n": 3 }` - Last 3 hours.
  - `image_0_time_range.png`: Snapshot of the first hour.
  - `image_1_time_range.png`: Snapshot of the second hour.
  - `image_2_time_range.png`: Snapshot of the third hour.
- **param_n_6**: Results for `{ "n": 6 }` - Last 6 hours (only 4 hours of data available, so it includes the earliest known data).
  - `image_0_time_range.png`: Snapshot of the first hour.
  - `image_1_time_range.png`: Snapshot of the second hour.
  - `image_2_time_range.png`: Snapshot of the third hour.
  - `image_3_time_range.png`: Snapshot of the fourth hour.

### get_bot_created_pages_stats

- **param_n_0**: Results for `{ "n": 0 }` - Empty results.
  - `param_n_0.png`: Snapshot of the empty result.
- **param_n_1**: Results for `{ "n": 1 }` - Last 1 hour.
  - `param_n_1.png`: Snapshot of the result for the last 1 hour.
- **param_n_3**: Results for `{ "n": 3 }` - Last 3 hours.
  - `param_n_3.png`: Snapshot of the result for the last 3 hours.

### get_top_users

- **param_n_0**: Results for `{ "n": 0 }` - Empty results.
  - `param_n_0.png`: Snapshot of the empty result.
- **param_n_1**: Results for `{ "n": 1 }` - Last 1 hour.
  - `image_1_place.png`: Snapshot of the user in 1st place.
  - `image_20_place.png`: Snapshot of the user in 20th place.
  - `image_2_place.png`: Snapshot of the user in 2nd place.
- **param_n_3**: Results for `{ "n": 3 }` - Last 3 hours.
  - `image_1_place.png`: Snapshot of the user in 1st place.
  - `image_20_place.png`: Snapshot of the user in 20th place.
  - `image_2_place.png`: Snapshot of the user in 2nd place.
- **param_n_6**: Results for `{ "n": 6 }` - Last 6 hours (only 4 hours of data available, so it includes the earliest known data).
  - `image_1_place.png`: Snapshot of the user in 1st place.
  - `image_20_place.png`: Snapshot of the user in 20th place.
  - `image_2_place.png`: Snapshot of the user in 2nd place.

Each image represents the API response for the given parameter value.