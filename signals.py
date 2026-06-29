import math

def signal_1(text):
    words = text.split()
    if len(words) == 0:
        return 0.0

    avg_len = sum(len(w) for w in words) / len(words)

    # simple heuristic: more uniform word length = more AI-like
    return min(1.0, avg_len / 12)


def signal_2(text):
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) == 0:
        return 0.0

    lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)

    variance = sum((x - avg) ** 2 for x in lengths) / len(lengths)

    # low variance → more AI-like
    score = 1 / (1 + math.sqrt(variance))

    return min(1.0, score)