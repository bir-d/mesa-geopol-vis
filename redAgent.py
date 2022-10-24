import mesa
import communications as comms

class redAgent(mesa.Agent):
    def __init__(self, unique_id, model, human, opinion):
        super().__init__(unique_id, model)
        self.human = human
        self.opinion = opinion # used for plotting
    
    def humanStep(self, potency = False):
        # ask user for potency of message if not already given
        if not potency:
            potency = int(input("Enter potency of message: "))
        comms.pushRedMessage(self.model, potency)
        
    def step(self):
        if self.human:
            self.humanStep()