import csv

DEFAULT_FILENAME = "players.csv"


def dict_to_csv(d, fields, filename=DEFAULT_FILENAME):
    rows = [[k, *v] for k, v in d.items()]
    with open(filename, "w", encoding="utf-8", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(fields)
        for row in rows:
            csv_writer.writerow(row)


def csv_to_dict(filename: str = DEFAULT_FILENAME):
    csv_dict = {}
    with open(filename, "r", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        csv_reader = list(csv_reader)
        fields = csv_reader.pop(0)
        for row in csv_reader:
            csv_dict[row[0]] = list(
                map(lambda i: int(i) if i.isdigit() else i, row[1:])
            )
    return fields, csv_dict


if __name__ == "__main__":
    fields, d = csv_to_dict()
    print(fields)
