import random
import mesa

class greenAgent(mesa.Agent):
    def __init__(self, unique_id, model, uncertainty_interval, opinion):
        super().__init__(unique_id, model)
        self.uncertainty = random.randint(uncertainty_interval[0], uncertainty_interval[1])
        self.opinion = opinion

    # Talk to an agent, if their uncertainty is lower than ours we will change to their opinion.
    # If we change opinions, we will take halfway between our and their opinion (A node who is very certain will make us more certain than a less certain node)
    def talk(self, agent):

        if agent.uncertainty < self.uncertainty:
            self.opinion = agent.opinion
            self.uncertainty = (self.uncertainty + agent.uncertainty) / 2

    def step(self):
        # Get a list of adjacent node ids and iterate
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        for neighbor in neighbors:
            # Get the agent at the node
            agent = self.model.grid.get_cell_list_contents([neighbor])[0]
            # Get a random int from 1 to 10, if its less or equal to the weight (which represents probability of interaction) we can talk to them.
            if (self.model.graph.edges[self.pos, neighbor]['weight'] >= random.randint(1,10)) and (isinstance(agent, greenAgent)): # we can only talk to other green agents
                # Talk to them.
                self.talk(agent)