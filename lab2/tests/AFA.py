class AFAState:
    def __init__(self, id_, term=False):
        self.id = id_          # уникальный идентификатор состояния
        self.term = term       # терминальное состояние
        self.edges = []        # список переходов: (символ или None для ε, [список состояний])

    def add_edge(self, symbol, states):
        self.edges.append((symbol, states))


# Строим DFA L1
def build_L1_AFA():
    p = [AFAState(i) for i in range(14)]
    # Терминальные состояния
    p[7].term = True
    p[10].term = True
    p[11].term = True
    p[13].term = True

    # Переходы
    p[0].edges += [('a', [p[1]]), ('b', [p[3]])]
    p[1].edges += [('b', [p[2]]), ('c', [p[0]])]
    p[2].edges += [('c', [p[0]])]
    p[3].edges += [('a', [p[4]]), ('c', [p[0]])]
    p[4].edges += [('a', [p[5]]), ('b', [p[5]]), ('c', [p[8]])]
    p[5].edges += [('a', [p[6]]), ('b', [p[6]]), ('c', [p[6]])]
    p[6].edges += [('a', [p[7]]), ('b', [p[7]]), ('c', [p[7]])]
    p[8].edges += [('a', [p[9]]), ('b', [p[12]]), ('c', [p[6]])]
    p[9].edges += [('a', [p[7]]), ('b', [p[11]]), ('c', [p[10]])]
    p[10].edges += [('a', [p[1]]), ('b', [p[3]])]
    p[11].edges += [('c', [p[0]])]
    p[12].edges += [('a', [p[13]]), ('b', [p[7]]), ('c', [p[10]])]
    p[13].edges += [('a', [p[5]]), ('b', [p[5]]), ('c', [p[8]])]

    return p[0]


# Строим DFA L2
def build_L2_as_AFA(final_states):
    states = {f"q{i}": AFAState(f"q{i}") for i in range(1, 13)}
    for f in final_states:
        states[f].term = True

    def add(src, ch, dst):
        states[src].add_edge(ch, [states[dst]])

    add("q1", "a", "q1");  add("q1", "b", "q2");  add("q1", "c", "q1")
    add("q2", "a", "q3");  add("q2", "b", "q2");  add("q2", "c", "q1")
    add("q3", "a", "q10"); add("q3", "b", "q4");  add("q3", "c", "q10")
    add("q4", "a", "q5");  add("q4", "b", "q6");  add("q4", "c", "q1")
    add("q5", "a", "q10"); add("q5", "b", "q9");  add("q5", "c", "q11")
    add("q6", "a", "q3");  add("q6", "b", "q7");  add("q6", "c", "q8")
    add("q7", "a", "q3");  add("q7", "b", "q2");  add("q7", "c", "q1")
    add("q8", "a", "q1");  add("q8", "b", "q2");  add("q8", "c", "q1")
    add("q9", "a", "q5");  add("q9", "b", "q6");  add("q9", "c", "q1")
    add("q10","a","q12");  add("q10","b","q6");  add("q10","c","q1")
    add("q11","a","q12");  add("q11","b","q6");  add("q11","c","q11")
    add("q12","a","q1");   add("q12","b","q7");  add("q12","c","q8")

    return states["q1"]


# Строим пересечение L1 ∩ L2
def intersect_L1_L2(L1_start, L2_start):
    start = AFAState("start")
    # AND-переход по ε в два автомата
    start.add_edge(None, [L1_start, L2_start])
    return start


# Проверка принятия AFA
def AFA_single(start, word):
    # твоя старая реализация accept_state с memo
    def accept_state_single(state, word, pos, memo):
        key = (state.id, pos)
        if key in memo:
            return memo[key]

        if pos == len(word):
            if state.term:
                memo[key] = True
                return True
            for sym, outs in state.edges:
                if sym is None:
                    if all(accept_state_single(s, word, pos, memo) for s in outs):
                        memo[key] = True
                        return True
            memo[key] = False
            return False

        for sym, outs in state.edges:
            if sym is None:
                if all(accept_state_single(s, word, pos, memo) for s in outs):
                    memo[key] = True
                    return True
            elif word[pos] == sym:
                for s in outs:
                    if accept_state_single(s, word, pos + 1, memo):
                        memo[key] = True
                        return True

        memo[key] = False
        return False

    return accept_state_single(start, word, 0, {})


# --- Проверка пересечения двух автоматов ---
def AFA_intersect(L1_start, L2_start, word):
    #a = AFA_single(L1_start, word)
    #b = AFA_single(L2_start, word)
    #print (a, b, "haha")
    return AFA_single(L1_start, word) and AFA_single(L2_start, word)

if __name__ == "__main__":
    L1_start = build_L1_AFA()
    L2_start = build_L2_as_AFA(final_states=["q9", "q11","q8","q7"])

    tests = ["abca", "aac", "bacab", "abcbabac"]
    for w in tests:
        print(f"{w}: {AFA_intersect(L1_start, L2_start, w)}")