import csv
import json

def convert_date_format(original):
    date, month, year = original.split('/')
    return year + '-' + month + '-' + date

def create_row_dict(row, cumulative_count):
    name = row[6]
    modified_date = convert_date_format(row[1])

    if name not in cumulative_count:
        cumulative_count[name] = 0
    cumulative_count[name] += 1

    return {
        "date": modified_date,
        "name": name,
        "category": name,
        "value": cumulative_count[name]
        }

data = []
with open("confirmed-cases.csv", encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line = 0
    cumulative_count = {}
    for row in csv_reader:
        if line == 0:
            pass
        else:
            row_dict = create_row_dict(row, cumulative_count)
            if row_dict["name"] == "" and row_dict["category"] == "":
                row_dict["name"] = "Unknown"
                row_dict["category"] = "Unknown"
            current_index = len(data) - 1
            while current_index >= 0 and data[current_index]["date"] == row_dict["date"]:
                if data[current_index]["name"] == row_dict["name"]:
                    data.pop(current_index)
                current_index -= 1
            data.append(row_dict)
            
        line += 1

with open('covid_by_nationality.json', 'w') as f:
    json.dump(data, f)