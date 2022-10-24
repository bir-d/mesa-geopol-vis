import random
import mesa
from mesa.space import NetworkGrid
from mesa.time import RandomActivationByType
import networkx as nx
from greenAgent import greenAgent

class populationModel(mesa.Model):
    def __init__(self, N, P, num_grey, percent_grey_bad, uncertainty_interval, percent_green_voters):
        self.num_agents = N
        self.edgeProbability = P
        self.uncertainty_interval = uncertainty_interval

        # Create the graph. We will use nx's Erdos-Renyi graph to represent a random graph of `N` nodes with `P` probability of an edge between any two nodes.
        self.graph = nx.erdos_renyi_graph(self.num_agents, self.edgeProbability)
        # Assign a random weight from 1-10 to each edge
        for (u, v) in self.graph.edges():
            self.graph.edges[u,v]['weight'] = random.randint(1,10) 

        # Feed graph into Mesa
        self.grid = NetworkGrid(self.graph)

        # Schedule that activates agents randomly by type (green, red, blue...) 
        self.schedule = RandomActivationByType(self)

        # Fill out the graph with agents and add them to the schedule
        for i, node in enumerate(self.graph.nodes()):
            if i == 0:
                # First agent is red
                pass
            elif i == 1:
                # Second agent is blue
                pass
            elif i < num_grey + 2:
                # Grey agents up to amount specified in num_grey, with percent_grey_bad of them being bad
                pass
            # else:
            # Green agents for the rest of the graph, with percent_green_voters of them being voters (i.e. opinion = 1)
            opinion = 1 if i < self.num_agents * percent_green_voters else 0
            a = greenAgent(i, self, self.uncertainty_interval, opinion)

            # Add node to graph and schedule
            self.schedule.add(a)
            self.grid.place_agent(a, node)

    # Finally, we just have the agents step in order of turns.
    def step(self):
        self.schedule.step_type(greenAgent)
        # self.schedule.step_type(redAgent)
        # self.schedule.step_type(blueAgent)

    # Utility functions
    def get_nodes_by_type(self, agentType):
        if agentType == "green":
            agentType = greenAgent
        # TODO add red and blue
        agent_keys: list[int] = list(self.schedule.agents_by_type[agentType].keys())
        return [self.schedule.agents_by_type[agentType][agent_key] for agent_key in agent_keys]
