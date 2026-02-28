import re
import random


TOKEN_PATTERN = re.compile(r"<\d+,[ST],\d+>|[abST]")


# ---------- чтение грамматики ----------

def load_rules(filename: str):
    productions = {}
    start_symbol = None

    with open(filename, "r") as f:
        for row in f:
            row = row.strip()
            if not row:
                continue

            left, right = row.split("->", 1)
            left = left.strip()
            symbols = tuple(TOKEN_PATTERN.findall(right.strip()))

            productions.setdefault(left, []).append(symbols)

            if start_symbol is None:
                start_symbol = left

    return productions, start_symbol


# ---------- Earley-подобный распознаватель ----------

def recognize(grammar, start, text: str) -> bool:
    length = len(text)
    nonterms = set(grammar.keys())

    def is_nt(sym):
        return sym in nonterms

    # создаём искусственный стартовый символ
    augmented = start + "_start"
    while augmented in nonterms:
        augmented += "_"

    # chart[i] — множество состояний в позиции i
    chart = [set() for _ in range(length + 1)]
    chart[0].add((augmented, (start,), 0, 0))

    for pos in range(length + 1):
        updated = True

        while updated:
            updated = False

            for state in list(chart[pos]):
                lhs, rhs, dot, origin = state

                # завершённая продукция
                if dot == len(rhs):
                    for prev in list(chart[origin]):
                        plhs, prhs, pdot, porigin = prev
                        if pdot < len(prhs) and prhs[pdot] == lhs:
                            new_state = (plhs, prhs, pdot + 1, porigin)
                            if new_state not in chart[pos]:
                                chart[pos].add(new_state)
                                updated = True
                    continue

                next_symbol = rhs[dot]

                # предсказание
                if is_nt(next_symbol):
                    for prod in grammar.get(next_symbol, []):
                        new_state = (next_symbol, prod, 0, pos)
                        if new_state not in chart[pos]:
                            chart[pos].add(new_state)
                            updated = True
                    continue

                # сканирование
                if pos < length and text[pos] == next_symbol:
                    new_state = (lhs, rhs, dot + 1, origin)
                    chart[pos + 1].add(new_state)

    return (augmented, (start,), 1, 0) in chart[length]


# ---------- добавление общего стартового символа ----------

def attach_start(grammar, accepting_states):
    grammar["S0"] = [(f"<0,S,{i}>",) for i in accepting_states]
    return "S0"


# ---------- генерация тестовых слов ----------

def random_words(count=20, max_len=10):
    result = []
    for _ in range(count):
        size = random.randint(0, max_len)
        result.append("".join(random.choice("ab") for _ in range(size)))
    return result


# ---------- основной тест ----------

base_rules, base_start = load_rules("grammar.txt")

ll_rules, _ = load_rules("../intersect_rules/LL(1).txt")
ll_start = attach_start(ll_rules, [3, 4])

lr_rules, _ = load_rules("../intersect_rules/LR(0).txt")
lr_start = attach_start(lr_rules, [4, 5])

tests = random_words()

print("Слово\tКС\tLL1\tLR0")

ok = True

for word in tests:
    res_base = recognize(base_rules, base_start, word)
    res_ll = recognize(ll_rules, ll_start, word)
    res_lr = recognize(lr_rules, lr_start, word)

    equal = (res_base == res_ll == res_lr)
    if not equal:
        ok = False

    shown = word if word else "ε"
    row = f"{shown}\t{res_base}\t{res_ll}\t{res_lr}"
    if not equal:
        row += "\tразличие"

    print(row)

if ok:
    print("Все результаты совпали")
