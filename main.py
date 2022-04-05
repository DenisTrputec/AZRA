import os
import sys
import logging
from datetime import date, datetime
from scripts.envVars import formMainWindow, baseMainWindow
from scripts.envVars import INPUT_FOLDER, OUTPUT_FOLDER, OUTPUT_FILE, INFO_FILE, HELP_FILE, LOG_FOLDER
from scripts.importData import ImportData
from scripts.export.excel import ExportDataExcel
from scripts.enumValues import ObjectType
from scripts.validation import Validate
from scripts.weightFactors import WeightFactors
from scripts.gui.weightFactorsGui import WeightFactorsWindow
from scripts.gui.weightFactorsGui2 import WeightFactorsWindow2
from scripts.gui.login import Login
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox


def setup_logger(name: str, file_path: str, format_string: str, level=logging.INFO):
    """
    :return: Logger object
    """
    handler = logging.FileHandler(file_path)
    handler.setFormatter(logging.Formatter(format_string))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    os.chmod(file_path, 0o777)
    return logger


class MainWindow(baseMainWindow, formMainWindow):
    def __init__(self):
        super(baseMainWindow, self).__init__()
        self.setupUi(self)
        self.child_window = None

        self.logInfo = setup_logger(name="InfoLogger",
                                    file_path=os.path.join(LOG_FOLDER, date.today().strftime("%Y%m%d.log")),
                                    format_string=f"{os.getlogin()}:%(message)s")
        self.logDebug = setup_logger(name="DebugLogger",
                                     file_path=os.path.join(LOG_FOLDER, date.today().strftime("debug_%Y%m%d.log")),
                                     format_string=f"%(levelname)s:%(module)s:%(message)s",
                                     level=logging.DEBUG)
        self.logDebug.info("Call:MainWindow.__init__()")

        self.lineOutput.setText(os.path.normpath(os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)))
        self.sbYear.setValue(date.today().year)
        self.lblError.setText("")

        self.actWeightFactorsGui.triggered.connect(self.show_weight_factors_gui)
        self.actHelp.triggered.connect(lambda: self.show_textfile_as_messagebox(HELP_FILE, "Pomoć"))
        self.actInfo.triggered.connect(lambda: self.show_textfile_as_messagebox(INFO_FILE, "Informacije"))

        self.btnInput.clicked.connect(self.get_input_file)
        self.btnOutput.clicked.connect(self.get_output_directory)
        self.btnCalculate.clicked.connect(self.calculate)

        self.is_admin = False
        self.is_iterative = True
        self.rank_list = []
        self.temp_wf = None
        self.logDebug.info("Return:MainWindow.__init__()")

    def login(self):
        self.child_window = Login(self)
        self.child_window.show()

    def show_textfile_as_messagebox(self, txt_file, title):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        with open(txt_file, 'r', encoding='UTF-8') as handle:
            msg.setText(handle.read())
            msg.show()

    def show_weight_factors_gui(self):
        if self.is_admin:
            self.child_window = WeightFactorsWindow(self)
        else:
            self.child_window = WeightFactorsWindow2(self)
        self.child_window.show()

    def get_input_file(self):
        file_path = QFileDialog.getOpenFileName(self, caption='Browse input file', directory=INPUT_FOLDER, filter='*.xlsx')[0]
        self.lineInput.setText(os.path.normpath(file_path))

    def get_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, caption='Browse output directory', directory=OUTPUT_FOLDER)
        self.lineOutput.setText(os.path.normpath(os.path.join(dir_path, OUTPUT_FILE)))

    def calculate(self):
        self.logInfo.info("Started calculation")
        self.logInfo.info(f"Object type is {self.return_checked_radio_button().name}")
        try:
            # Validate filepaths
            Validate.input(self, self.lineInput.text())
            Validate.output(self, self.lineOutput.text())

            # Initialize attributes
            self.lblError.setText("")
            self.rank_list = []

            # Read data
            object_type = self.return_checked_radio_button()
            data = ImportData(self, self.lineInput.text(), object_type, self.sbYear.value())
            try:
                weight_factors = WeightFactors(self, self, object_type) if self.temp_wf is None else self.temp_wf[object_type.name]
            except Exception:
                self.error_message("Problem kod učitavanja težinskih faktora!")
                return
            self.logInfo.info(weight_factors)

            # Create Rank list
            if self.is_iterative:
                for i in range(1, len(data.investmentObjects)):
                    data.calculate_indexes(weight_factors)
                    rank_list_current = data.return_list_sort_by_index_desc()
                    rank_list_current[0].rank = i
                    rank_list_current[0].is_in_calculation = False
                    self.rank_list.append(rank_list_current[0])
                    if i + 1 == len(data.investmentObjects):
                        rank_list_current[-1].rank = i
                        rank_list_current[-1].is_in_calculation = False
                        self.rank_list.append(rank_list_current[-1])
            else:
                data.calculate_indexes(weight_factors)
                rank_list_current = data.return_list_sort_by_index_desc()
                for i, obj in enumerate(rank_list_current):
                    obj.rank = i + 1
                    obj.is_in_calculation = False
                    self.rank_list.append(obj)

            print("---Rank List----------------------------------")
            for obj in self.rank_list:
                print(obj.rank, obj.row_number, obj.name, obj.index)
        except Exception as e:
            # self.error_message(e.args[0])
            self.logDebug.exception(e)
            self.logInfo.info("Calculation Failed")
            return

        try:
            ExportDataExcel.create_output_excel(self.rank_list, self.lineOutput.text())
        except Exception as e:
            self.error_message(e.args[0])
            self.logDebug.exception(e)
            self.logInfo.info("Creating output file Failed")
        self.lblError.setStyleSheet("color: black")
        self.lblError.setText("Kalkulacija uspješno izvršena i kreirana je izlazna datoteka!")
        self.logDebug.info("Return:MainWindow.calculate()")
        self.logInfo.info("Calculation was finished successfully!")

    def error_message(self, text: str):
        self.lblError.setStyleSheet("color: red")
        self.lblError.setText(text)

    def return_checked_radio_button(self):
        if self.rbLine.isChecked():
            return ObjectType.Line
        if self.rbTrafoLarge.isChecked():
            return ObjectType.TransformerLarge
        if self.rbTrafoMedium.isChecked():
            return ObjectType.TransformerMedium
        if self.rbStation.isChecked():
            return ObjectType.Station


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.logInfo.info(f'Application started at {datetime.now().strftime("%H:%M:%S")}')
    main_window.login()
    sys.exit(app.exec_())
