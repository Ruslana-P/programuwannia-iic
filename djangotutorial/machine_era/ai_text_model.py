import re

def count_syllables(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if len(word) == 0:
        return 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def analyze_readability(text):
    """
    Розраховує Flesch Reading Ease score.
    Формула: 206.835 - 1.015(total_words/total_sentences) - 84.6(total_syllables/total_words)
    """
    if not text.strip():
        return 0.0, "EMPTY.DATA"

    # Очистка і розбиття
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    total_sentences = len(sentences) or 1

    words = re.findall(r'\b\w+\b', text)
    total_words = len(words) or 1

    total_syllables = sum(count_syllables(w) for w in words)

    # Розрахунок Score
    score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
    score = round(score, 2)

    # Вердикт
    if score >= 90:
        verdict = "VERY.EASY (5th grade)"
    elif score >= 80:
        verdict = "EASY (6th grade)"
    elif score >= 70:
        verdict = "FAIRLY.EASY (7th grade)"
    elif score >= 60:
        verdict = "STANDARD (8th-9th grade)"
    elif score >= 50:
        verdict = "FAIRLY.DIFFICULT (High School)"
    elif score >= 30:
        verdict = "DIFFICULT (College)"
    else:
        verdict = "VERY.CONFUSING (Professional/Academic)"

    return score, verdict