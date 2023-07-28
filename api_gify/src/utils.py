from . import config

def url_search(key_word:str, n_outputs=3):
    return config.URL_SEARCH + "?api_key=" + config.API_KEY + f"&limit={n_outputs + 1}" +f"&q={key_word}"

def extract_links(response, n_links=3):
    json_format = response.json()
    links = []
    for gif_number in range(n_links):
        links.append(json_format["data"][gif_number]['images']['original']['url'])
    return links

