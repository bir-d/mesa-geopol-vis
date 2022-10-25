import mesa
import communications as comms

class redAgent(mesa.Agent):
    def __init__(self, unique_id, model, ai, opinion):
        super().__init__(unique_id, model)
        self.ai = ai
        self.opinion = opinion # used for plotting
        self.smartInitialised = False
        self.learningInitialised = False
    
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
        print(percentage)
        if percentage > 0.0 and percentage <= 0.20:
            potency = 1
        elif percentage > 0.20 and percentage <= 0.40:
            potency = 2
        elif percentage > 0.40 and percentage <= 0.60:
            potency = 3
        elif percentage > 0.60 and percentage <= 0.80:
            potency = 4
        elif percentage > 0.80 and percentage <= 1:
            potency = 5
        comms.pushRedMessage(self.model, potency)
    
    def learningInit(self):
        self.last_num_voters, self.last_num_non_voters = self.getDistribution()
        self.gamma = 100
        self.bins = input("Enter number of bins: ")
        self.minGamma = input("Enter minimum gamma: ")
        self.gammaDecay = 1 - (input("Enter gamma decay: "))
        self.learningTable = []
        for i in range(0, 100, int(100/self.bins)):
            self.learningTable.append([[i], [0, 0, 0, 0, 0]])
        self.learning = False

    def learningStep(self):
        if not self.learningInitialised:
            self.learningInit()
            self.learningInitialised = True

        self.num_voters, self.num_non_voters = self.getDistribution()
        percentage = num_voters / (num_voters + num_non_voters)

        if self.learning:
            bin = percentage // self.bins
            percentage_change = percentage - self.last_percentage
            self.learningTable[bin][1][self.potency - 1] = percentage_change
            self.learning = False

        if random.random() < self.gamma:
            self.potency = random.randint(1,5)
            self.step_from_args(self.potency)
            self.last_percentage = percentage
            self.learning = True
            self.gamma = self.gamma * self.gammaDecay
        else:
            bin = percentage // self.bins
            maxReward, self.potency = max(self.learningTable[bin][1]), self.learningTable[bin][1].index(max(self.learningTable[bin][1]))
            if maxReward == 0:
                self.potency = random.randint(1,5)
                self.step_from_args(self.potency)
                self.last_percentage = percentage
                self.learning = True
                self.step_from_args(self.potency)  
            else:
                self.step_from_args(self.potency)



    def smartInit(self):
        self.last_num_voters, self.last_num_non_voters = self.getDistribution()

    def smartStep(self):
        if not self.smartInitialised:
            self.smartInit()
            self.smartInitialised = True

        # Tries to infer what potency blue just used and matches it. If it can't infer, it uses percentageStep
        # Red agents cant see uncertainty, so if Blue uses a high potency message, red might think it was a low potency message
        num_voters, num_non_voters = self.getDistribution()
        last_percentage = self.last_num_voters / (self.last_num_voters + self.last_num_non_voters)
        percentage = num_voters / (num_voters + num_non_voters)
        percentage_change = percentage - last_percentage

        print(f"last percentage: {last_percentage}, current percentage: {percentage}, percentage change: {percentage_change}")

        if percentage_change > 0.0 and percentage_change <= 0.20:
            potency = 1
        elif percentage_change > 0.20 and percentage_change <= 0.40:
            potency = 2
        elif percentage_change > 0.40 and percentage_change <= 0.60:
            potency = 3
        elif percentage_change > 0.60 and percentage_change <= 0.80:
            potency = 4
        elif percentage_change > 0.80 and percentage_change <= 1:
            potency = 5
        else:
            self.percentageStep()
            return
        comms.pushRedMessage(self.model, potency)

    def step_from_args(self, potency):
        comms.pushRedMessage(self.model, potency)


    def step(self):
        if self.ai == "human":
            self.humanStep()
        if self.ai == "random":
            potency = random.randint(1,10)
            self.step_from_args(potency)
        if self.ai == "percentage":
            self.percentageStep()
        if self.ai == "smart":
            self.smartStep()
        