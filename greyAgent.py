import mesa
import communications as comms

class greyAgent(mesa.Agent):
    def __init__(self, unique_id, model, opinion, active, isGood):
        super().__init__(unique_id, model)
        self.opinion = opinion
        self.active = active
        self.isGood = isGood
    
    def step(self):
        if self.active:
            if self.isGood:
                #TODO: Do grey nodes message at high potency?
                comms.pushBlueMessage(self.model, 5)
            else:
                comms.pushGreyBadMessage(self.model, 5)
            self.active = False
        