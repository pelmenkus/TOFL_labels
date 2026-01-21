from DFA import DFA 
from NFA import NFA, build_nfa
from regex import match_by_regex
import random
from AFA import build_L1_AFA, build_L2_as_AFA, AFA_intersect  # Исправил опечатку

alphabet = ['a', 'b', 'c']
MAX_LEN = 20
NUM_TESTS = 1000

# Случайное слово
def make_random_word() -> str:
    length = random.randint(0, MAX_LEN)
    return ''.join(random.choice(alphabet) for _ in range(length))

def main():
    nfa_start = build_nfa()
    L1_start = build_L1_AFA()
    L2_start = build_L2_as_AFA(final_states=["q9", "q11","q8","q7"])
    for _ in range(NUM_TESTS):
        w = make_random_word()
        r = match_by_regex(w)
        d = DFA(w)  # Убедись, что это возвращает True/False
        n = NFA(nfa_start, w)  # True/False
        a = AFA_intersect(L1_start, L2_start, w)  # True/False
        if r:
            print(w)  # На всякий случай, чтобы проверить корректное слово
            print()
        if not (r == d == n == a):
            print(f'Ошибка на слове "{w}"')
            print(f'  regex: {r}')
            print(f'  DFA  : {d}')
            print(f'  NFA  : {n}')
            print(f'  AFA  : {a}')  # Исправлено название
            return

    print("Все тесты пройдены: True")

if __name__ == "__main__":
    main()