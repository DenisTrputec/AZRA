import os
import csv
from random import choice
from string import hexdigits
from PyQt5.QtWidgets import QMessageBox
from scripts.envVars import ADMIN_PASSWORD, WEIGHT_FACTORS_FILEPATH, WEIGHT_FACTORS_FOLDER
from scripts.envVars import formWeightFactorsWindow, baseWeightFactorsWindow
from scripts.weightFactors import WeightFactors
from scripts.enumValues import ObjectType
from scripts.crypto import CryptoFile


class WeightFactorsWindow(baseWeightFactorsWindow, formWeightFactorsWindow):
    def __init__(self, main_window):
        main_window.logDebug.info("Call:WeightFactorsWindow.__init__()")
        super(baseWeightFactorsWindow, self).__init__()
        self.setupUi(self)
        self.__pwin = main_window
        self.__temp_filepath = os.path.join(WEIGHT_FACTORS_FOLDER, "".join(choice(hexdigits) for i in range(16)))
        self.__weight_factors_filepath = WEIGHT_FACTORS_FILEPATH
        self.__password = ADMIN_PASSWORD
        self.weight_factors_line = None
        self.weight_factors_trafo_large = None
        self.weight_factors_trafo_medium = None
        self.weight_factors_station = None
        self.load_data()
        self.connect_signals()
        self.is_changed = False
        self.__pwin.logDebug.info("Return:WeightFactorsWindow.__init__()")
        self.__pwin.logInfo.info("Opened WeightFactorsWindow")

    def load_data(self):
        self.lblError.setText("")
        try:
            self.weight_factors_line = WeightFactors(self.__pwin, self, ObjectType.Line)
            self.weight_factors_trafo_large = WeightFactors(self.__pwin, self, ObjectType.TransformerLarge)
            self.weight_factors_trafo_medium = WeightFactors(self.__pwin, self, ObjectType.TransformerMedium)
            self.weight_factors_station = WeightFactors(self.__pwin, self, ObjectType.Station)
            if self.__pwin.temp_wf is None:
                self.set_values()
            else:
                self.set_temp_values()

            self.calculate_line_sums()
            self.calculate_trafo_large_sums()
            self.calculate_trafo_medium_sums()
            self.calculate_station_sums()
        except Exception as e:
            self.__pwin.logDebug.exception(e)
            self.error_message(e.args[0])
            # self.error_message("Greška prilikom učitavanja težinskih faktora!")
            self.change_label_color("red", self.lblError)

    # <editor-fold desc="#####  Calculate sums  #####">

    def calculate_line_sums(self):
        condition_sum = self.sbLineCondition1.value() + self.sbLineCondition2.value() + self.sbLineCondition3.value() \
                        + self.sbLineCondition4.value() + self.sbLineCondition5.value()
        significance_sum = self.sbLineSignificance1.value() + self.sbLineSignificance2.value() \
                           + self.sbLineSignificance3.value() + self.sbLineSignificance4.value() \
                           + self.sbLineSignificance5.value()

        self.lblError.setText("")
        self.lblLineConditionSum.setText(str(condition_sum))
        self.lblLineSignificanceSum.setText(str(significance_sum))
        if condition_sum != significance_sum:
            self.change_label_color("red", self.lblLineConditionSum, self.lblLineSignificanceSum)
            return False
        else:
            self.change_label_color("black", self.lblLineConditionSum, self.lblLineSignificanceSum)
            return True

    def calculate_trafo_large_sums(self):
        condition_sum = self.sbTrafoLargeCondition1.value() + self.sbTrafoLargeCondition2.value() \
                        + self.sbTrafoLargeCondition3.value()
        significance_sum = self.sbTrafoLargeSignificance1.value() + self.sbTrafoLargeSignificance2.value() \
                           + self.sbTrafoLargeSignificance3.value()

        self.lblError.setText("")
        self.lblTrafoLargeConditionSum.setText(str(condition_sum))
        self.lblTrafoLargeSignificanceSum.setText(str(significance_sum))
        if condition_sum != significance_sum:
            self.change_label_color("red", self.lblTrafoLargeConditionSum, self.lblTrafoLargeSignificanceSum)
            return True
        else:
            self.change_label_color("black", self.lblTrafoLargeConditionSum, self.lblTrafoLargeSignificanceSum)
            return True

    def calculate_trafo_medium_sums(self):
        condition_sum = self.sbTrafoMediumCondition1.value() + self.sbTrafoMediumCondition2.value() \
                        + self.sbTrafoMediumCondition3.value()
        significance_sum = self.sbTrafoMediumSignificance1.value() + self.sbTrafoMediumSignificance2.value() \
                           + self.sbTrafoMediumSignificance3.value()

        self.lblError.setText("")
        self.lblTrafoMediumConditionSum.setText(str(condition_sum))
        self.lblTrafoMediumSignificanceSum.setText(str(significance_sum))
        if condition_sum != significance_sum:
            self.change_label_color("red", self.lblTrafoMediumConditionSum, self.lblTrafoMediumSignificanceSum)
            return False
        else:
            self.change_label_color("black", self.lblTrafoMediumConditionSum, self.lblTrafoMediumSignificanceSum)
            return True

    def calculate_station_sums(self):
        condition_sum = self.sbStationCondition1.value() + self.sbStationCondition2.value() \
                        + self.sbStationCondition3.value() + self.sbStationCondition4.value() \
                        + self.sbStationCondition5.value()
        significance_sum = self.sbStationSignificance1.value() + self.sbStationSignificance2.value() \
                           + self.sbStationSignificance3.value() + self.sbStationSignificance4.value() \
                           + self.sbStationSignificance5.value()

        self.lblStationConditionSum.setText(str(condition_sum))
        self.lblStationSignificanceSum.setText(str(significance_sum))
        if condition_sum != significance_sum:
            self.change_label_color("red", self.lblStationConditionSum, self.lblStationSignificanceSum)
            return False
        else:
            self.change_label_color("black", self.lblStationConditionSum, self.lblStationSignificanceSum)
            return True

    # </editor-fold>

    def error_message(self, text):
        self.change_label_color(self.lblError)
        self.lblError.setText(text)

    @staticmethod
    def change_label_color(color, *args):
        for arg in args:
            arg.setStyleSheet("color: " + color)

    def connect_signals(self):
        self.btnSave.clicked.connect(self.save_changes)
        self.btnLoad.clicked.connect(self.load_data)
        self.btnSaveTemp.clicked.connect(self.save_temp_changes)

        self.sbLineCondition1.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))
        self.sbLineCondition2.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))
        self.sbLineCondition3.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))
        self.sbLineCondition4.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))
        self.sbLineCondition5.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))
        self.sbLineSignificance1.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))
        self.sbLineSignificance2.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))
        self.sbLineSignificance3.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))
        self.sbLineSignificance4.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))
        self.sbLineSignificance5.valueChanged.connect(lambda: self.value_changed(self.calculate_line_sums))

        self.sbTrafoLargeCondition1.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_large_sums))
        self.sbTrafoLargeCondition2.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_large_sums))
        self.sbTrafoLargeCondition3.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_large_sums))
        self.sbTrafoLargeSignificance1.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_large_sums))
        self.sbTrafoLargeSignificance2.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_large_sums))
        self.sbTrafoLargeSignificance3.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_large_sums))

        self.sbTrafoMediumCondition1.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_medium_sums))
        self.sbTrafoMediumCondition2.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_medium_sums))
        self.sbTrafoMediumCondition3.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_medium_sums))
        self.sbTrafoMediumSignificance1.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_medium_sums))
        self.sbTrafoMediumSignificance2.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_medium_sums))
        self.sbTrafoMediumSignificance3.valueChanged.connect(lambda: self.value_changed(self.calculate_trafo_medium_sums))

        self.sbStationCondition1.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))
        self.sbStationCondition2.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))
        self.sbStationCondition3.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))
        self.sbStationCondition4.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))
        self.sbStationCondition5.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))
        self.sbStationSignificance1.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))
        self.sbStationSignificance2.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))
        self.sbStationSignificance3.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))
        self.sbStationSignificance4.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))
        self.sbStationSignificance5.valueChanged.connect(lambda: self.value_changed(self.calculate_station_sums))

        self.sbLineAll1.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbLineAll2.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbLineAll3.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbTrafoLargeAll1.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbTrafoLargeAll2.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbTrafoLargeAll3.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbTrafoMediumAll1.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbTrafoMediumAll2.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbTrafoMediumAll3.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbStationAll1.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbStationAll2.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))
        self.sbStationAll3.valueChanged.connect(lambda: self.value_changed(lambda: self.lblError.setText("")))

    def set_values(self):
        self.sbLineCondition1.setValue(float(self.weight_factors_line.data['condition'][0]))
        self.sbLineCondition2.setValue(float(self.weight_factors_line.data['condition'][1]))
        self.sbLineCondition3.setValue(float(self.weight_factors_line.data['condition'][2]))
        self.sbLineCondition4.setValue(float(self.weight_factors_line.data['condition'][3]))
        self.sbLineCondition5.setValue(float(self.weight_factors_line.data['condition'][4]))
        self.sbLineSignificance1.setValue(float(self.weight_factors_line.data['significance'][0]))
        self.sbLineSignificance2.setValue(float(self.weight_factors_line.data['significance'][1]))
        self.sbLineSignificance3.setValue(float(self.weight_factors_line.data['significance'][2]))
        self.sbLineSignificance4.setValue(float(self.weight_factors_line.data['significance'][3]))
        self.sbLineSignificance5.setValue(float(self.weight_factors_line.data['significance'][4]))
        self.sbLineAll1.setValue(float(self.weight_factors_line.data['all'][0]))
        self.sbLineAll2.setValue(float(self.weight_factors_line.data['all'][1]))
        self.sbLineAll3.setValue(float(self.weight_factors_line.data['all'][2]))

        self.sbTrafoLargeCondition1.setValue(float(self.weight_factors_trafo_large.data['condition'][0]))
        self.sbTrafoLargeCondition2.setValue(float(self.weight_factors_trafo_large.data['condition'][1]))
        self.sbTrafoLargeCondition3.setValue(float(self.weight_factors_trafo_large.data['condition'][2]))
        self.sbTrafoLargeSignificance1.setValue(float(self.weight_factors_trafo_large.data['significance'][0]))
        self.sbTrafoLargeSignificance2.setValue(float(self.weight_factors_trafo_large.data['significance'][1]))
        self.sbTrafoLargeSignificance3.setValue(float(self.weight_factors_trafo_large.data['significance'][2]))
        self.sbTrafoLargeAll1.setValue(float(self.weight_factors_trafo_large.data['all'][0]))
        self.sbTrafoLargeAll2.setValue(float(self.weight_factors_trafo_large.data['all'][1]))
        self.sbTrafoLargeAll3.setValue(float(self.weight_factors_trafo_large.data['all'][2]))

        self.sbTrafoMediumCondition1.setValue(float(self.weight_factors_trafo_medium.data['condition'][0]))
        self.sbTrafoMediumCondition2.setValue(float(self.weight_factors_trafo_medium.data['condition'][1]))
        self.sbTrafoMediumCondition3.setValue(float(self.weight_factors_trafo_medium.data['condition'][2]))
        self.sbTrafoMediumSignificance1.setValue(float(self.weight_factors_trafo_medium.data['significance'][0]))
        self.sbTrafoMediumSignificance2.setValue(float(self.weight_factors_trafo_medium.data['significance'][1]))
        self.sbTrafoMediumSignificance3.setValue(float(self.weight_factors_trafo_medium.data['significance'][2]))
        self.sbTrafoMediumAll1.setValue(float(self.weight_factors_trafo_medium.data['all'][0]))
        self.sbTrafoMediumAll2.setValue(float(self.weight_factors_trafo_medium.data['all'][1]))
        self.sbTrafoMediumAll3.setValue(float(self.weight_factors_trafo_medium.data['all'][2]))

        self.sbStationCondition1.setValue(float(self.weight_factors_station.data['condition'][0]))
        self.sbStationCondition2.setValue(float(self.weight_factors_station.data['condition'][1]))
        self.sbStationCondition3.setValue(float(self.weight_factors_station.data['condition'][2]))
        self.sbStationCondition4.setValue(float(self.weight_factors_station.data['condition'][3]))
        self.sbStationCondition5.setValue(float(self.weight_factors_station.data['condition'][4]))
        self.sbStationSignificance1.setValue(float(self.weight_factors_station.data['significance'][0]))
        self.sbStationSignificance2.setValue(float(self.weight_factors_station.data['significance'][1]))
        self.sbStationSignificance3.setValue(float(self.weight_factors_station.data['significance'][2]))
        self.sbStationSignificance4.setValue(float(self.weight_factors_station.data['significance'][3]))
        self.sbStationSignificance5.setValue(float(self.weight_factors_station.data['significance'][4]))
        self.sbStationAll1.setValue(float(self.weight_factors_station.data['all'][0]))
        self.sbStationAll2.setValue(float(self.weight_factors_station.data['all'][1]))
        self.sbStationAll3.setValue(float(self.weight_factors_station.data['all'][2]))

    def set_temp_values(self):
        self.sbLineCondition1.setValue(float(self.__pwin.temp_wf['Line'].data['condition'][0]))
        self.sbLineCondition2.setValue(float(self.__pwin.temp_wf['Line'].data['condition'][1]))
        self.sbLineCondition3.setValue(float(self.__pwin.temp_wf['Line'].data['condition'][2]))
        self.sbLineCondition4.setValue(float(self.__pwin.temp_wf['Line'].data['condition'][3]))
        self.sbLineCondition5.setValue(float(self.__pwin.temp_wf['Line'].data['condition'][4]))
        self.sbLineSignificance1.setValue(float(self.__pwin.temp_wf['Line'].data['significance'][0]))
        self.sbLineSignificance2.setValue(float(self.__pwin.temp_wf['Line'].data['significance'][1]))
        self.sbLineSignificance3.setValue(float(self.__pwin.temp_wf['Line'].data['significance'][2]))
        self.sbLineSignificance4.setValue(float(self.__pwin.temp_wf['Line'].data['significance'][3]))
        self.sbLineSignificance5.setValue(float(self.__pwin.temp_wf['Line'].data['significance'][4]))
        self.sbLineAll1.setValue(float(self.__pwin.temp_wf['Line'].data['all'][0]))
        self.sbLineAll2.setValue(float(self.__pwin.temp_wf['Line'].data['all'][1]))
        self.sbLineAll3.setValue(float(self.__pwin.temp_wf['Line'].data['all'][2]))

        self.sbTrafoLargeCondition1.setValue(float(self.__pwin.temp_wf['TransformerLarge'].data['condition'][0]))
        self.sbTrafoLargeCondition2.setValue(float(self.__pwin.temp_wf['TransformerLarge'].data['condition'][1]))
        self.sbTrafoLargeCondition3.setValue(float(self.__pwin.temp_wf['TransformerLarge'].data['condition'][2]))
        self.sbTrafoLargeSignificance1.setValue(float(self.__pwin.temp_wf['TransformerLarge'].data['significance'][0]))
        self.sbTrafoLargeSignificance2.setValue(float(self.__pwin.temp_wf['TransformerLarge'].data['significance'][1]))
        self.sbTrafoLargeSignificance3.setValue(float(self.__pwin.temp_wf['TransformerLarge'].data['significance'][2]))
        self.sbTrafoLargeAll1.setValue(float(self.__pwin.temp_wf['TransformerLarge'].data['all'][0]))
        self.sbTrafoLargeAll2.setValue(float(self.__pwin.temp_wf['TransformerLarge'].data['all'][1]))
        self.sbTrafoLargeAll3.setValue(float(self.__pwin.temp_wf['TransformerLarge'].data['all'][2]))

        self.sbTrafoMediumCondition1.setValue(float(self.__pwin.temp_wf['TransformerMedium'].data['condition'][0]))
        self.sbTrafoMediumCondition2.setValue(float(self.__pwin.temp_wf['TransformerMedium'].data['condition'][1]))
        self.sbTrafoMediumCondition3.setValue(float(self.__pwin.temp_wf['TransformerMedium'].data['condition'][2]))
        self.sbTrafoMediumSignificance1.setValue(float(self.__pwin.temp_wf['TransformerMedium'].data['significance'][0]))
        self.sbTrafoMediumSignificance2.setValue(float(self.__pwin.temp_wf['TransformerMedium'].data['significance'][1]))
        self.sbTrafoMediumSignificance3.setValue(float(self.__pwin.temp_wf['TransformerMedium'].data['significance'][2]))
        self.sbTrafoMediumAll1.setValue(float(self.__pwin.temp_wf['TransformerMedium'].data['all'][0]))
        self.sbTrafoMediumAll2.setValue(float(self.__pwin.temp_wf['TransformerMedium'].data['all'][1]))
        self.sbTrafoMediumAll3.setValue(float(self.__pwin.temp_wf['TransformerMedium'].data['all'][2]))

        self.sbStationCondition1.setValue(float(self.__pwin.temp_wf['Station'].data['condition'][0]))
        self.sbStationCondition2.setValue(float(self.__pwin.temp_wf['Station'].data['condition'][1]))
        self.sbStationCondition3.setValue(float(self.__pwin.temp_wf['Station'].data['condition'][2]))
        self.sbStationCondition4.setValue(float(self.__pwin.temp_wf['Station'].data['condition'][3]))
        self.sbStationCondition5.setValue(float(self.__pwin.temp_wf['Station'].data['condition'][4]))
        self.sbStationSignificance1.setValue(float(self.__pwin.temp_wf['Station'].data['significance'][0]))
        self.sbStationSignificance2.setValue(float(self.__pwin.temp_wf['Station'].data['significance'][1]))
        self.sbStationSignificance3.setValue(float(self.__pwin.temp_wf['Station'].data['significance'][2]))
        self.sbStationSignificance4.setValue(float(self.__pwin.temp_wf['Station'].data['significance'][3]))
        self.sbStationSignificance5.setValue(float(self.__pwin.temp_wf['Station'].data['significance'][4]))
        self.sbStationAll1.setValue(float(self.__pwin.temp_wf['Station'].data['all'][0]))
        self.sbStationAll2.setValue(float(self.__pwin.temp_wf['Station'].data['all'][1]))
        self.sbStationAll3.setValue(float(self.__pwin.temp_wf['Station'].data['all'][2]))

    def value_changed(self, func):
        self.is_changed = True
        self.lblError.setText("")
        func()
        self.__pwin.logInfo.info("Value changed")

    def save_changes(self):
        if not self.is_changed:
            return

        if not (self.calculate_line_sums() and self.calculate_trafo_large_sums()
                and self.calculate_trafo_medium_sums() and self.calculate_station_sums()):
            self.error_message("Sume u barem jednoj od kartica nisu jednake!")
            self.change_label_color("red", self.lblError)
            return

        ans = self.yes_no_question("Jeste li sigurni da želite pohraniti promjene?")
        if ans:
            with open(self.__temp_filepath, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=',')
                csv_writer.writerow(["Line", "condition", self.sbLineCondition1.value(),
                                     self.sbLineCondition2.value(), self.sbLineCondition3.value(),
                                     self.sbLineCondition4.value(), self.sbLineCondition5.value()])
                csv_writer.writerow(["Line", "significance", self.sbLineSignificance1.value(),
                                     self.sbLineSignificance2.value(), self.sbLineSignificance3.value(),
                                     self.sbLineSignificance4.value(), self.sbLineSignificance5.value()])
                csv_writer.writerow(["Line", "all", self.sbLineAll1.value(),
                                     self.sbLineAll2.value(), self.sbLineAll3.value()])
                csv_writer.writerow(["TransformerLarge", "condition", self.sbTrafoLargeCondition1.value(),
                                     self.sbTrafoLargeCondition2.value(), self.sbTrafoLargeCondition3.value()])
                csv_writer.writerow(["TransformerLarge", "significance", self.sbTrafoLargeSignificance1.value(),
                                     self.sbTrafoLargeSignificance2.value(), self.sbTrafoLargeSignificance3.value()])
                csv_writer.writerow(["TransformerLarge", "all", self.sbTrafoLargeAll1.value(),
                                     self.sbTrafoLargeAll2.value(), self.sbTrafoLargeAll3.value()])
                csv_writer.writerow(["TransformerMedium", "condition", self.sbTrafoMediumCondition1.value(),
                                     self.sbTrafoMediumCondition2.value(), self.sbTrafoMediumCondition3.value()])
                csv_writer.writerow(["TransformerMedium", "significance", self.sbTrafoMediumSignificance1.value(),
                                     self.sbTrafoMediumSignificance2.value(), self.sbTrafoMediumSignificance3.value()])
                csv_writer.writerow(["TransformerMedium", "all", self.sbTrafoMediumAll1.value(),
                                     self.sbTrafoMediumAll2.value(), self.sbTrafoMediumAll3.value()])
                csv_writer.writerow(["Station", "condition", self.sbStationCondition1.value(),
                                     self.sbStationCondition2.value(), self.sbStationCondition3.value(),
                                     self.sbStationCondition4.value(), self.sbStationCondition5.value()])
                csv_writer.writerow(["Station", "significance", self.sbStationSignificance1.value(),
                                     self.sbStationSignificance2.value(), self.sbStationSignificance3.value(),
                                     self.sbStationSignificance4.value(), self.sbStationSignificance5.value()])
                csv_writer.writerow(["Station", "all", self.sbStationAll1.value(),
                                     self.sbStationAll2.value(), self.sbStationAll3.value()])

            CryptoFile.encrypt(self.__pwin, self.__temp_filepath, self.__weight_factors_filepath, self.__password)
            os.remove(self.__temp_filepath)

            self.is_changed = False
            self.error_message("Promjene su spremljene!")
            self.change_label_color("green", self.lblError)
            self.__pwin.logInfo.info("WEIGHT FACTOR CHANGES WERE SAVED")

    def save_temp_changes(self):
        if not (self.calculate_line_sums() and self.calculate_trafo_large_sums()
                and self.calculate_trafo_medium_sums() and self.calculate_station_sums()):
            self.error_message("Sume u barem jednoj od kartica nisu jednake!")
            self.change_label_color("red", self.lblError)
            return

        self.__pwin.temp_wf = {'Line': {'condition': [], 'significance': [], 'all': []},
                               'TransformerLarge': {'condition': [], 'significance': [], 'all': []},
                               'TransformerMedium': {'condition': [], 'significance': [], 'all': []},
                               'Station': {'condition': [], 'significance': [], 'all': []}}

        temp_data = {'Line': {
                        'condition': [self.sbLineCondition1.value(), self.sbLineCondition2.value(),
                                      self.sbLineCondition3.value(), self.sbLineCondition4.value(),
                                      self.sbLineCondition5.value()],
                        'significance': [self.sbLineSignificance1.value(), self.sbLineSignificance2.value(),
                                         self.sbLineSignificance3.value(), self.sbLineSignificance4.value(),
                                         self.sbLineSignificance5.value()],
                        'all': [self.sbLineAll1.value(), self.sbLineAll2.value(), self.sbLineAll3.value()]
                     },
                     'TransformerLarge': {
                         'condition': [self.sbTrafoLargeCondition1.value(), self.sbTrafoLargeCondition2.value(),
                                       self.sbTrafoLargeCondition3.value()],
                         'significance': [self.sbTrafoLargeSignificance1.value(), self.sbTrafoLargeSignificance2.value(),
                                          self.sbTrafoLargeSignificance3.value()],
                         'all': [self.sbTrafoLargeAll1.value(), self.sbTrafoLargeAll2.value(), self.sbTrafoLargeAll3.value()]
                     },
                     'TransformerMedium': {
                         'condition': [self.sbTrafoMediumCondition1.value(), self.sbTrafoMediumCondition2.value(),
                                       self.sbTrafoMediumCondition3.value()],
                         'significance': [self.sbTrafoMediumSignificance1.value(), self.sbTrafoMediumSignificance2.value(),
                                          self.sbTrafoMediumSignificance3.value()],
                         'all': [self.sbTrafoMediumAll1.value(), self.sbTrafoMediumAll2.value(), self.sbTrafoMediumAll3.value()]
                     },
                     'Station': {
                         'condition': [self.sbStationCondition1.value(), self.sbStationCondition2.value(),
                                       self.sbStationCondition3.value(), self.sbStationCondition4.value(),
                                       self.sbStationCondition5.value()],
                         'significance': [self.sbStationSignificance1.value(), self.sbStationSignificance2.value(),
                                          self.sbStationSignificance3.value(), self.sbStationSignificance4.value(),
                                          self.sbStationSignificance5.value()],
                         'all': [self.sbStationAll1.value(), self.sbStationAll2.value(), self.sbStationAll3.value()]
                     }
                     }

        self.__pwin.temp_wf['Line'] = WeightFactors(self.__pwin, self, ObjectType.Line, temp_data=temp_data)
        self.__pwin.temp_wf['TransformerLarge'] = WeightFactors(self.__pwin, self, ObjectType.TransformerLarge, temp_data=temp_data)
        self.__pwin.temp_wf['TransformerMedium'] = WeightFactors(self.__pwin, self, ObjectType.TransformerMedium, temp_data=temp_data)
        self.__pwin.temp_wf['Station'] = WeightFactors(self.__pwin, self, ObjectType.Station, temp_data=temp_data)

        self.error_message("Privremene promjene su spremljene!")
        self.change_label_color("green", self.lblError)
        self.__pwin.logInfo.info("TEMP WEIGHT FACTOR CHANGES WERE MADE")

    def yes_no_question(self, question):
        msgbox = QMessageBox(self)
        msgbox.setWindowTitle("Pitanje")
        msgbox.setText(question)
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgbox.setIcon(QMessageBox.Question)

        if msgbox.exec() == QMessageBox.Yes:
            return True
        else:
            return False
