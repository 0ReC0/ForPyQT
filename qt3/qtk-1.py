def check_number(inp_number):
    if not ("+7" == inp_number[:2] or "8" == inp_number[0]):
        return 404
    if "\t" in inp_number:
        return 404
    inp_number.replace(" ", "")
    if not inp_number.count("(") == inp_number.count(")"):
        return 404
    if "--" in inp_number or inp_number[0] == '-' or inp_number[-1] == '-':
        return 404
    number = "".join(filter(str.isdigit, inp_number))
    if len(number) != 11:
        return 404
    if number[0] == "8" or number[0] == "7":
        number = "+7" + number[1:]
    return number


if __name__ == '__main__':
    inp_number = input().strip()
    number = check_number(inp_number)
    if number == 404:
        print("error")
    else:
        print(number)
