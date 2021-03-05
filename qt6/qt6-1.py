with open('ikea.txt', encoding='utf-8') as file:
    data = file.read()

    # Посмотрим, как работать с таким форматом в Python. Тут нет ничего сложного, поскольку у нас есть мощная
    # функциональность по работе со строками, в частности, метод split.
    # for row in data.split('\n')[:10]:
    #     print(row.split('\t'))

    # Вспомним списочные выражения и сразу сделаем «двумерный массив», а потом обратимся к цене пятого по счету товара:
    table = [r.split('\t') for r in data.split('\n')]
    # print(table[5][1])

    # Мы можем также отсортировать элементы по цене и напечатать 10 самых дешевых товаров:
    table = table[1:]
    table.sort(key=lambda x: int(x[1]))
    for r in table[:10]:
        print(r)