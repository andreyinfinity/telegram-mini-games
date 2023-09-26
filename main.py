import json


with open("data/hh-areas.json", "r", encoding="utf-8") as file:
    data = json.load(file)

cities = []

for item in data[0]["areas"]:
    for i in item["areas"]:
        if "(" in i["name"]:
            continue
        cities.append(i["name"])

with open("data/cities.json", "w", encoding="utf-8") as file:
    json.dump(cities, file, ensure_ascii=False)

print(cities)