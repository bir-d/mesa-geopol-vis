import mesa
from mesa.space import NetworkGrid
from mesa.time import RandomActivationByType
import networkx as nx
from greenAgent import greenAgent


class populationModel(mesa.Model):
    def __init__(self, N, P, num_grey, percent_grey_bad, uncertainty_interval, percent_green_voters):
        self.num_agents = N
        self.edgeProbability = P

        # Create the graph. We will use nx's Erdos-Renyi graph to represent a random graph of `N` nodes with `P` probability of an edge between any two nodes.
        self.graph = nx.erdos_renyi_graph(self.num_agents, self.edgeProbability) # TODO: We need to add edge weightings to this.
        # Feed it into Mesa
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
                # Grey agents up to amount specified in num_grey
                pass
            else:
                # Green agents for the rest of the graph
                opinion = 1 if i < self.num_agents * percent_green_voters else 0
                a = greenAgent(i, self, uncertainty_interval, opinion)

            #add to graph
            self.schedule.add(a)
            self.grid.place_agent(a, node)

    # Finally, we just have the agents step in order of turns.
    def step(self):
        self.schedule.step_type(greenAgent)
        # self.schedule.step_type(redAgent)
        # self.schedule.step_type(blueAgent)
