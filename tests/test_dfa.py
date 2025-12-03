import os
from src.dfa_loader import load_all_dfas
from src.classifier import classify_sequence


def get_dfas():
    """
    Helper that loads all DFA JSON definitions from the machines/ directory.
    This assumes this directory structure:

    project_root/
      src/
      machines/
      tests/
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    machines_dir = os.path.join(base_dir, "machines")
    return load_all_dfas(machines_dir)


def test_normal_handshake():
    """
    normal_handshake DFA should accept SYN SYN_ACK ACK
    and classify it as a normal_handshake.
    """
    dfas = get_dfas()
    label, _ = classify_sequence(dfas, ["SYN", "SYN_ACK", "ACK"])
    assert label == "normal_handshake"


def test_syn_flood():
    """
    syn_flood DFA should accept sequences with 3 or more SYN in a row.
    """
    dfas = get_dfas()
    label, _ = classify_sequence(dfas, ["SYN", "SYN", "SYN", "SYN"])
    assert label == "suspicious_syn_flood"


def test_incomplete_handshake():
    """
    incomplete_handshake DFA should accept SYN SYN_ACK followed by
    a non-ACK event such as TIMEOUT.
    """
    dfas = get_dfas()
    label, _ = classify_sequence(dfas, ["SYN", "SYN_ACK", "TIMEOUT"])
    assert label == "incomplete_handshake"
