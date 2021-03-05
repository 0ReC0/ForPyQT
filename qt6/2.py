import csv
import sys

# with open('input.txt') as inp_file:
data = map(lambda line: line.rstrip().split("\t"), sys.stdin.readlines())
with open("plantis.csv", encoding="utf-8", mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    field_names = "nomen, definitio, pluma, Russian nomen, familia, Russian nomen familia".split(", ")
    writer.writerow(field_names)
    for line in data:
        writer.writerow(line)