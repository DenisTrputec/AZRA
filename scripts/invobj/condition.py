class Condition:
    def __init__(self, **kwargs):
        self.year = kwargs.pop('year_of_construction')
        self.technical_condition = kwargs.pop('technical_condition', None)
        self.unavailability = kwargs.pop('unavailability', None)
        self.examination_and_diagnostics = kwargs.pop('examination_and_diagnostics', None)
        self.other_indicators = kwargs.pop('other_indicators', None)
        self.condition_primary_equipment = kwargs.pop('condition_primary_equipment', None)
        self.condition_secondary_equipment = kwargs.pop('condition_secondary_equipment', None)
        self.condition_auxiliary_equipment = kwargs.pop('condition_auxiliary_equipment', None)
        self.condition_construction_parts = kwargs.pop('condition_construction_parts', None)
        self.index = 0

    def calculate_age(self, observed_year, max_age):
        return (observed_year - self.year) / max_age if max_age != 0 else 0

    def calculate_unavailability(self, max_unavailability):
        return self.unavailability / max_unavailability if max_unavailability != 0 else 0

    def calculate_index_line(self, weight_factors, observed_year, max_age, max_unavailability):
        self.index = self.technical_condition * float(weight_factors[0]) \
                     + self.calculate_age(observed_year, max_age) * float(weight_factors[1]) \
                     + self.calculate_unavailability(max_unavailability) * float(weight_factors[2]) \
                     + self.examination_and_diagnostics * float(weight_factors[3]) \
                     + self.other_indicators * float(weight_factors[4])

    def calculate_index_trafo_large(self, weight_factors, observed_year, max_age, max_unavailability):
        self.index = self.examination_and_diagnostics * float(weight_factors[0]) \
                     + self.calculate_age(observed_year, max_age) * float(weight_factors[1]) \
                     + self.calculate_unavailability(max_unavailability) * float(weight_factors[2])

    def calculate_index_trafo_med(self, weight_factors, observed_year, max_age, max_unavailability):
        self.index = self.examination_and_diagnostics * float(weight_factors[0]) \
                     + self.calculate_age(observed_year, max_age) * float(weight_factors[1]) \
                     + self.calculate_unavailability(max_unavailability) * float(weight_factors[2])

    def calculate_index_station(self, weight_factors, observed_year, max_age):
        self.index = self.calculate_age(observed_year, max_age) * float(weight_factors[0]) \
                     + self.condition_primary_equipment * float(weight_factors[1]) \
                     + self.condition_secondary_equipment * float(weight_factors[2]) \
                     + self.condition_auxiliary_equipment * float(weight_factors[3]) \
                     + self.condition_construction_parts * float(weight_factors[4])
