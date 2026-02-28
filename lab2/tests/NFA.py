class NfaState:
    def __init__(self, id_, final=False):
        self.id = id_
        self.final = final
        self.arcs = []  # (symbol, target_state)

def build_nfa():
    q0 = NfaState(0)
    q1 = NfaState(1)
    q2 = NfaState(2)
    q3 = NfaState(3)
    q4 = NfaState(4)
    q5 = NfaState(5)
    q6 = NfaState(6)
    q7 = NfaState(7, final=True)

    q0.arcs += [('a', q1), ('b', q3)]
    q1.arcs += [('b', q2), ('c', q0)]
    q2.arcs += [('c', q0)]
    q3.arcs += [('a', q4), ('c', q0)]
    q4.arcs += [('c', q0)]

    for ch in 'abc':
        q4.arcs.append((ch, q5))

    for ch in 'ab':
        q5.arcs.append((ch, q6))

    for ch in 'bc':
        q6.arcs.append((ch, q7))

    return q0

def NFA(start: NfaState, word: str) -> bool:
    stack = [(start, word)]

    while stack:
        state, rest = stack.pop()

        if not rest:
            if state.final:
                return True
            continue

        ch = rest[0]
        tail = rest[1:]

        for sym, to in state.arcs:
            if sym == ch:
                stack.append((to, tail))

    return False