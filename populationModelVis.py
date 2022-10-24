from time import sleep
import networkx as nx
import populationModel
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from greenAgent import greenAgent
from redAgent import redAgent
from blueAgent import blueAgent


class populationModelVis():
    def setValues(self):
        # Default values
        self.N = 15
        self.P = 0.2
        self.num_grey = 0
        self.percent_grey_bad = 0.5
        self.uncertainty_interval = (0,10)
        self.percent_green_voters = 0.8
        self.red_is_human = True
        self.blue_is_human = True

        # Ask if user wants to use default values, print defaults if input is ? or blank
        while True:
            selection = input("Use default values? (Y/n/?) ")
            if selection.lower() == "?":
                print("N =", self.N)
                print("P =", self.P)
                print("num_grey =", self.num_grey)
                print("percent_grey_bad =", self.percent_grey_bad)
                print("uncertainty_interval =", self.uncertainty_interval)
                print("percent_green_voters =", self.percent_green_voters)
                print("red_is_human =", self.red_is_human)
                print("blue_is_human =", self.blue_is_human)
            elif selection.lower() == "n":
                # Take user input for parameters
                self.N = int(input("Enter number of agents: "))
                self.P = float(input("Enter edge probability: "))
                self.num_grey = int(input("Enter number of grey agents: "))
                self.percent_grey_bad = float(input("Enter percentage of grey agents who are bad: "))
                self.uncertainty_interval = (float(input("Enter minimum uncertainty: ")), float(input("Enter maximum uncertainty: ")))
                self.percent_green_voters = float(input("Enter percentage of green agents who are voters: "))
                self.red_is_human = input("Is red agent human? (Y/n) ").lower() == "y"
                self.blue_is_human = input("Is blue agent human? (Y/n) ").lower() == "y"
            elif selection.lower() == "y" or selection == "":
                break

    def createModel(self):
        # create model
        self.model = populationModel.populationModel(self.N, self.P, self.num_grey, self.percent_grey_bad, self.uncertainty_interval, self.percent_green_voters, self.red_is_human, self.blue_is_human)
        self.pos = nx.circular_layout(self.model.graph)

    def drawModel(self):
        labels = nx.get_edge_attributes(self.model.graph,'weight')
        self.edges = nx.draw_networkx_edge_labels(self.model.graph, self.pos, edge_labels=labels)
       
        colors = []
        for node in self.model.graph.nodes():
            opinion = self.model.grid.get_cell_list_contents([node])[0].opinion
            if opinion == 1:
                colors.append("#00ff00") # green
            elif opinion == 0:
                colors.append("#ff00ff") # purple
            elif opinion == -1:
                colors.append("#ff0000") # red
            elif opinion == -2:
                colors.append("#0000ff") # blue

        self.f = nx.draw(
                    self.model.graph,
                    pos = self.pos,
                    with_labels= True,
                    # labels of nodes uncertainty except for red and blue
                    labels = {node: self.model.grid.get_cell_list_contents([node])[0].uncertainty for node in self.model.graph.nodes() if self.model.grid.get_cell_list_contents([node])[0].opinion not in [-1, -2]},
                    node_color = colors,
                )
        plt.draw()
    
    def drawButton(self):
        # axes for button on bottom right
        ax = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.button = Button(ax, 'Step')
        self.button.on_clicked(self.updateGraph)

    def updateGraph(self, event):
        for agentString in ["green", "red", "blue"]:
            print(f"\n{agentString}'s TURN")
            self.model.stepAgent(agentString)
            plt.clf()
            self.drawModel()
            self.drawButton()
            sleep(2)

    def __init__(self):
        self.setValues()
        self.createModel()
        self.drawModel()
        self.drawButton()

        plt.show()

vis = populationModelVis()