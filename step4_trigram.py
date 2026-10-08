import random

pairs = {}


def parse(path):
    with open(path, "r") as file:
        sentences = file.readlines()

    for sentence in sentences:
        tokens = sentence.split()

        # Count every two-word context -> next word.
        for i in range(len(tokens) - 2):
            context = (tokens[i], tokens[i + 1])
            next_word = tokens[i + 2]

            if context not in pairs:
                pairs[context] = {}

            if next_word not in pairs[context]:
                pairs[context][next_word] = 0

            pairs[context][next_word] += 1

        # Add <END> after the final two-word context.
        context = (tokens[-2], tokens[-1])

        if context not in pairs:
            pairs[context] = {}

        if "<END>" not in pairs[context]:
            pairs[context]["<END>"] = 0

        pairs[context]["<END>"] += 1


def normalise():
    for context in pairs:
        total = sum(pairs[context].values())

        for next_word in pairs[context]:
            pairs[context][next_word] /= total


def generate_word(word1, word2):
    context = (word1, word2)

    words = list(pairs[context].keys())
    probs = list(pairs[context].values())

    return random.choices(words, weights=probs, k=1)[0]


def generate():
    word1 = "The"
    word2 = "train"

    sentence = "The train"

    while (word1, word2) in pairs:
        next_word = generate_word(word1, word2)

        if next_word == "<END>":
            break

        sentence += " " + next_word

        # Move the two-word context forward by one word.
        word1 = word2
        word2 = next_word

    return sentence


# For the synthetic corpus:
parse("training_data_small.txt")

# To try the real railway corpus instead, use:
# parse("training_data_medium.txt")

normalise()

print(generate())
