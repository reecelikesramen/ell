import random
from typing import List, Tuple
import ell
ell.config.verbose = True


names_list = [
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Eve",
    "Frank",
    "Grace",
    "Hank",
    "Ivy",
    "Jack",
]

@ell.lm(model="gpt-4o-mini", temperature=1.0)
def create_personality() -> str:
    """You are backstoryGPT. You come up with a backstory for a character incljuding name. Choose a completely random name from the list. Format as 'Name: <name>\nBackstory: <3 sentence backstory>'"""
    return "Come up with a backstory about " + random.choice(names_list)


def format_message_history(message_history : List[Tuple[str, str]]) -> str:
    return "\n".join([f"{name}: {message}" for name, message in message_history])

@ell.lm(model="gpt-4o-mini", temperature=0.3, max_tokens=20)
def chat(personality : str, message_history : List[Tuple[str, str]]) -> str:

    return [
        ell.system(f"""You are
    {personality}. 

    Your goal is to come up with a response to a chat. Only respond in one sentence (should be like a text message in informality.)"""),
        ell.user(format_message_history(message_history)),
    ]



if __name__ == "__main__":
    from ell.stores.sql import SQLiteStore
    store = SQLiteStore('sqlite_example')
    store.install(autocommit=True)
    messages : List[Tuple[str, str]]= []
    personalities = [create_personality(), create_personality()]

    names = []
    backstories = []
    for personality in personalities:
        parts = personality.split("\n")
        names.append(parts[0].split(": ")[1])
        backstories.append(parts[1].split(": ")[1])
    print(names)
    whos_turn = 0 
    for _ in range(10):

        personality_talking = personalities[whos_turn]
        messages.append(
            (names[whos_turn], chat(personality_talking, messages)))
        
        whos_turn = (whos_turn + 1) % len(personalities)
    print(messages)