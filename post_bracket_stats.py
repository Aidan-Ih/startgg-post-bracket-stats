#!/usr/bin/env python
from api_requests import get_entrants_from_slug, get_sets_from_slug
from utility import get_seed_performance, get_upset_factor
import argparse

# get event_id from command line
parser = argparse.ArgumentParser(description='Generates post bracket stats for a start.gg double elimination event')
parser.add_argument('slug', help="The slug after the /tournament/ in the url")
parser.add_argument('event_name', help="The name of the event in the bracket")
args = parser.parse_args()
slug = args.slug
event_name = args.event_name

# get start.gg token from dotfile
try:
    f = open(".token", "r")
except FileNotFoundError:
    print(".token file does not exist, see README for instructions")
    quit()
    
token = f.readline()

#TODO generate SPR ranking
def get_spr():
    entrants = get_entrants_from_slug(slug, event_name, token)
    spr_tuple_list = []
    for entrant in entrants:
        seed = entrant["initialSeed"]
        placement = entrant["standing"]
        SPR = get_seed_performance(seed, placement)
        spr_tuple_list.append((entrant["name"], SPR))
        
    spr_tuple_list = sorted(spr_tuple_list, key=lambda x: x[1], reverse=True)
    for i in spr_tuple_list:
        print(i)

def get_uf():
    sets = get_sets_from_slug(slug, event_name, token)
    #TODO generate upset factor
    uf_tuple_list = []
        
    for s in sets:
        player1 = s["player1"]
        player2 = s["player2"]
        if player1[2] == 1:
            winner = player1
            loser = player2
        else:
            winner = player2
            loser = player1
            
        UF = get_upset_factor(winner[1], loser[1])
        uf_tuple_list.append((winner[0], loser[0], UF))
    
    uf_tuple_list = sorted(uf_tuple_list, key=lambda x: x[2], reverse=True)
    
    for i in uf_tuple_list:
        print(i)            

print("\n ### SEED PERFORMANCE RANKING### \n")
get_spr()
print("\n ### UPSET FACTORS ### \n")
get_uf()
