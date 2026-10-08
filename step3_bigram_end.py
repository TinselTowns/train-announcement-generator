import random

pairs = {}


def parse(path):
    with open(path, "r") as file:
        sentences = file.readlines()

    for sentence in sentences:
        tokens = sentence.split()

        # Count every word -> next word pair.
        for i in range(len(tokens) - 1):
            word = tokens[i]
            next_word = tokens[i + 1]

            if word not in pairs:
                pairs[word] = {}

            if next_word not in pairs[word]:
                pairs[word][next_word] = 0

            pairs[word][next_word] += 1

        # Add an explicit end-of-sentence transition.
        last_word = tokens[-1]

        if last_word not in pairs:
            pairs[last_word] = {}

        if "<END>" not in pairs[last_word]:
            pairs[last_word]["<END>"] = 0

        pairs[last_word]["<END>"] += 1


def normalise():
    for word in pairs:
        total = sum(pairs[word].values())

        for next_word in pairs[word]:
            pairs[word][next_word] /= total


def generate_word(word):
    words = list(pairs[word].keys())
    probs = list(pairs[word].values())

    return random.choices(words, weights=probs, k=1)[0]


def generate():
    word = "The"
    sentence = word

    while word in pairs:
        next_word = generate_word(word)

        if next_word == "<END>":
            break

        sentence += " " + next_word
        word = next_word

    return sentence


parse("training_data_small.txt")
normalise()

print(generate())
