import re

regex = re.compile(r'^(ab?c|ba?c)*ba.[ab][bc]$')  # ВСТАВИТЬ ВАШЕ регулярное выражение

def match_by_regex(word: str) -> bool:
    return bool(regex.fullmatch(word))