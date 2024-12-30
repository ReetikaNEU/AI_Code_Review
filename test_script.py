import json

# Load the test dataset
with open("test_dataset_augmented.json", "r") as f:
    test_data = json.load(f)

# Initialize counters for auxiliary features
num_lines = []
nested_if_count = []
loop_count = []

# Loop through the dataset to extract auxiliary features
for item in test_data:
    num_lines.append(item.get("num_lines", 0))
    nested_if_count.append(item.get("nested_if_count", 0))
    loop_count.append(item.get("loop_count", 0))

# Print distribution
print(f"Number of samples: {len(test_data)}")
print(f"Avg. num_lines: {sum(num_lines) / len(num_lines):.2f}, Min: {min(num_lines)}, Max: {max(num_lines)}")
print(f"Avg. nested_if_count: {sum(nested_if_count) / len(nested_if_count):.2f}, Min: {min(nested_if_count)}, Max: {max(nested_if_count)}")
print(f"Avg. loop_count: {sum(loop_count) / len(loop_count):.2f}, Min: {min(loop_count)}, Max: {max(loop_count)}")



