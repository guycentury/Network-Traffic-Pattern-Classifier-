import os
from src.dfa_loader import load_all_dfas
from src.classifier import classify_sequence

def get_dfas():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    machines_dir = os.path.join(base_dir, "machines")
    return load_all_dfas(machines_dir)

def test_normal_handshake():
    dfas = get_dfas()
    label, _ = classify_sequence(dfas, ["SYN", "SYN_ACK", "ACK"])
    assert label == "normal_handshake"

def test_syn_flood():
    dfas = get_dfas()
    label, _ = classify_sequence(dfas, ["SYN", "SYN", "SYN", "SYN"])
    assert label == "suspicious_syn_flood"

def test_incomplete_handshake():
    dfas = get_dfas()
    label, _ = classify_sequence(dfas, ["SYN", "SYN_ACK", "TIMEOUT"])
    assert label == "incomplete_handshake"
