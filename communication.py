import networkx as nx

# Contains functions to communicate with the population

# Push a message to all green agents on the grid.
# The message is either "good" or "bad" (vote, and not vote)
# The sender is either "red", "blue", or "grey", but right now only red is used as we don't touch nodes uncertainty if the message is coming from a grey or blue node.
# The potency is the strength of the message, and is a number between 0 and 5
# This number represents the fraction of the uncertainty interval that will have their opinion changed by the message.

max_potency = 5

def getUncertaintyThreshold(potency, uncertainty_interval):
    """Takes the potency as a percentage (given potency / max potency) and then gives the threshold in which nodes with uncertainty above it will change their opinion"""
    min = uncertainty_interval[0]
    max = uncertainty_interval[1]
    percentage = potency / max_potency
    return ((min - max) * percentage) + max

def pushRedMessage(grid, potency, uncertainty_interval):
    threshold = getUncertaintyThreshold(potency, uncertainty_interval)
    # Iterate through all nodes, if their uncertainty is high enough, change their opinion.
    for node in grid.get_all_cell_contents():
        if node.opinion > threshold:
            node.opinion = 0
            # For now we will have their uncertainty increase by the percentage of the potency (a max potency will double the uncertainty)
            node.uncertainty = max(
                                    (node.uncertainty * (1 + potency / max_potency)),
                                    uncertainty_interval[1]
                                )

def pushBlueMessage(grid, potency, uncertainty_interval):
    # Same logic as pushRedMessage, but we will change the opinion to 1 instead, as well as not change the uncertainty ( Blue team pays with energy instead )
    threshold = getUncertaintyThreshold(potency, uncertainty_interval)
    for node in grid.get_all_cell_contents():
        if node.opinion > threshold:
            node.opinion = 1


# A GreyGood will just push via pushBlueMessage(), so we only need a function for GreyBad
# TODO: Will a greyBad always push at max potency? For now we will assume they do. 
def pushGreyBadMessage(grid, potency, uncertainty_interval):
    potency = max_potency
    threshold = getUncertaintyThreshold(potency, uncertainty_interval)
    for node in grid.get_all_cell_contents():
        if node.opinion > threshold:
            node.opinion = 0

