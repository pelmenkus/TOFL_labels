def DFA(word: str) -> bool:
    q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, qDead = range(14)

    det = [
        [q1, q2, qDead],    # q0
        [qDead, q3, q0],    # q1
        [q4, qDead, q0],    # q2
        [qDead, qDead, q0], # q3
        [q5, q5, q6],       # q4
        [q7, q7, qDead],    # q5
        [q8, q9, qDead],    # q6
        [qDead, q10, q10],  # q7
        [qDead, q11, q12],  # q8
        [q4, q10, q12],     # q9
        [qDead, qDead, qDead], # q10
        [qDead, qDead, q0],    # q11
        [q1, q2, qDead],       # q12
        [qDead, qDead, qDead], # dead
    ]

    final_states = {q10, q11, q12}

    state = q0
    for ch in word:
        if ch == 'a':
            idx = 0
        elif ch == 'b':
            idx = 1
        elif ch == 'c':
            idx = 2
        else:
            return False
        state = det[state][idx]

    return state in final_states