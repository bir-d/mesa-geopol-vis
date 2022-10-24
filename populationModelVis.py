from time import sleep
import networkx as nx
import populationModel
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class populationModelVis():
    def setValues(self):
        # Default values
        self.N = 50
        self.P = 0.0330
        self.num_grey = 4
        self.percent_grey_bad = 0.25
        self.uncertainty_interval = (0,100)
        self.percent_green_voters = 0.75
        self.red_is_human = "human"
        self.blue_is_human = True
        self.blue_energy = 15
        self.amount_turns = 10
        self.turnNumber = 0

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
                self.blue_energy = int(input("Enter blue agent's energy: "))
                self.amount_turns = int(input("Enter number of turns: "))
            elif selection.lower() == "y" or selection == "":
                break

    def createModel(self):
        # create model
        self.model = populationModel.populationModel(self.N, self.P, self.num_grey, self.percent_grey_bad, self.uncertainty_interval, self.percent_green_voters, self.red_is_human, self.blue_is_human, self.blue_energy, self.amount_turns)
        self.pos = nx.spring_layout(self.model.graph)

    def drawModel(self):
        labels = nx.get_edge_attributes(self.model.graph,'weight')
        self.edges = nx.draw_networkx_edge_labels(self.model.graph, self.pos, edge_labels=labels)
       
        colors = []
        for node in self.model.graph.nodes():
            agent = self.model.grid.get_cell_list_contents([node])[0]
            opinion = agent.opinion
            if opinion == 1: # green
                colors.append("#00ff00") 
            elif opinion == 0: # green (non-voter)
                colors.append("#ff00ff") # purple
            elif opinion == -1: # red
                colors.append("#ff0000") 
            elif opinion == -2: # blue
                colors.append("#0000ff") 
            elif opinion == -3: # grey
                if not agent.active:
                    colors.append((0,0,0,0.5)) #half opacity black
                else:
                    if agent.isGood:
                        colors.append((0.00600, 0.0654, 0.600, 1)) # dark blue, half opacity if inactive
                    else:
                        colors.append((0.600, 0.00600, 0.0258, 1)) # dark red, half opacity if inactive

        self.f = nx.draw(
                    self.model.graph,
                    pos = self.pos,
                    with_labels= True,
                    # labels of nodes uncertainty except for red and blue or grey
                    labels = {node: round(self.model.grid.get_cell_list_contents([node])[0].uncertainty, 1) for node in self.model.graph.nodes() if self.model.grid.get_cell_list_contents([node])[0].opinion not in [-1, -2, -3]},
                    node_color = colors,
                )
        plt.draw()
    
    def drawButton(self): # draw button to step model
        # axes for button on bottom right
        ax = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.button = Button(ax, 'Step')
        self.button.on_clicked(self.updateGraph)
    
    #draws parameters on bottom right
    def drawParams(self):
        current_voters = 0
        current_non_voters = 0
        for node in self.model.get_nodes_by_type("green"):
            if node.opinion == 1:
                current_voters += 1
            else:
                current_non_voters += 1

        params = ""
        params += f"N: {self.N}\n"
        params += f"P: {self.P}\n"
        params += f"num_grey: {self.num_grey}\n"
        params += f"percent_grey_bad: {self.percent_grey_bad}\n"
        params += f"uncertainty_interval: {self.uncertainty_interval}\n"
        params += f"percent_green_voters: {self.percent_green_voters}\n"
        params += f"red_is_human: {self.red_is_human}\n"
        params += f"blue_is_human: {self.blue_is_human}\n"
        params += f"blue_energy: {self.blue_energy}\n"
        params += f"amount_turns: {self.amount_turns}\n"

        stats = ""
        stats += f"current_green_voters: {current_voters}\n"
        stats += f"current_green_non_voters: {current_non_voters}\n"
        stats += f"current_green_voter_percentage: {round((current_voters / (current_voters + current_non_voters)) * 100, 2)}%\n"
        stats += f"turnNumber: {self.turnNumber}/{self.amount_turns}\n"

        self.paramsBox = plt.annotate(params, xy=(0, 0), xycoords='figure fraction')
        self.statsBox = plt.annotate(stats, xy=(0, 0.9), xycoords='figure fraction')

    def updateGraph(self, event):
        self.turnNumber += 1
        for agentString in ["green", "red", "blue", "grey"]:
            print(f"\n{agentString}'s TURN")
            self.model.stepAgent(agentString)
            plt.clf()
            self.drawModel()
            if self.turnNumber < self.amount_turns:                
                self.drawButton()
            self.drawParams()
            plt.draw()
            plt.pause(2)

    def __init__(self):
        self.setValues()
        self.createModel()
        self.drawModel()
        self.drawButton()
        self.drawParams()

        plt.show()

vis = populationModelVis()