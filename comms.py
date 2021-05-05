import sys
sys.path.append("..")
import json

def update_json_data(key, value):
    access_file = open("data.json", "r")
    json_object = json.load(access_file)
    access_file.close()

    json_object[key] = value

    access_file = open("data.json", "w")
    json.dump(json_object, access_file, indent=4)
    access_file.close()


def view_json_data(key_input):

    try:
        with open('data.json') as f:
            data = json.load(f)
            f.close()
        return data[key_input]
    except Exception as e:
        print("an exception occured - {}".format(e))
        view_data(name, key)

