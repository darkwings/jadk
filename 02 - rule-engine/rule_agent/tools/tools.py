import random

def get_value(source_id: str) -> dict:
    """
    Generates a dictionary with a source ID and the value associated to that ID
    """
    dict = {
        "source_id": source_id,
        "value": random.randint(1, 1000)
    }
    return dict