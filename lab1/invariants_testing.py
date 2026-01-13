import random
from fuzz_tests import random_word, reduce_word


newT = {
    "bpb": "abapba",
    "p": "aba",
    "apa": "bb",
    "abba": "baab",
    "baababaa": "abbbb",
    "aababaab": "bbbba",
    "aabaa": "bb",
}

""" 1. p не увеличивается
    2. b не уменьшается
    3. (a + b) mod 3 постоянно"""
def check_invariants(chain: list[str]) -> bool:

    if chain:
        w = chain[0]
        main_p = w.count('p')
        main_b = w.count('b')
        main_ab = (w.count('a') + main_b) % 3

        for w in chain[1:]:
            b_count = w.count('b')
            p_count = w.count('p')
            a_count = w.count('a')
            if p_count > main_p:
                print(f"Цепочка: {chain}")
                print(f"Слово: {w}")
                print(f"FALSE. Инвариант p: main_p = {main_p}, curr_p = {p_count}")
                return False
            if b_count < main_b:
                print(f"Цепочка: {chain}")
                print(f"Слово: {w}")
                print(f"FALSE. Инвариант b: main_b = {main_b}, curr_b = {b_count}")
                return False
            if (a_count + b_count) % 3 != main_ab:
                print(f"Цепочка: {chain}")
                print(f"Слово: {w}")
                print(f"FALSE. Инвариант a+b: main_ab = {main_ab}, curr_ab = {(a_count + b_count) % 3}")
                return False

    return True

#Прогон тестов
def test_invariants(all_tests: int):

    fail_count = 0

    for _ in range(all_tests):
        start = random_word(10, 25)
        chain = reduce_word(start, newT)
        test_passed = check_invariants(chain)

        if not test_passed:
            fail_count += 1
        #print(f"Начало: {start}")
        #print(f"Цепочка: {chain}\n")

    print(f"\nВсего тестов: {all_tests}")
    print(f"Нарушений инвариантов: {fail_count}")



if __name__ == "__main__":
    random.seed(1231231)#тоже с сидом для проверки корректности
    test_invariants(all_tests=8)
