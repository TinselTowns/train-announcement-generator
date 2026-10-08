path = "training_data_medium.txt"

with open(path, "r") as file:
    sentences = file.readlines()

with open(path, "w") as file:
    for sentence in sentences:
        sentence = sentence.split(":", 1)[1].strip()
        file.write(sentence + "\n")