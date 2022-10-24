# Contains functions to communicate with the population

# The potency is the strength of the message, and is a number between 0 and 5
# This number represents the fraction of the uncertainty interval that will have their opinion changed by the message.

max_potency = 5

def getUncertaintyThreshold(potency, uncertainty_interval):
    """Takes the potency as a percentage (given potency / max potency) and then gives the threshold in which nodes with uncertainty above it will change their opinion"""
    min = uncertainty_interval[0]
    max = uncertainty_interval[1]
    percentage = potency / max_potency
    return ((min - max) * percentage) + max

def pushRedMessage(model, potency):
    uncertainty_interval = model.uncertainty_interval
    threshold = getUncertaintyThreshold(potency, uncertainty_interval)

    # Iterate through all nodes, if their uncertainty is high enough, change their opinion.
    for node in model.get_nodes_by_type("green"):
        if node.uncertainty > threshold:
            node.opinion = 0
            # For now we will have their uncertainty increase by the percentage of the potency (a max potency will double the uncertainty)
            node.uncertainty = min(
                                    ((node.uncertainty + 1) * (1 + (potency / max_potency))),
                                    uncertainty_interval[1]
                                ) # We need to clamp uncertainty here to the upper bound of the interval

def pushBlueMessage(model, potency):
    # Same logic as pushRedMessage, but we will change the opinion to 1 instead, as well as not change the uncertainty ( Blue team pays with energy instead )
    uncertainty_interval = model.uncertainty_interval
    threshold = getUncertaintyThreshold(potency, uncertainty_interval)

    for node in model.get_nodes_by_type("green"):
        if node.uncertainty > threshold:
            node.opinion = 1
            # Blue nodes have the opposite effect of red nodes on uncertainty, think of it as the government being more stable, more trustworthy than red's underhanded techniques.
            node.uncertainty = max(
                                    ((node.uncertainty) * ((potency / max_potency)/2)),
                                    uncertainty_interval[0]
                                ) # We need to clamp uncertainty here to the lower bound of the interval


# A GreyGood will just push via pushBlueMessage(), so we only need a function for GreyBad
def pushGreyBadMessage(model, potency):
    uncertainty_interval = model.uncertainty_interval
    threshold = getUncertaintyThreshold(potency, uncertainty_interval)

    for node in model.get_nodes_by_type("green"):
        if node.uncertainty > threshold:
            node.opinion = 0

