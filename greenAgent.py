import mesa

class greenAgent(mesa.Agent):
    def __init__(self, unique_id, model, uncertainty_interval, opinion):
        super().__init__(unique_id, model)
        # TODO: Look into ways to initialise uncertainty of the agent. Random uncertainty?
        # For now we will have agents who start at minimum uncertainty
        self.uncertainty = uncertainty_interval[0] # Uncertainty interval is a tuple of min and max uncertainty, so we take the 0th
        self.opinion = opinion