import mesa
import communications as comms

class redAgent(mesa.Agent):
    def __init__(self, unique_id, model, ai, opinion):
        super().__init__(unique_id, model)
        self.ai = ai
        self.opinion = opinion # used for plotting
        if self.ai == "smart"
            self.smartInit()
    
    def humanStep(self):
        # ask user for potency of message if not already given
        potency = int(input("Enter potency of message: "))
        comms.pushRedMessage(self.model, potency)

    def getDistribution(self):
        num_voters = 0
        num_non_voters = 0
        for node in self.model.get_nodes_by_type("green"):
            if node.opinion == 1:
                num_voters += 1
            else:
                num_non_voters += 1
        return num_voters, num_non_voters

    def percentageStep(self):
        num_voters, num_non_voters = self.getDistribution()
        percentage = num_voters / (num_voters + num_non_voters)
        if percentage > 0.0:
            potency = 1
        elif percentage > 0.20:
            potency = 2
        elif percentage > 0.40:
            potency = 3
        elif percentage > 0.60:
            potency = 4
        elif percentage > 0.80:
            potency = 5
        comms.pushRedMessage(self.model, potency)
    
    def smartInit(self):
        self.last_num_voters, self.last_num_non_voters = self.getDistribution()

    def smartStep(self):
        # Tries to infer what potency blue just used and matches it. If it can't infer, it uses percentageStep
        num_voters, num_non_voters = self.getDistribution()
        last_percentage = self.last_num_voters / (self.last_num_voters + self.last_num_non_voters)
        percentage = num_voters / (num_voters + num_non_voters)
        percentage_change = percentage - last_percentage

        if percentage_change >= 0.0:
            potency = 1
        elif percentage_change > 0.20:
            potency = 2
        elif percentage_change > 0.40:
            potency = 3
        elif percentage_change > 0.60:
            potency = 4
        elif percentage_change > 0.80:
            potency = 5
        else:
            self.percentageStep()
            return

    def step_from_args(self, potency):
        comms.pushRedMessage(self.model, potency)


    def step(self):
        if self.ai == "human":
            self.humanStep()
        if self.ai == "random":
            potency = random.randint(1,10)
            self.step_from_args(potency)
        if self.ai == "percentage"
            self.percentageStep()
        