import json
import torch
from transformers import RobertaTokenizer
from fine_tune_codebert import RobertaWithoutAuxiliaryFeatures
from torch.utils.data import DataLoader, Dataset

# model_path = "./fine_tuned_codebert_with_auxnew/checkpoint-250"
model_path = "./fine_tuned_codebert/checkpoint-2504"
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = RobertaWithoutAuxiliaryFeatures.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

class TestCodeDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        inputs = self.tokenizer(
            item["code"],
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        )
        inputs = {key: val.squeeze(0) for key, val in inputs.items()}
        inputs["labels"] = torch.tensor(item["label"], dtype=torch.long)
        return inputs

with open("test_dataset_augmented_filtered.json", "r") as f:
    test_data = json.load(f)

test_data = test_data[:500]
test_dataset = TestCodeDataset(test_data, tokenizer)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

model.eval()
correct = 0
total = 0
wrong_predictions = []

with torch.no_grad():
    for batch in test_loader:
        inputs = {key: val.to(device) for key, val in batch.items() if key != "labels"}
        labels = batch["labels"].to(device)
        outputs = model(**inputs)  # No 'auxiliary_features'
        predicted_labels = torch.argmax(outputs["logits"], dim=1)
        correct += (predicted_labels == labels).sum().item()
        total += labels.size(0)

        for i in range(len(labels)):
            if predicted_labels[i] != labels[i]:
                wrong_predictions.append({
                    "code": test_data[total - len(labels) + i]["code"],
                    "true_label": labels[i].item(),
                    "predicted_label": predicted_labels[i].item()
                })

accuracy = correct / total
print(f"Test Accuracy: {accuracy * 100:.2f}%")

with open("wrong_predictions.json", "w") as f:
    json.dump(wrong_predictions, f, indent=4)
    print(f"Misclassified examples saved to wrong_predictions.json")