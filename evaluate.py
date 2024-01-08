import torch
import numpy as np
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from model import NeuralNet
from nltk_utils import tokenize, bag_of_words
from train import ChatDataset  # Assuming you have defined ChatDataset in your train.py

# Define batch_size
batch_size = 8  # or any value you want to use for testing

# Load your trained model
data = torch.load("data.pth")
model_state = data["model_state"]
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

# Load your test data and labels
test_dataset = ChatDataset()  # Assuming you have implemented the ChatDataset class for your test data
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

all_predictions = []
all_labels = []

with torch.no_grad():
    for (words, labels) in test_loader:
        outputs = model(words)
        _, predicted = torch.max(outputs, 1)

        all_predictions.extend(predicted.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# Convert lists to numpy arrays for easier calculations
true_labels = np.array(all_labels)
predicted_labels = np.array(all_predictions)

# Calculate metrics
accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels, average='weighted')
recall = recall_score(true_labels, predicted_labels, average='weighted')
f1 = f1_score(true_labels, predicted_labels, average='weighted')
conf_matrix = confusion_matrix(true_labels, predicted_labels)

# Print metrics
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print(f"Confusion Matrix:\n{conf_matrix}")