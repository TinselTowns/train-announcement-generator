import random

CITIES = ["London", "Manchester", "Birmingham", "Cambridge", "Newcastle"]

SIGNAL = ["a signalling failure", "a signalling fault"]
TRAIN = ["a train breakdown"]
STAFF = ["a shortage of staff", "a driver availability issue"]
WEATHER = ["heavy rain", "strong winds"]

PROBLEMS = [SIGNAL, TRAIN, STAFF, WEATHER]

from_city = random.choice(CITIES)
possible_destinations = [city for city in CITIES if city != from_city]
to_city = random.choice(possible_destinations)

problem_section = random.choice(PROBLEMS)
problem = random.choice(problem_section)

explanation = (
    f"The train from {from_city} to {to_city} "
    f"was delayed due to {problem}"
)

print(explanation)
