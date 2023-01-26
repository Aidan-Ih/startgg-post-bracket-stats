import requests

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

#sets = get_sets("6d0d769a0294cc2068c96080115056f5", 828710)
#for s in sets:
#  print(s)
#print(len(sets))