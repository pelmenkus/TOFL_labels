import re

regex = re.compile(r'^(ab?c|ba?c)*ba.[ab][bc]$') # сокращенная регулярка

def match_by_regex(word: str) -> bool:
    return bool(regex.fullmatch(word))