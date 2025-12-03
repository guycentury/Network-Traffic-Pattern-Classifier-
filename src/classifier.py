# src/classifier.py

"""
Classifier module for the network traffic DFA project.

Given:
    - A list of DFA objects
    - An input sequence of network events (e.g. ["SYN", "SYN_ACK", "ACK"])

This module:
    - Runs the sequence through each DFA
    - Returns a high-level label (normal_handshake, suspicious_syn_flood, etc.)
    - Returns detailed results for each DFA (accepted, path, error)
"""

from typing import List, Dict, Any
from .dfa import DFA


def classify_sequence(dfas: List[DFA], input_sequence: List[str]) -> tuple[str, List[Dict[str, Any]]]:
    """
    Run the given input_sequence through all DFAs and produce:
      - A high-level classification label
      - A list of detailed results for each DFA

    Parameters
    ----------
    dfas : List[DFA]
        List of DFA objects (loaded from the JSON definitions in the machines/ directory).
        Each DFA must have a unique 'name' attribute such as:
            - "normal_handshake"
            - "syn_flood"
            - "incomplete_handshake"

    input_sequence : List[str]
        Sequence of network events, e.g. ["SYN", "SYN_ACK", "ACK"].

    Returns
    -------
    label : str
        Overall classification label for the input sequence. Expected values:
            - "normal_handshake"
            - "suspicious_syn_flood"
            - "incomplete_handshake"
            - "unknown_pattern"
            - "multiple_matches"  (if more than one DFA accepts)

    results : List[Dict[str, Any]]
        One entry per DFA with fields:
            - "dfa_name": str
            - "accepted": bool
            - "path": List[str]   (states visited)
            - "error": Optional[str]
    """
    results: List[Dict[str, Any]] = []

    for dfa in dfas:
        accepted, path, error = dfa.run(input_sequence)
        results.append({
            "dfa_name": dfa.name,
            "accepted": accepted,
            "path": path,
            "error": error
        })

    # Find all DFAs that accepted the sequence
    accepted_dfas = [r["dfa_name"] for r in results if r["accepted"]]

    # Decide high-level label based on which DFA(s) accepted
    if not accepted_dfas:
        label = "unknown_pattern"
    elif "normal_handshake" in accepted_dfas:
        label = "normal_handshake"
    elif "syn_flood" in accepted_dfas:
        label = "suspicious_syn_flood"
    elif "incomplete_handshake" in accepted_dfas:
        label = "incomplete_handshake"
    elif len(accepted_dfas) > 1:
        label = "multiple_matches"
    else:
        # Fallback: if some other DFA accepts but we didn't explicitly map it
        label = accepted_dfas[0]

    return label, results
