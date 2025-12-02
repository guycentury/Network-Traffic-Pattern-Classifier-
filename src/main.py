import sys
import os
from .dfa_loader import load_all_dfas
from .classifier import classify_sequence

def main():
    # Determine machines/ directory relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    machines_dir = os.path.join(base_dir, "machines")

    dfas = load_all_dfas(machines_dir)

    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
    else:
        raw = input("Enter sequence (e.g. 'SYN SYN_ACK ACK'): ")

    tokens = raw.strip().split()

    label, detailed_results = classify_sequence(dfas, tokens)

    print(f"\nInput sequence: {tokens}")
    print(f"Overall classification: {label}\n")

    for result in detailed_results:
        print(f"DFA: {result['dfa_name']}")
        if result["error"]:
            print(f"  Error: {result['error']}")
        else:
            print(f"  Accepted: {result['accepted']}")
            print(f"  Path: {result['path']}")
        print()

if __name__ == "__main__":
    main()
