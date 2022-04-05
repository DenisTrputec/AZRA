class InvestmentObject:
    def __init__(self, object_type, row_number, control_center, investment_id, item, code, name):
        self.type = object_type
        self.row_number = row_number
        self.cc = control_center
        self.id = investment_id
        self.item = item
        self.code = code
        self.name = name
        self.condition = None
        self.significance = None
        self.economy = None
        self.is_in_calculation = True
        self.rank = 0
        self.index = 0

    def __str__(self):
        return f"{self.name} C:{self.condition.index} S:{self.significance.index} I:{self.index}"

    def calculate_index(self, weight_factors):
        self.index = self.condition.index * float(weight_factors[0]) \
                     + self.significance.index * float(weight_factors[1]) \
                     + self.economy.index * float(weight_factors[2])
