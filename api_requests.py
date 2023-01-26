import requests

#gets the event ID from the slug of the tournament, and the event name
def get_event_id(slug, event_name, token):
    url = "https://api.start.gg/gql/alpha"
    headers = {"Authorization": "Bearer " + token}
    query = """
    query Tournaments($slug_name: String!) {
        tournament(slug: $slug_name) {
            id
            name
            events {
                id
                name
            }
        }
    }
    """    
    variables = {
        "slug_name": slug
    }
    
    to_send = {"query": query,
               "variables": variables}
    
    response = requests.post(url, json=to_send, headers=headers)
    events = response.json()["data"]["tournament"]["events"]
    for event in events:
        if event["name"] == event_name:
            return event["id"]
    
    return -1

#returns an array of entrants with their name, seed, id, and placement
def get_entrants(token, id):
    url = "https://api.start.gg/gql/alpha"
    headers = {"Authorization": "Bearer " + token}
    query = """
    query EventEntrants($eventId: ID!, $page: Int!, $perPage: Int!) {
        event(id: $eventId) {
            id
            name
            entrants(query: {
                page: $page
                perPage: $perPage
            }) {
                pageInfo {
                    total
                    totalPages
                }
                nodes {
                    name
                    initialSeedNum
                    standing {
                        placement
                    }
                    participants {
                        player {
                            id
                        }
                    }
                }
            }
        }
    }
    """    
    variables = {
    "eventId": id,
    "page": 1,
    "perPage": 50
    }
    to_send = {"query": query,
                         "variables": variables}
    
    players = []
    curr_page = 0
    info = {"totalPages": 1}
    
    while(curr_page < info["totalPages"]):
        curr_page += 1
        variables["page"] = curr_page
        response = requests.post(url, json=to_send, headers=headers)
        try:
            data = response.json()["data"]["event"]["entrants"]
        except:
            print(response)
        info = data["pageInfo"]
        players += data["nodes"]
        
    players = [{"name": x["name"], "initialSeed": x["initialSeedNum"], "id": x["participants"][0]["player"]["id"], "standing": x["standing"]["placement"]} for x in players]
    sorted_players = sorted(players, key=lambda x: x["initialSeed"])
    return sorted_players
  
def get_sets(token, id):
    url = "https://api.start.gg/gql/alpha"
    headers = {"Authorization": "Bearer " + token}
    query = """
    query EventSets($eventId: ID!, $page: Int!, $perPage: Int!) {
        event(id: $eventId) {
            sets(
                page: $page
                perPage: $perPage
            ) {
                pageInfo {
                    total
                    totalPages
                }
                nodes {
                    id
                    slots {
                      id
                      seed {
                          seedNum
                      }
                      standing {
                          placement
                      }
                      entrant {
                        id
                        name
                      }
                    }
                }
            }
        }
    }
    """    
    variables = {
    "eventId": id,
    "page": 1,
    "perPage": 50
    }
    to_send = {"query": query,
               "variables": variables}
    
    sets = []
    curr_page = 0
    info = {"totalPages": 1}
    
    while(curr_page < info["totalPages"]):
        curr_page += 1
        variables["page"] = curr_page
        response = requests.post(url, json=to_send, headers=headers)
        data = response.json()["data"]["event"]["sets"]
        info = data["pageInfo"]
        nodes = data["nodes"]
        these_sets = [{"id": node["id"], 
                       "player1": (node["slots"][0]["entrant"]["name"], 
                                   node["slots"][0]["seed"]["seedNum"],
                                   node["slots"][0]["standing"]["placement"]), 
                       "player2": (node["slots"][1]["entrant"]["name"],
                                   node["slots"][1]["seed"]["seedNum"],
                                   node["slots"][1]["standing"]["placement"])} for node in nodes]
        sets += these_sets
    
    return(sets)
    
def get_entrants_from_slug(slug, event_name, token):
    event_id = get_event_id(slug, event_name, token)
    return get_entrants(token, event_id)

def get_sets_from_slug(slug, event_name, token):
    event_id = get_event_id(slug, event_name, token)
    return get_sets(token, event_id)
    