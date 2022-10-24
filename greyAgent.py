import mesa
import communications as comms

class greyAgent(mesa.Agent):
    def __init__(self, unique_id, model, opinion, active, isGood):
        super().__init__(unique_id, model)
        self.opinion = opinion
        self.active = active
        self.isGood = isGood
        print(opinion, active, isGood)
    
    def step(self):
        if self.active:
            if self.isGood:
                comms.pushBlueMessage(self.model, potency)
            else:
                comms.pushGreyBadMessage(self.model, potency)
            self.active = False
        