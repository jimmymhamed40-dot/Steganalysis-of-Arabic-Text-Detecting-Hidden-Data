import re
import math
from collections import Counter


def extract_features(text):
    """Extract simple statistical features from Arabic text."""
    words = text.split()
    characters = [char for char in text if not char.isspace()]

    if not characters:
        return {
            "word_count": len(words),
            "character_count": 0,
            "unique_char_ratio": 0.0,
            "average_word_length": 0.0,
            "repeated_character_ratio": 0.0,
            "word_entropy": 0.0,
        }

    counts = Counter(characters)
    unique_char_ratio = len(counts) / len(characters)

    average_word_length = (
        sum(len(word) for word in words) / len(words)
        if words else 0.0
    )

    repeated_character_ratio = (
        sum(count - 1 for count in counts.values()) / len(characters)
    )

    word_counts = Counter(words)
    word_entropy = -sum(
        (count / len(words)) * math.log2(count / len(words))
        for count in word_counts.values()
    ) if words else 0.0

    return {
        "word_count": len(words),
        "character_count": len(characters),
        "unique_char_ratio": round(unique_char_ratio, 4),
        "average_word_length": round(average_word_length, 4),
        "repeated_character_ratio": round(repeated_character_ratio, 4),
        "word_entropy": round(word_entropy, 4),
    }


def analyze_text(text):
    features = extract_features(text)

    print("\nنتائج تحليل النص العربي")
    print("-" * 30)

    for feature, value in features.items():
        print(f"{feature}: {value}")

    print("\nملاحظة: هذه الخصائص الإحصائية وحدها لا تثبت وجود بيانات مخفية.")


if __name__ == "main":
    sample_text = input("أدخلي نصاً عربياً للتحليل: ")
    analyze_text(sample_text)