import json
import os
from .dfa import DFA

def load_dfa_from_file(path):
    with open(path, "r") as f:
        data = json.load(f)

    return DFA(
        name=data["name"],
        alphabet=data["alphabet"],
        states=data["states"],
        start_state=data["start_state"],
        accept_states=data["accept_states"],
        transitions=data["transitions"]
    )

def load_all_dfas(machines_dir):
    dfas = []
    for filename in os.listdir(machines_dir):
        if filename.endswith(".json"):
            full_path = os.path.join(machines_dir, filename)
            dfas.append(load_dfa_from_file(full_path))
    return dfas
