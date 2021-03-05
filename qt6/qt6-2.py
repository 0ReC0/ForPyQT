import csv
# with open('ikea.csv', encoding="utf8") as csvfile:
#     reader = csv.reader(csvfile, delimiter=';', quotechar='"')
#     for index, row in enumerate(reader):
#         if index > 10:
#             break
#         print(row)

# with open('ikea.csv', encoding="utf8") as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
#     expensive = sorted(reader, key=lambda x: int(x['price']), reverse=True)
#
# for record in expensive[:10]:
#     print(record)

# with open('квадраты.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(
#         csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     for i in range(10):
#         writer.writerow([i, i ** 2, "Квадрат числа %d равен %d" % (i, i ** 2)])

data = [{
    'lastname': 'Иванов',
    'firstname': 'Пётр',
    'class_number': 9,
    'class_letter': 'А'
}, {
    'lastname': 'Кузнецов',
    'firstname': 'Алексей',
    'class_number': 9,
    'class_letter': 'В'
}, {
    'lastname': 'Меньшова',
    'firstname': 'Алиса',
    'class_number': 9,
    'class_letter': 'А'
}, {
    'lastname': 'Иванова',
    'firstname': 'Татьяна',
    'class_number': 9,
    'class_letter': 'Б'
}]

with open('dictwriter.csv', 'w', newline='') as f:
    writer = csv.DictWriter(
        f, fieldnames=list(data[0].keys()),
        delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for d in data:
        writer.writerow(d)