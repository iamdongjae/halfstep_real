import sys
from better_profanity import profanity
import re
import requests

profanity.load_censor_words()

url = "https://raw.githubusercontent.com/PersesTitan/BadWordFiltering/master/badwords.txt"
response = requests.get(url)
word_list = response.text.split(",")
kr_bad_word_list = list()
for word in word_list:
    kr_bad_word_list.append(word.strip())

def detect_profanity(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    words = re.findall(r'\w+', text)
    total_words = len(words)
    profanity_count_en = sum(1 for word in words if profanity.contains_profanity(word))
    profanity_count_kr = sum(text.count(word) for word in kr_bad_word_list if word in text)
    
    profanity_count = profanity_count_en + profanity_count_kr

    profanity_ratio = (profanity_count / total_words) * 100 if total_words > 0 else 0
    return profanity_ratio

if __name__ == "__main__":
    file_path = sys.argv[1]
    profanity_ratio = detect_profanity(file_path)
    print(profanity_ratio)
