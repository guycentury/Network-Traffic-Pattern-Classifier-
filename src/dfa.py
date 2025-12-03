class DFA:
    def __init__(self, name, alphabet, states, start_state, accept_states, transitions):
        self.name = name
        self.alphabet = set(alphabet)
        self.states = set(states)
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transitions = transitions

    def run(self, input_symbols):
        """
        Run this DFA on a list of input symbols.

        Returns:
            (accepted: bool, path: list[str], error: Optional[str])
        """
        state = self.start_state
        path = [state]

        for symbol in input_symbols:
            if symbol not in self.alphabet:
                return False, path, f"Unknown symbol: {symbol}"

            state_transitions = self.transitions.get(state, {})
            if symbol not in state_transitions:
                return False, path, f"No transition defined for ({state}, {symbol})"

            state = state_transitions[symbol]
            path.append(state)

        accepted = state in self.accept_states
        return accepted, path, None
