from .dfa import DFA

def classify_sequence(dfas: list[DFA], input_sequence: list[str]):
    """
    Run a list of DFAs on the same input sequence.
    Returns:
        label: str - overall classification
        results: list[dict] - detailed per-DFA result
    """
    results = []

    for dfa in dfas:
        accepted, path, error = dfa.run(input_sequence)
        results.append({
            "dfa_name": dfa.name,
            "accepted": accepted,
            "path": path,
            "error": error
        })

    # Decide overall label based on which DFAs accepted
    accepted_dfas = [r["dfa_name"] for r in results if r["accepted"]]

    if not accepted_dfas:
        label = "unknown_pattern"
    elif "normal_handshake" in accepted_dfas:
        label = "normal_handshake"
    elif "syn_flood" in accepted_dfas:
        label = "suspicious_syn_flood"
    elif "incomplete_handshake" in accepted_dfas:
        label = "incomplete_handshake"
    else:
        label = "multiple_matches"

    return label, results
