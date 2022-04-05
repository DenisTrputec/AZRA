class Significance:
    def __init__(self, **kwargs):
        self.transmission_capacity_increase_need = kwargs.pop('transmission_capacity_increase_need', None)
        self.section_safety = kwargs.pop('section_safety', None)
        self.permanent_unavailability_risk = kwargs.pop('permanent_unavailability_risk', None)
        self.damage_evaluation = kwargs.pop('damage_evaluation', None)
        self.revitalization_infulance = kwargs.pop('revitalization_infulance', None)
        self.transmitted_energy = kwargs.pop('transmitted_energy', None)
        self.max_load_app_power_ratio = kwargs.pop('max_load_app_power_ratio', None)
        self.short_circuit_level = kwargs.pop('short_circuit_level', None)
        self.annual_energy = kwargs.pop('annual_energy', None)
        self.downtime_risk = kwargs.pop('downtime_risk', None)
        self.downtime_damage = kwargs.pop('downtime_damage', None)
        self.planned_connections_number = kwargs.pop('planned_connections_number', None)
        self.index = 0

    def calculate_revitalization_influance(self, max_influance):
        return self.revitalization_infulance / max_influance if max_influance != 0 else 0

    def calculate_transmitted_energy(self, max_transmitted_energy):
        return self.transmitted_energy / max_transmitted_energy if max_transmitted_energy != 0 else 0

    def calculate_max_load_app_power_ratio(self, max_ratio):
        return self.max_load_app_power_ratio / max_ratio if max_ratio != 0 else 0

    def calculate_annual_energy(self, max_energy):
        return self.annual_energy / max_energy if max_energy != 0 else 0

    def calculate_index_line(self, weight_factors, max_influance):
        self.index = self.transmission_capacity_increase_need * float(weight_factors[0]) \
                     + self.section_safety * float(weight_factors[1]) \
                     + self.permanent_unavailability_risk * float(weight_factors[2]) \
                     + self.damage_evaluation * float(weight_factors[3]) \
                     + self.calculate_revitalization_influance(max_influance) * float(weight_factors[4])

    def calculate_index_trafo_large(self, weight_factors):
        self.index = self.section_safety * float(weight_factors[0]) \
                     + self.damage_evaluation * float(weight_factors[1]) \
                     + self.permanent_unavailability_risk * float(weight_factors[2])

    def calculate_index_trafo_med(self, weight_factors, max_transmitted_energy, max_ratio):
        self.index = self.calculate_transmitted_energy(max_transmitted_energy) * float(weight_factors[0]) \
                     + self.calculate_max_load_app_power_ratio(max_ratio) * float(weight_factors[1]) \
                     + self.damage_evaluation * float(weight_factors[2])

    def calculate_index_station(self, weight_factors, max_energy):
        self.index = self.short_circuit_level * float(weight_factors[0]) \
                     + self.calculate_annual_energy(max_energy) * float(weight_factors[1]) \
                     + self.downtime_risk * float(weight_factors[2]) \
                     + self.downtime_damage * float(weight_factors[3]) \
                     + self.planned_connections_number * float(weight_factors[4])
