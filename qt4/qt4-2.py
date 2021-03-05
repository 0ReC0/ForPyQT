table_replacements = {
    "й": "j", "ц": "c", "у": "u", "к": "k", "е": "e", "н": "n",
    "г": "g", "ш": "sh", "щ": "shh", "з": "z", "х": "h", "ъ": "#",
    "ф": "f", "ы": "y", "в": "v", "а": "a", "п": "p", "р": "r",
    "о": "o", "л": "l", "д": "d", "ж": "zh", "э": "je", "я": "ya",
    "ч": "ch", "с": "s", "м": "m", "и": "i", "т": "t", "ь": "'",
    "б": "b", "ю": "ju", "ё": "jo"
}

with open('cyrillic.txt', encoding="utf-8") as inp_file:
    with open('transliteration.txt', encoding="utf-8", mode="w") as out_file:
        def replace_symb(current_symb):
            if current_symb.isupper():
                return table_replacements.get(current_symb.lower(), current_symb).title()
            return table_replacements.get(current_symb, current_symb)

        replaced_text = "".join(map(replace_symb, inp_file.read()))
        out_file.write(replaced_text)
