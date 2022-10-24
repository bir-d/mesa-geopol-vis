import random
import mesa
from mesa.space import NetworkGrid
from mesa.time import RandomActivationByType
import networkx as nx
from greenAgent import greenAgent
from redAgent import redAgent
from blueAgent import blueAgent
from greyAgent import greyAgent

class populationModel(mesa.Model):
    def __init__(self, N, P, num_grey, percent_grey_bad, uncertainty_interval, percent_green_voters, red_is_human, blue_is_human):
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
        num_green = self.num_agents - num_grey - 1 - 1 # -1 for red, -1 for blue
        greenCount = 0
        greyCount = 0
        for i, node in enumerate(self.graph.nodes()):
            if i == 0:
                # First agent is red
                a = redAgent(i, self, red_is_human, -1)
            elif i == 1:
                # Second agent is blue
                a = blueAgent(i, self, blue_is_human, -2, 100)
            elif i < num_grey + 2:
                # Grey agents up to amount specified in num_grey, with percent_grey_bad of them being bad
                greyCount += 1
                isGood = False if greyCount < num_grey * percent_grey_bad else True
                a = greyAgent(i, self, -3, False, isGood)
            else:
                # Green agents for the rest of the graph, with percent_green_voters of them being voters (i.e. opinion = 1)
                greenCount += 1
                opinion = 1 if greenCount < num_green * percent_green_voters else 0
                a = greenAgent(i, self, self.uncertainty_interval, opinion)

            # Add node to graph and schedule
            self.schedule.add(a)
            self.grid.place_agent(a, node)

    # Stepping by type handled by user (right now in populationModelVis.py)
    def stepAgent(self, agentString):
        agentType = self.get_agentType_from_agentString(agentString)
        self.schedule.step_type(agentType)

    def get_agentType_from_agentString(self, agentString):
        if agentString == "green":
            return greenAgent
        elif agentString == "red":
            return redAgent
        elif agentString == "blue":
            return blueAgent
        elif agentString == "grey":
            return greyAgent
        else:
            raise Exception("Invalid agentString")

    # Utility functions
    def get_nodes_by_type(self, agentString, randomize=False):
        agentType = self.get_agentType_from_agentString(agentString)
        agent_keys: list[int] = list(self.schedule.agents_by_type[agentType].keys())
        if randomize:
            random.shuffle(agent_keys)
        return [self.schedule.agents_by_type[agentType][agent_key] for agent_key in agent_keys]

