import random

GRAMMAR = {
    "SENTENCE": [
        (["TRAIN_DESCRIPTION", "DELAY"], 1),
    ],

    "TRAIN_DESCRIPTION": [
        (["The", "TRAIN", "from", "CITY", "to", "CITY"], 5),
        (["The", "SERVICE", "between", "CITY", "and", "CITY"], 2),
    ],

    "TRAIN": [
        (["train"], 3),
        (["service"], 1),
    ],

    "SERVICE": [
        (["service"], 1),
        (["train service"], 1),
    ],

    "DELAY": [
        (["was", "delayed", "because", "of", "PROBLEM"], 5),
        (["was", "delayed", "due", "to", "PROBLEM"], 5),
    ],

    "PROBLEM": [
        (["SIGNAL"], 5),
        (["TRAIN_PROBLEM"], 2),
        (["STAFF"], 2),
        (["WEATHER"], 1),
    ],

    "SIGNAL": [
        (["a signalling failure"], 1),
        (["a signalling fault"], 1),
    ],

    "TRAIN_PROBLEM": [
        (["a train breakdown"], 1),
        (["a technical fault with the train"], 1),
    ],

    "STAFF": [
        (["a shortage of staff"], 1),
        (["a driver availability issue"], 1),
    ],

    "WEATHER": [
        (["heavy rain"], 1),
        (["strong winds"], 1),
    ],

    "CITY": [
        (["London"], 1),
        (["Manchester"], 1),
        (["Birmingham"], 1),
        (["Cambridge"], 1),
        (["Newcastle"], 1),
    ],
}


def generate(symbol):
    rules = GRAMMAR[symbol]

    choices = [rule for rule, weight in rules]
    weights = [weight for rule, weight in rules]

    rule = random.choices(choices, weights=weights, k=1)[0]

    result = []

    for part in rule:
        if part in GRAMMAR:
            result.append(generate(part))
        else:
            result.append(part)

    return " ".join(result)


print(generate("SENTENCE"))
