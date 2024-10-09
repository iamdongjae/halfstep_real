import sys
from better_profanity import profanity
import re

profanity.load_censor_words()

def detect_profanity(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    words = re.findall(r'\w+', text)
    total_words = len(words)
    profanity_count = sum(1 for word in words if profanity.contains_profanity(word))

    profanity_ratio = (profanity_count / total_words) * 100 if total_words > 0 else 0
    return profanity_ratio

if __name__ == "__main__":
    file_path = sys.argv[1]
    profanity_ratio = detect_profanity(file_path)
    print(profanity_ratio)
