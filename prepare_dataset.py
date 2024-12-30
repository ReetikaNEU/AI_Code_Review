from datasets import load_dataset
import json
from collections import Counter
import random  # For balancing the dataset
import re

def compute_complexity_tags(code):
    """
    Extract complexity tags for a given code snippet.
    """
    # Count the number of lines
    num_lines = len(code.split("\n"))

    # Count the number of nested 'if' statements
    nested_if_count = len(re.findall(r"\bif\b", code))

    # Count the number of loops (for, while)
    loop_count = len(re.findall(r"\b(for|while)\b", code))

    # Return tags as a dictionary
    return {
        "num_lines": num_lines,
        "nested_if_count": nested_if_count,
        "loop_count": loop_count
    }

def print_label_distribution(dataset, dataset_name):
    labels = [sample["label"] for sample in dataset]
    label_counts = Counter(labels)
    print(f"Label distribution in {dataset_name}: {label_counts}")

def balance_dataset(dataset):
    """
    Balances the dataset by undersampling the majority class.
    """
    false_samples = [sample for sample in dataset if sample["label"] == False]
    true_samples = [sample for sample in dataset if sample["label"] == True]

    # Undersample majority class (False) to match the minority class (True)
    false_samples = random.sample(false_samples, len(true_samples))

    # Combine and shuffle
    balanced_dataset = false_samples + true_samples
    random.shuffle(balanced_dataset)
    return balanced_dataset

def augment_code(code):
    """
    Apply transformations to the code for data augmentation.
    """
    # Example: Replace '==' with '!=' (only for augmentation purposes)
    code = code.replace("==", "!=")
    # Add more transformations as needed
    return code

def augment_dataset(dataset):
    """
    Augment the dataset by applying code transformations for diversity.
    """
    augmented_dataset = []
    for sample in dataset:
        if "code" not in sample:
            print("Skipping sample without 'code' field:", sample)
            continue
        augmented_sample = sample.copy()
        augmented_sample["code"] = augment_code(sample["code"])
        augmented_dataset.append(augmented_sample)
    return augmented_dataset

def load_defect_detection_dataset():
    """
    Load and preprocess the CodeXGLUE Defect Detection dataset.
    """
    # Load the dataset from the CodeXGLUE benchmark
    dataset = load_dataset("code_x_glue_cc_defect_detection")
    train_data = dataset["train"]
    valid_data = dataset["validation"]
    test_data = dataset["test"]  # Add the test dataset

    # Convert datasets to a format suitable for the Hugging Face Trainer
    train_dataset = [
        {
            "code": sample.get("func", ""),  # Use a default value if "func" is missing
            "label": sample["target"],
            **compute_complexity_tags(sample.get("func", ""))
        }
        for sample in train_data
    ]
    valid_dataset = [
        {
            "code": sample.get("func", ""),  # Use a default value if "func" is missing
            "label": sample["target"],
            **compute_complexity_tags(sample.get("func", ""))
        }
        for sample in valid_data
    ]
    test_dataset = [
        {
            "code": sample.get("func", ""),  # Use a default value if "func" is missing
            "label": sample["target"],
            **compute_complexity_tags(sample.get("func", ""))
        }
        for sample in test_data
    ]

    # Debugging: Print a sample from the dataset
    print("Sample from train_dataset before augmentation:", train_dataset[0])

    # Augment the training dataset
    train_dataset = augment_dataset(train_dataset)

    # Balance the training dataset
    train_dataset = balance_dataset(train_dataset)

    # Print label distribution for debugging
    print_label_distribution(train_dataset, "Balanced Training Dataset")
    print_label_distribution(valid_dataset, "Validation Dataset")
    print_label_distribution(test_dataset, "Test Dataset")

    return train_dataset, valid_dataset, test_dataset

def save_test_dataset_to_json():
    """
    Save the test dataset to a JSON file for evaluation purposes.
    """
    _, _, test_dataset = load_defect_detection_dataset()
    with open("test_dataset_augmented.json", "w") as f:
        json.dump(test_dataset, f, indent=4)
    print(f"Test dataset saved to test_dataset_augmented.json with {len(test_dataset)} samples.")

if __name__ == "__main__":
    # Load datasets
    train_dataset, valid_dataset, test_dataset = load_defect_detection_dataset()

    # Save the updated datasets
    with open("train_dataset_augmented.json", "w") as f:
        json.dump(train_dataset, f, indent=4)
    with open("valid_dataset_augmented.json", "w") as f:
        json.dump(valid_dataset, f, indent=4)
    with open("test_dataset_augmented.json", "w") as f:
        json.dump(test_dataset, f, indent=4)

    print("Augmented datasets saved with additional complexity tags.")