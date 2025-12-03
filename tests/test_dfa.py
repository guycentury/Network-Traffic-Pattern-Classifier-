import os
import sys

# Make sure Python can find the src/ package
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.dfa_loader import load_all_dfas
from src.classifier import classify_sequence


def get_dfas():
    """Helper to load all DFA definitions from the machines/ folder."""
    machines_dir = os.path.join(ROOT_DIR, "machines")
    return load_all_dfas(machines_dir)


def test_normal_handshake():
    dfas = get_dfas()
    label, _ = classify_sequence(dfas, ["SYN", "SYN_ACK", "ACK"])
    assert label == "normal_handshake"


def test_syn_flood():
    dfas = get_dfas()
    label, _ = classify_sequence(dfas, ["SYN", "SYN", "SYN", "SYN"])
    assert label == "suspicious_syn_flood"


def test_incomplete_handshake_timeout():
    dfas = get_dfas()
    label, _ = classify_sequence(dfas, ["SYN", "SYN_ACK", "TIMEOUT"])
    assert label == "incomplete_handshake"


def test_unknown_pattern():
    dfas = get_dfas()
    # This pattern shouldn't match any DFA exactly
    label, _ = classify_sequence(dfas, ["ACK", "RST"])
    assert label == "unknown_pattern"
