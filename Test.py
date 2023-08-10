import json
with open("My Collection.postman_collection.json") as f:
    parsered = json.load(f)
    print(parsered['info'])

