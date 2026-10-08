import random
import math
vocab = {}
reverse_vocab = {}


pairs = {}

data = []

weights = []

LEARNING_RATE = 0.015
EMBEDDING_SIZE = 3
embeddings = []

def train():
    global embeddings, weights
    parse("training_data_small.txt")
    embeddings = [[random.random() for _ in range(EMBEDDING_SIZE)] for _ in range(len(vocab))]

    weights = [[random.random() for _ in range(EMBEDDING_SIZE)] for _ in range(len(vocab))]
    for epoch in range(40):
        total_loss = 0
        count = 0
        for sentence in data:
            for i in range(len(sentence)-2):
                input_id1 = sentence[i]
                input_id2 = sentence[i+1]
                target_id = sentence[i+2]

                probs = predict(input_id1, input_id2)
                count+=1
                #print(probs)
                correct_probability = probs[target_id]
                #print("probability:", correct_probability)
                loss = - math.log(correct_probability)
                total_loss+=loss
                #print('Loss', loss)
                gradients = [probs[i] - (i==target_id) for i in range(len(probs))]
                #print(gradients)
                weights_backpropagation(input_id1, input_id2, gradients)
                embedding_backpropagation(input_id1, gradients)
                embedding_backpropagation(input_id2, gradients)
                #print("Target:", target_id, "P:", probs[target_id], "Loss:", loss)
        average_loss = total_loss / count

        print("Epoch:", epoch, "Loss:", average_loss)

def predict(input_id1, input_id2):
    embedding1 = embeddings[input_id1]
    embedding2 = embeddings[input_id2]

    embedding = [embedding1[i]+embedding2[i] for i in range(EMBEDDING_SIZE)]
    
    scores = [dot_product(embedding, weights[i]) for i in range(len(vocab))]

    max_score = max(scores)

    exp_scores = [math.exp(score - max_score) for score in scores]

    exp_sum = sum(exp_scores)

    probs = [x / exp_sum for x in exp_scores]

    return probs

def weights_backpropagation(input_id1, input_id2, gradients):
    global weights
    embedding1 = embeddings[input_id1]
    embedding2 = embeddings[input_id2]

    embedding = [embedding1[i]+embedding2[i] for i in range(EMBEDDING_SIZE)]
    for i in range(len(weights)):
        for j in range(EMBEDDING_SIZE):
            weights[i][j] -= LEARNING_RATE * gradients[i] * embedding[j]

def embedding_backpropagation(input_id, gradients):
    global embeddings
    embedding_gradient = [0]*EMBEDDING_SIZE

    for i in range(EMBEDDING_SIZE):
        for j in range(len(weights)):
            embedding_gradient[i] += gradients[j] * weights[j][i]

    for i in range(EMBEDDING_SIZE):
        embeddings[input_id][i] -= LEARNING_RATE * embedding_gradient[i]

def dot_product(a, b):
    result = 0
    for i in range(len(a)):
        result += a[i]*b[i]
    return result

def parse(path):
    populate_vocab(path)

    with open(path, "r") as file:
        sentences = file.readlines()
        for sentence in sentences:
            new_sentence = []
            tokens = sentence.split()
            for token in tokens:
                new_sentence.append(vocab[token])
            data.append(new_sentence)
    


def populate_vocab(path):
    next_id = 0
    with open(path, "r") as file:
        sentences = file.readlines()
        for sentence in sentences:
            tokens = sentence.split()
            for token in tokens:
                if token not in vocab:
                    vocab[token] = next_id
                    next_id += 1

train()
probs = predict(vocab["This"], vocab["train"])
max_prob = 0
next_word = 0
for i in range(len(probs)):
    if probs[i] > max_prob:
        max_prob = probs[i]
        next_word = i
for word in vocab.keys():
    reverse_vocab[vocab[word]] = word
print(reverse_vocab[next_word])
print(max_prob)

top_ids = sorted(
    range(len(probs)),
    key=lambda i: probs[i],
    reverse=True
)[:5]

for i in top_ids:
    print(reverse_vocab[i], probs[i])
word1 = 'This'
word2 = 'train'
next_word = ''
print(word1)
print(word2)
while '.' not in next_word:
    probs = predict(vocab[word1], vocab[word2])
    next_id = random.choices(range(len(vocab)), weights=probs, k=1)[0]
    next_word = reverse_vocab[next_id]
    word1 = word2
    word2 = next_word
    print(next_word)
#print(vocab)
#print(data)


