import csv
import re
import math
from collections import Counter

from sklearn.model_selection import GroupShuffleSplit
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def extract_features(text):
    characters = [c for c in text if not c.isspace()]
    words = text.split()

    zero_width_chars = ["\u200b", "\u200c", "\u200d", "\ufeff"]
    zero_width_count = sum(text.count(c) for c in zero_width_chars)
    tatweel_count = text.count("ـ")

    return {
        "character_count": len(characters),
        "word_count": len(words),
        "average_word_length": (
            sum(len(w) for w in words) / len(words) if words else 0
        ),
        "tatweel_count": tatweel_count,
        "zero_width_count": zero_width_count,
        "format_char_count": sum(
            1 for c in text if c in["\u200b", "\u200c", "\u200d", "\ufeff"]
        ),
        "unique_char_ratio": (
            len(set(characters)) / len(characters) if characters else 0
        )
    }

# Read dataset
texts = []
labels = []
groups = []

with open("arabic_dataset.csv", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    for row in reader:
        texts.append(row["text"])
        labels.append(int(row["label"]))
        groups.append(row["base_id"])

# Extract features
X = [extract_features(text) for text in texts]

# Split by original sentence to avoid data leakage
splitter = GroupShuffleSplit(
    n_splits=1, test_size=0.30, random_state=42
)
train_index, test_index = next(
    splitter.split(X, labels, groups)
)

X_train = [X[i] for i in train_index]
X_test = [X[i] for i in test_index]
y_train = [labels[i] for i in train_index]
y_test = [labels[i] for i in test_index]

# Build and train model
model = Pipeline([
    ("vectorizer", DictVectorizer()),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    ))
])

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)

print("\n===== MODEL RESULTS =====")
print("Training samples:", len(train_index))
print("Testing samples:", len(test_index))
print("Accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(
    y_test, predictions,
    target_names=["Normal", "Suspicious"],
    zero_division=0
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))


# Draw and save Confusion Matrix
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score

cm = confusion_matrix(y_test, predictions)

plt.figure(figsize=(6, 5))
plt.imshow(cm, cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.xticks([0, 1], ["Normal", "Suspicious"])
plt.yticks([0, 1], ["Normal", "Suspicious"])

for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i, j], ha="center", va="center")

plt.colorbar()
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()

# Draw model performance chart
metrics = [
    precision_score(y_test, predictions, zero_division=0),
    recall_score(y_test, predictions, zero_division=0),
    f1_score(y_test, predictions, zero_division=0)
]

plt.figure(figsize=(7, 5))
plt.bar(["Precision", "Recall", "F1-score"], metrics)
plt.ylim(0, 1.1)
plt.title("Model Performance")
plt.ylabel("Score")
plt.savefig("model_performance.png")
plt.close()

print("\nCharts saved successfully!")
print("confusion_matrix.png")
print("model_performance.png")
# Save evaluation results
with open("results.txt", "w", encoding="utf-8") as file:
    file.write("Arabic Text Steganalysis - Model Results\n")
    file.write("Model: Random Forest\n")
    file.write(f"Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%\n")
    file.write(f"Training Samples: {len(train_index)}\n")
    file.write(f"Testing Samples: {len(test_index)}\n")
    file.write(f"Confusion Matrix:\n{cm}\n")
    file.write("\nClassification Report:\n")
    file.write(classification_report(
        y_test, predictions,
        target_names=["Normal", "Suspicious"],
        zero_division=0
    ))

print("Results saved to results.txt")