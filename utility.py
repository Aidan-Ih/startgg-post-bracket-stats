import math
#Supports to 256 player brackets
placements = [1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193]

#gets the placement given a result
def get_placement(result):
    #wouldn't get many points in an algo class but it's fast enough with
    #a short list
    prev = 0
    for i in placements:
        if i <= result:
            prev = i
        else:
            return prev
    
#gets the SPR given a seed and placement
def get_seed_performance(seed, placement):
    expected = get_placement(seed)
    expected_index = placements.index(expected)
    actual_index = placements.index(placement)
    
    return expected_index - actual_index
    
def get_upset_factor(winner_seed, loser_seed):
    projected_loser = get_placement(loser_seed)
    return get_seed_performance(winner_seed, projected_loser)