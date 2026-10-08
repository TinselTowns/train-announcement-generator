# Progress: From a Grammar to a Trigram Language Model

This project started as a simple hand-written system for generating realistic UK train-delay explanations. The goal was to gradually move from rules written by a human toward patterns learned directly from text.

The four steps below capture the main progression.

## Step 1 Grammar

### Motivation

The first step was to understand how a language generator can be built without any machine learning at all.

Instead of learning from data, I explicitly described the structure of a train-delay sentence ourselves. For example, a sentence could have the form:

```text
TRAIN_DESCRIPTION + DELAY
```

The grammar contained alternatives for things such as cities, train descriptions, and causes of delays.

For example:

```python
GRAMMAR = {
    "SENTENCE": [
        ["TRAIN_DESCRIPTION", "DELAY"]
    ],

    "TRAIN_DESCRIPTION": [
        ["The", "TRAIN", "from", "CITY", "to", "CITY"],
        ["The", "SERVICE", "between", "CITY", "and", "CITY"],
    ],

    "DELAY": [
        ["was", "delayed", "because", "of", "PROBLEM"],
        ["was", "delayed", "due", "to", "PROBLEM"],
    ],

    "PROBLEM": [
        ["SIGNAL"],
        ["TRAIN_PROBLEM"],
        ["STAFF"],
        ["WEATHER"],
    ],
}
```

The generator recursively expands these symbols until only ordinary words remain.

### Example output

```text
The train from Cambridge to Newcastle was delayed due to a signalling fault.
```

Another possible output:

```text
The service between London and Manchester was delayed because of heavy rain.
```

At this stage, **the grammar knows everything**. The system does not learn anything from examples. I tell it what a valid sentence should look like.

This gave us a useful starting point, but it also raised the next question:

> What if I don't want to decide all of these choices ourselves?

That leads to rules and weights.

## Step 2 Rules with Weights

### Motivation

The grammar initially chose between alternatives randomly. But in real language, some alternatives occur more often than others.

For example, I might want the model to choose signalling problems more often than weather problems:

```python
"PROBLEM": [
    (["SIGNAL"], 5),
    (["TRAIN_PROBLEM"], 2),
    (["STAFF"], 2),
    (["WEATHER"], 1),
]
```

The weights mean that the choices are no longer equally likely.

I used:

```python
random.choices(choices, weights=weights, k=1)
```

This was an important conceptual step because it introduced the idea that language generation can be **probabilistic**.

Instead of saying:

```text
choose A or B
```

I can say:

```text
A is more likely than B
```

### Example output

The weighted grammar could produce:

```text
The train from London to Cambridge was delayed due to a signalling failure.
```

and:

```text
The service between Manchester and Birmingham was delayed because of a shortage of staff.
```

The structure is still hand-written, but now the choices have probabilities.

This led to the key question for the next stage:

> Instead of manually assigning the weights, can I learn them from example sentences?

That is where the n-gram model begins.

## Step 3 Bigram with an <END> token

### Motivation

For the bigram model, I removed the hand-written grammar from the generation process.

Instead, I gave the model training text and counted which words appeared next to which other words.

For example:

```text
The train from London
```

produces relationships such as:

```text
The   -> train
train -> from
from  -> London
```

I stored the counts in a nested dictionary:

```python
pairs = {
    "The": {
        "train": 10,
        "service": 5
    },
    "train": {
        "from": 8
    }
}
```

I then normalized the counts so that the possible next words became probabilities.

For example:

```text
train -> from = 1.0
```

means that, in the training data, `from` followed `train` every time that transition was observed.

I also introduced a special `<END>` token.

If a sentence ended with:

```text
... signalling fault.
```

I represented the end as:

```text
fault -> <END>
```

This gives the model a way to know when a generated sentence should stop.

### Example output

The bigram model could produce a sentence such as:

```text
The service from Cambridge to London was delayed following a signalling fault. <END>
```

But it could also produce something broken:

```text
The service from Manchester to a signalling fault. <END>
```

This was an important result.

The model was no longer following our grammar. It was simply following learned word-to-word probabilities.

The problem is that a word only has **one word of context**.

When the model sees:

```text
to
```

it only knows which words followed `to` in the training data. It does not know that, in our intended sentence structure, `to` should normally be followed by a city.

This explains why the model can produce locally plausible transitions while creating a globally strange sentence.

That motivates the next step: give it more context.

## Step 4 Trigram

### Motivation

A trigram model looks at the previous **two words** instead of just one.

So instead of learning:

```text
train -> from
```

I learn:

```text
(The, train) -> from
```

The model therefore stores relationships such as:

```python
pairs = {
    ("The", "train"): {
        "from": 1
    }
}
```

The important difference is the amount of context available.

For a bigram:

```text
The -> train
```

For a trigram:

```text
The train -> from
```

During generation, the context moves forward one word at a time:

```text
The train
    ↓
train from
    ↓
from Cambridge
    ↓
Cambridge to
    ↓
to Newcastle
```

At every point, the next word is chosen based on the previous two words.

### Example output

With the synthetic training data, the trigram model produced outputs such as:

```text
The train from Cambridge to Newcastle was delayed due to a signalling fault.
```

and:

```text
The train from Birmingham to London was delayed due to a technical problem.
```

and:

```text
The train from London to Newcastle was delayed following flooding.
```

These were noticeably more coherent than many of the bigram outputs.

I then tried the same trigram model on more realistic railway text, without changing the basic model.

Examples included:

```text
This train has been delayed by the train guard being taken ill
```

```text
This train has been delayed by thick fog earlier on this train's journey
```

```text
This train has been cancelled because of expected industrial action yesterday
```

The outputs are not perfect, but they demonstrate the main progression of the project.

The model has moved from:

```text
hand-written grammar
```

to:

```text
hand-written probabilities
```

to:

```text
probabilities learned from text
```

and finally to:

```text
probabilities learned from two-word context
```

The next natural step is to move beyond counting n-grams and build a **neural language model**, where the model learns numerical parameters from data rather than storing explicit word-pair or word-triplet tables.
