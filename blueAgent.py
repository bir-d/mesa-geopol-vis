import mesa
import communications as comms

class blueAgent(mesa.Agent):
    def __init__(self, unique_id, model, human, opinion, energy):
        super().__init__(unique_id, model)
        self.human = human
        self.opinion = opinion # used for plotting
        self.energy = energy # Energy level of the agent. potency is subtracted directly from here so use a low number
    
    def humanStep(self, potency = False, grey = False):
        # ask user for potency of message if not given
        print("Your energy level is: " + str(self.energy))
        # ask if user would like to release a grey agent
        answer = input("Would you like to release a grey agent? (y/n): ")
        if answer == "y":
            greys = self.model.get_nodes_by_type("grey", True) # pass randomize then we can just activate the first one
            greys[0].active = True
        else:
            potency = int(input("Enter potency of message: "))
            self.updateEnergy(potency)
            comms.pushBlueMessage(self.model, potency)

    def updateEnergy(self, potency):
        self.energy = self.energy - potency

    def step(self):
        if self.human:
            self.humanStep()