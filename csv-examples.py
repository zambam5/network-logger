import csv

total = 0
lines = 0
with open("nile.csv", "r", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip the first line
    for row in reader:
        total += float(row[1])  # need float for the decimals
        lines += 1
average = total / lines

with open("nile.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    newrow = ["Average", average]
    writer.writerow(newrow)
