import requests
import imghdr
key = 'AIzaSyArdvkTXE1oDlhs3VbJ4KJGYZtclFj79Hg'


def search_place(query):
    search_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    inputType = 'textQuery'
    language = 'pl'
    search_payload = {"key": key, "inputtype": inputType,
                      "query": query+" Białystok", "language": language}
    search_req = requests.get(search_url, params=search_payload)
    search_json = search_req.json()
    return search_json['results'][0]


if __name__ == '__main__':
    print(search_place('Rynek Kościuszki'))
