import random

GRAMMAR = {
    "SENTENCE": [
        (['TRAIN_DESCRIPTION', 'DELAY'], 1)
    ],

    'TRAIN_DESCRIPTION': [
        (['The', 'TRAIN', 'from', 'CITY', 'to', 'CITY'], 1),
        (['The', 'SERVICE', 'between', 'CITY', 'and', 'CITY'], 1),
        (["The", "CITY", "to", "CITY", "SERVICE"], 1),
    ],

    'TRAIN': [
        (['train'], 1),
        (['serice'], 1)
    ],

     "SERVICE": [
        (["service"], 1),
        (["train service"], 1),
    ],

    'DELAY': [
        (['was', 'delayed', 'because', 'of', 'PROBLEM'], 7),
        (['was', 'dealyed', 'due', 'to', 'PROBLEM'], 3)
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
        (["a technical fault with the train"], 4),
    ],

    "STAFF": [
        (["a shortage of staff"], 3),
        (["a driver availability issue"], 2),
    ],

    "WEATHER": [
        (["heavy rain"], 5),
        (["strong winds"], 3),
    ],

    "CITY": [
        (["London"], 10),
        (["Manchester"], 7),
        (["Birmingham"], 6),
        (["Cambridge"], 2),
        (["Newcastle"], 3),
    ],
}

pairs = {}

def train():
    parse("training_data_medium.txt")
    normalise()

def parse(path):
    with open(path, "r") as file:
        sentences = file.readlines()
        for sentence in sentences:
            tokens = sentence.split()
            for i in range(len(tokens)-2):
                if (tokens[i], tokens[i+1]) not in pairs:
                    pairs[(tokens[i], tokens[i+1])] = {}
                next_words = pairs[(tokens[i], tokens[i+1])].keys()
                next_word = tokens[i+2]
                if next_word not in next_words:
                    pairs[(tokens[i], tokens[i+1])][next_word] = 0
                pairs[(tokens[i], tokens[i+1])][next_word] += 1
            if (tokens[-2], tokens[-1]) not in pairs:
                pairs[(tokens[-2], tokens[-1])] = {}

            if "<END>" not in pairs[(tokens[-2], tokens[-1])]:
                pairs[(tokens[-2], tokens[-1])]["<END>"] = 0

            pairs[(tokens[-2], tokens[-1])]["<END>"] += 1

def normalise():
    for word in pairs.keys():
        count = 0
        for next_word in pairs[word].keys():
            count += pairs[word][next_word]
        for next_word in pairs[word].keys():
            pairs[word][next_word]/=count

def generate():
    next_word = generate_word('This', 'train')
    cur_word = 'train'

    sentence = 'This train'

    if next_word == '<END>':
        return sentence

    sentence += ' ' + next_word

    while (cur_word, next_word) in pairs:
        new_word = generate_word(cur_word, next_word)

        cur_word = next_word
        next_word = new_word

        if next_word == '<END>':
            break

        sentence += ' ' + next_word

    return sentence
    
def generate_word(word1, word2):
    next_word = ''
    
    words = [w for w in pairs[(word1, word2)]]
    probs = [pairs[(word1, word2)][w] for w in pairs[(word1, word2)]]
    next_word = random.choices(words, weights=probs, k=1)[0]
    return next_word


#def generate(symbol):
#    rules = GRAMMAR[symbol]
#    choices = [rule for rule, _ in rules]
#    weights = [weight for _, weight in rules]

#    rule = random.choices(choices, weights=weights, k=1)[0]

 #   result = []
 #   for token in rule:
 #       if token in GRAMMAR:
 #           result.append(generate(token))
 #       else:
 #           result.append(token)
 #   return " ".join(result)

#explanation = generate("SENTENCE")
#print(explanation) 
train()
print(pairs[("This", "train")])

print(generate())