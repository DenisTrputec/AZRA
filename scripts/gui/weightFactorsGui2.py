from scripts.envVars import formWeightFactorsWindow2, baseWeightFactorsWindow2
from scripts.enumValues import ObjectType
from scripts.weightFactors import WeightFactors


class WeightFactorsWindow2(baseWeightFactorsWindow2, formWeightFactorsWindow2):
    def __init__(self, main_window):
        main_window.logDebug.info("Call:WeightFactorsWindow2.__init__()")
        super(baseWeightFactorsWindow2, self).__init__()
        self.setupUi(self)
        self.__pwin = main_window
        self.weight_factors_line = None
        self.weight_factors_trafo_large = None
        self.weight_factors_trafo_medium = None
        self.weight_factors_station = None
        self.load_data()
        self.__pwin.logDebug.info("Return:WeightFactorsWindow2.__init__()")
        self.__pwin.logInfo.info("Opened WeightFactorsWindow2")

    def load_data(self):
        self.lblError.setText("")
        try:
            self.weight_factors_line = WeightFactors(self.__pwin, self, ObjectType.Line)
            self.weight_factors_trafo_large = WeightFactors(self.__pwin, self, ObjectType.TransformerLarge)
            self.weight_factors_trafo_medium = WeightFactors(self.__pwin, self, ObjectType.TransformerMedium)
            self.weight_factors_station = WeightFactors(self.__pwin, self, ObjectType.Station)
            self.set_values()
        except Exception as e:
            self.__pwin.logDebug.exception(e)
            self.lblError.setText(e.args[0])
            # self.lblError.setText("Greška prilikom učitavanja težinskih faktora!")

    def set_values(self):
        # Line
        self.lbl1.setText(f"{float(self.weight_factors_line.data['condition'][0]):.2f}")
        self.lbl2.setText(f"{float(self.weight_factors_line.data['condition'][1]):.2f}")
        self.lbl3.setText(f"{float(self.weight_factors_line.data['condition'][2]):.2f}")
        self.lbl4.setText(f"{float(self.weight_factors_line.data['condition'][3]):.2f}")
        self.lbl5.setText(f"{float(self.weight_factors_line.data['condition'][4]):.2f}")
        self.lbl6.setText(f"{float(self.weight_factors_line.data['significance'][0]):.2f}")
        self.lbl7.setText(f"{float(self.weight_factors_line.data['significance'][1]):.2f}")
        self.lbl8.setText(f"{float(self.weight_factors_line.data['significance'][2]):.2f}")
        self.lbl9.setText(f"{float(self.weight_factors_line.data['significance'][3]):.2f}")
        self.lbl10.setText(f"{float(self.weight_factors_line.data['significance'][4]):.2f}")
        self.lbl11.setText(f"Stanje: {float(self.weight_factors_line.data['all'][0]):.1f}")
        self.lbl12.setText(f"Značaj: {float(self.weight_factors_line.data['all'][1]):.1f}")
        self.lbl13.setText(f"Ekonomija: {float(self.weight_factors_line.data['all'][2]):.1f}")

        # Transfomer Large
        self.lbl21.setText(f"{float(self.weight_factors_trafo_large.data['condition'][0]):.2f}")
        self.lbl22.setText(f"{float(self.weight_factors_trafo_large.data['condition'][1]):.2f}")
        self.lbl23.setText(f"{float(self.weight_factors_trafo_large.data['condition'][2]):.2f}")
        self.lbl24.setText(f"{float(self.weight_factors_trafo_large.data['significance'][0]):.2f}")
        self.lbl25.setText(f"{float(self.weight_factors_trafo_large.data['significance'][1]):.2f}")
        self.lbl26.setText(f"{float(self.weight_factors_trafo_large.data['significance'][2]):.2f}")
        self.lbl27.setText(f"Stanje: {float(self.weight_factors_trafo_large.data['all'][0]):.1f}")
        self.lbl28.setText(f"Značaj: {float(self.weight_factors_trafo_large.data['all'][1]):.1f}")
        self.lbl29.setText(f"Ekonomija: {float(self.weight_factors_trafo_large.data['all'][2]):.1f}")

        # Transfomer Medium
        self.lbl41.setText(f"{float(self.weight_factors_trafo_medium.data['condition'][0]):.2f}")
        self.lbl42.setText(f"{float(self.weight_factors_trafo_medium.data['condition'][1]):.2f}")
        self.lbl43.setText(f"{float(self.weight_factors_trafo_medium.data['condition'][2]):.2f}")
        self.lbl44.setText(f"{float(self.weight_factors_trafo_medium.data['significance'][0]):.2f}")
        self.lbl45.setText(f"{float(self.weight_factors_trafo_medium.data['significance'][1]):.2f}")
        self.lbl46.setText(f"{float(self.weight_factors_trafo_medium.data['significance'][2]):.2f}")
        self.lbl47.setText(f"Stanje: {float(self.weight_factors_trafo_medium.data['all'][0]):.1f}")
        self.lbl48.setText(f"Značaj: {float(self.weight_factors_trafo_medium.data['all'][1]):.1f}")
        self.lbl49.setText(f"Ekonomija: {float(self.weight_factors_trafo_medium.data['all'][2]):.1f}")

        # Station
        self.lbl61.setText(f"{float(self.weight_factors_station.data['condition'][0]):.2f}")
        self.lbl62.setText(f"{float(self.weight_factors_station.data['condition'][1]):.2f}")
        self.lbl63.setText(f"{float(self.weight_factors_station.data['condition'][2]):.2f}")
        self.lbl64.setText(f"{float(self.weight_factors_station.data['condition'][3]):.2f}")
        self.lbl65.setText(f"{float(self.weight_factors_station.data['condition'][4]):.2f}")
        self.lbl66.setText(f"{float(self.weight_factors_station.data['significance'][0]):.2f}")
        self.lbl67.setText(f"{float(self.weight_factors_station.data['significance'][1]):.2f}")
        self.lbl68.setText(f"{float(self.weight_factors_station.data['significance'][2]):.2f}")
        self.lbl69.setText(f"{float(self.weight_factors_station.data['significance'][3]):.2f}")
        self.lbl70.setText(f"{float(self.weight_factors_station.data['significance'][4]):.2f}")
        self.lbl71.setText(f"Stanje: {float(self.weight_factors_station.data['all'][0]):.1f}")
        self.lbl72.setText(f"Značaj: {float(self.weight_factors_station.data['all'][1]):.1f}")
        self.lbl73.setText(f"Ekonomija: {float(self.weight_factors_station.data['all'][2]):.1f}")
