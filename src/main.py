import os
import sys

from .dfa_loader import load_all_dfas
from .classifier import classify_sequence


def main():
    """
    Command-line entry point for the network traffic pattern classifier.
    Usage examples:
        python -m src.main "SYN SYN_ACK ACK"
        python -m src.main "SYN SYN SYN SYN"
    If no arguments are provided, the program will prompt for input.
    """
    # Resolve machines directory relative to this file's parent
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    machines_dir = os.path.join(base_dir, "machines")

    # Load all DFA definitions from JSON files
    dfas = load_all_dfas(machines_dir)

    # Get the input sequence either from CLI args or from user input
    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
    else:
        raw = input("Enter a sequence of events "
                    "(space-separated, e.g. 'SYN SYN_ACK ACK'): ")

    tokens = raw.strip().split()

    # Classify the sequence using all DFAs
    label, results = classify_sequence(dfas, tokens)

    # Print a summary
    print("\n=== Network Traffic Pattern Classification ===")
    print(f"Input sequence: {tokens}")
    print(f"Overall classification: {label}\n")

    # Print detailed DFA results
    for r in results:
        print(f"DFA: {r['dfa_name']}")
        if r["error"]:
            print(f"  Error: {r['error']}")
        else:
            print(f"  Accepted: {r['accepted']}")
            print(f"  Path: {r['path']}")
        print()


if __name__ == "__main__":
    main()
