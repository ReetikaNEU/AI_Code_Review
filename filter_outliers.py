import json

# Define capping thresholds
NUM_LINES_THRESHOLD = 500
NESTED_IF_THRESHOLD = 50
LOOP_COUNT_THRESHOLD = 10

# Load the dataset
with open("test_dataset_augmented.json", "r") as f:
    test_data = json.load(f)

# Apply capping
for item in test_data:
    item["num_lines"] = min(item.get("num_lines", 0), NUM_LINES_THRESHOLD)
    item["nested_if_count"] = min(item.get("nested_if_count", 0), NESTED_IF_THRESHOLD)
    item["loop_count"] = min(item.get("loop_count", 0), LOOP_COUNT_THRESHOLD)

# Save the updated dataset
with open("test_dataset_augmented_filtered.json", "w") as f:
    json.dump(test_data, f, indent=4)

print("Filtered dataset saved as test_dataset_augmented_filtered.json")