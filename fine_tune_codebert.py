from transformers import RobertaTokenizer, TrainingArguments, Trainer, RobertaModel, RobertaPreTrainedModel
import torch
import torch.nn as nn
from torch.utils.data import Dataset
from prepare_dataset import load_defect_detection_dataset
from transformers import RobertaForSequenceClassification

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class CodeDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=256):  # Reduced max length
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
        inputs["auxiliary_features"] = torch.tensor(
            [
                item.get("num_lines", 0),
                item.get("nested_if_count", 0),
                item.get("loop_count", 0)
            ],
            dtype=torch.float32
        )
        return inputs


class RobertaWithoutAuxiliaryFeatures(RobertaForSequenceClassification):
    def __init__(self, config):
        super().__init__(config)


def fine_tune_codebert():
    # Load datasets
    train_dataset, valid_dataset, _ = load_defect_detection_dataset()

    # Reduce dataset size for faster training
    train_dataset = train_dataset[:2000]  # Using 2000 samples for training
    valid_dataset = valid_dataset[:500]  # Using 500 samples for validation

    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    model = RobertaWithoutAuxiliaryFeatures.from_pretrained("microsoft/codebert-base", num_labels=2)
    model.to(device)

    train_data = CodeDataset(train_dataset, tokenizer)
    valid_data = CodeDataset(valid_dataset, tokenizer)

    # Training arguments with corrected evaluation and save strategy
    training_args = TrainingArguments(
    output_dir="./fine_tuned_codebert_with_aux",
    evaluation_strategy="epoch",  # Match evaluation and save strategy
    save_strategy="epoch",  # Save model at the end of every epoch
    learning_rate=2e-5,
    per_device_train_batch_size=4,  # Smaller batch size for memory efficiency
    num_train_epochs=3,  # Reduced epochs for testing
    weight_decay=0.01,
    load_best_model_at_end=True,  # Load the best model based on validation metrics
    logging_dir="./logs",
    logging_steps=10,
    gradient_accumulation_steps=2,  # Simulating a larger batch size
    fp16=True,  # Enable mixed precision
    dataloader_num_workers=2,  # Use 2 workers to load data faster
    report_to="none"  # Disable W&B integration
)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=valid_data,
        tokenizer=tokenizer
    )

    # Start training
    print("Starting training...")
    trainer.train()

    # Save the fine-tuned model
    model.save_pretrained("./fine_tuned_codebert_with_aux")
    tokenizer.save_pretrained("./fine_tuned_codebert_with_aux")
    print("Fine-tuned model saved successfully!")


if __name__ == "__main__":
    fine_tune_codebert()