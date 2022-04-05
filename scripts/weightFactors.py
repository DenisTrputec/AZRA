from scripts.envVars import ADMIN_PASSWORD, WEIGHT_FACTORS_FILEPATH
from scripts.crypto import CryptoFile
from scripts.validation import Validate


default_data = [['Line', 'condition', 10, 5, 5, 10, 10],
                ['Line', 'significance', 10, 10, 5, 10, 5],
                ['Line', 'all', 8, 12, 100],
                ['TransformerLarge', 'condition', 10, 5, 5],
                ['TransformerLarge', 'significance', 10, 5, 5],
                ['TransformerLarge', 'all', 8, 12, 100],
                ['TransformerMedium', 'condition', 10, 5, 5],
                ['TransformerMedium', 'significance', 5, 5, 10],
                ['TransformerMedium', 'all', 8, 12, 100],
                ['Station', 'condition', 7.5, 10, 5, 5, 10],
                ['Station', 'significance', 10, 8.75, 5, 5, 8.75],
                ['Station', 'all', 8, 12, 100]]


class WeightFactors:
    def __init__(self, main_window, current_window, object_type, temp_data=None):
        main_window.logDebug.info("Call:WeightFactors.__init__()")
        self.__pwin = main_window
        self.__cwin = current_window
        self.__weight_factors_filepath = WEIGHT_FACTORS_FILEPATH
        self.__object_type = object_type
        self.data = {}
        if temp_data is None:
            try:
                weight_factors_decrypted = CryptoFile.decrypt(self.__pwin, self.__weight_factors_filepath, ADMIN_PASSWORD)
            except Exception as e:
                self.__pwin.logDebug.exception(e)
                raise Exception("Weight Factors reading error!")
            for row in weight_factors_decrypted.decode().split('\n'):
                if row != "":
                    values = row.split(',')
                    if values[0] in self.__object_type.name:
                        self.data[values[1]] = values[2:]
        else:
            for key, value in temp_data.items():
                if key == self.__object_type.name:
                    for key2, value2 in value.items():
                        self.data[key2] = value2

        Validate.weight_factors(self.__pwin, self.__cwin, self.data)
        self.__pwin.logDebug.info("Return:WeightFactors.__init__()")

    def __str__(self):
        return f"Weight Factors\nCondition:{self.data['condition']}\nSignificance:{self.data['significance']}\nAll:{self.data['all']}"


if __name__ == "__main__":
    # Encryption of weight factors
    original_file = "C:/Programi/Python3/KiM/decrypted_fake.csv"
    weight_factors_filepath = "/resources/weight_factors/weight_factors_encrypted"
    password = "ndc-dt.268".encode()
    CryptoFile.encrypt(None, original_file, weight_factors_filepath, password)
