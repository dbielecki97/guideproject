import requests
key = 'AIzaSyArdvkTXE1oDlhs3VbJ4KJGYZtclFj79Hg'


def search_place(query):
    search_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    inputType = 'textQuery'
    language = 'pl'
    search_payload = {"key": key, "inputtype": inputType,
                      "query": query, "language": language}
    search_req = requests.get(search_url, params=search_payload)
    search_json = search_req.json()
    return search_json['results'][0]


def search_for_photo(photoreference):
    photo_url = 'https://maps.googleapis.com/maps/api/place/photo?'
    photo_payload = {"key": key, "photoreference": photoreference,
                     "maxheight": 500, "maxwidth": 500}
    photo_req = requests.get(photo_url, params=photo_payload)
    return photo_req.content


if __name__ == '__main__':
    search_place("Pałac Branickich")
