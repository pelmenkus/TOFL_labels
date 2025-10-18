import random
from collections import deque


# словарь правил переписывания: {ключ = правило -> значение = переписывание}
T = {
    "bpb": "abapba",
    "p": "aba",
    "apa": "bb",
    "abba": "baab",
}

newT = {
    "bpb": "abapba",
    "p": "aba",
    "apa": "bb",
    "abba": "baab",
    "baababaa": "abbbb",
    "aababaab": "bbbba",
    "aabaa": "bb",
}

alph = ['a', 'b', 'p']

#случайное слово из алфавита
def random_word(min_len: int, max_len: int) -> str:

    n = random.randint(min_len, max_len)
    return ''.join(random.choice(alph) for _ in range(n))

#Применяет все возможные правила из словаря + учет, к примеру, для правила aba->b строка ababa может по системе T стать abb или bba
def rewrite(word: str, rules: dict[str, str]) -> list[str]:

    outcomes = set()
    for pattern, replacement in rules.items():
        start = 0
        while True:
            pos = word.find(pattern, start)
            if pos == -1:
                break
            new_word = word[:pos] + replacement + word[pos + len(pattern):]
            outcomes.add(new_word)
            start = pos + 1
    return list(outcomes)

#Генерю случайные переписывания до редексов в Т
def reduce_word(word: str, rules: dict[str, str]) -> list[str]:
    trace = [word]
    while True:
        next_words = rewrite(word, rules)
        if not next_words:
            break
        #случайное возможное применение
        word = random.choice(next_words)
        trace.append(word)
    return trace

#Проверяет достижимость old_w из new_w при данных правилах
def is_reachable(new_w: str, old_w: str, rules: dict[str, str]) -> bool:

    if new_w == old_w:
        return True

    queue = deque([new_w])
    visited = {new_w}

    while queue:
        word = queue.popleft()

        for next_word in rewrite(word, rules):
            if next_word in visited:
                continue
            if next_word == old_w:
                return True
            visited.add(next_word)
            queue.append(next_word)

    return False

#Генерация случайных тестов на эквивалентность систем T и T'
def fuzz_test(all_tests: int):

    success = fail = shown = 0

    for _ in range(all_tests):
        start = random_word(10, 25)
        seq = reduce_word(start, T)
        target = seq[-1]

        reachable = is_reachable(start, target, newT)
        if reachable:
            success += 1
            print(f"Старт:  {start}")
            print(f"Конец:  {target}")
            print(f"Цепочка: {seq}")
            print("Test passed, OK\n")
        else:
            fail += 1
            print(f"\nОшибка #{shown}")
            print(f"Старт:  {start}")
            print(f"Конец:  {target}")
            print(f"Цепочка: {seq}")
            print("Test failed, BAD\n")

    print(f"\nКол-во тестов: {success + fail}")
    print(f"Успех: {success}")
    print(f"Ошибки: {fail}")


if __name__ == "__main__":
    random.seed(13)
    fuzz_test(all_tests=10)