class Economy:
    def __init__(self, enpv):
        self.enpv = enpv
        self.index = 0

    def calculate_economic_indicator(self, max_enpv):
        return self.enpv / max_enpv if self.enpv > 0 else 0

    def calculate_index(self, weight_factors, max_enpv):
        self.index = self.calculate_economic_indicator(max_enpv) * float(weight_factors[0])

