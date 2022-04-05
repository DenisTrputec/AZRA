import os


class Validate:
    @staticmethod
    def input(window, filepath):
        if not os.path.exists(filepath):
            window.error_message("Ne postoji odabrana ulazna datoteka!")
            raise Exception("Selected input file doesn't exist!")
        elif not filepath.endswith(".xlsx"):
            window.error_message("Ulazna datoteka nije točnog formata! (Mora biti *.xlsx)")
            raise Exception("Input file format error")

    @staticmethod
    def output(window, filepath):
        if not os.path.isdir(os.path.dirname(os.path.abspath(filepath))):
            window.error_message("Ne postoji odabrani izlazni direktorij!")
            raise Exception("Selected output directory doesn't exist!")
        elif not filepath.endswith(".xlsx"):
            window.error_message("Izlazna datoteka nije točnog formata! (Mora biti *.xlsx)")
            raise Exception("Output file format error")

    @staticmethod
    def control_center(window, sheet, row, col):
        if sheet[row][col].value not in ['NDC', 'ZG', 'RI', 'ST', 'OS']:
            window.error_message(f"Neispravna vrijednost '{sheet[row][col].value}' u stupcu '{sheet[1][col].value}'")
            raise Exception(f"Faulty value '{sheet[row][col].value}' in column '{sheet[1][col].value}'")

    @staticmethod
    def if_zero_and_one(window, sheet, row, col):
        if not isinstance(sheet[row][col].value, int) or (sheet[row][col].value != 0 and sheet[row][col].value != 1):
            window.error_message(f"Neispravna vrijednost '{sheet[row][col].value}' u stupcu '{sheet[1][col].value}'")
            raise Exception(f"Faulty value '{sheet[row][col].value}' in column '{sheet[1][col].value}'")

    @staticmethod
    def if_zero_and_half_and_one(window, sheet, row, col):
        if not (isinstance(sheet[row][col].value, int) or isinstance(sheet[row][col].value, float)) or \
                sheet[row][col].value > 1.0 or sheet[row][col].value < 0.0:
            window.error_message(f"Neispravna vrijednost '{sheet[row][col].value}' u stupcu '{sheet[1][col].value}'")
            raise Exception(f"Faulty value '{sheet[row][col].value}' in column '{sheet[1][col].value}'")

    @staticmethod
    def if_between_zero_and_one(window, sheet, row, col):
        if not (isinstance(sheet[row][col].value, int) or isinstance(sheet[row][col].value, float)) or \
                sheet[row][col].value > 1.0 or sheet[row][col].value < 0.0:
            window.error_message(f"Neispravna vrijednost '{sheet[row][col].value}' u stupcu '{sheet[1][col].value}'")
            raise Exception(f"Faulty value '{sheet[row][col].value}' in column '{sheet[1][col].value}'")

    @staticmethod
    def year(window, sheet, row, col, year):
        if not isinstance(sheet[row][col].value, int) or sheet[row][col].value > year:
            window.error_message(f"Neispravna vrijednost '{sheet[row][col].value}' u stupcu '{sheet[1][col].value}'")
            raise Exception(f"Faulty value '{sheet[row][col].value}' in column '{sheet[1][col].value}'")

    @staticmethod
    def if_number(window, sheet, row, col):
        if not (isinstance(sheet[row][col].value, int) or isinstance(sheet[row][col].value, float)):
            window.error_message(f"Neispravna vrijednost '{sheet[row][col].value}' u stupcu '{sheet[1][col].value}'")
            raise Exception(f"Faulty value '{sheet[row][col].value}' in column '{sheet[1][col].value}'")

    @staticmethod
    def if_number_positive(window, sheet, row, col):
        if not (isinstance(sheet[row][col].value, int) or isinstance(sheet[row][col].value, float)) or \
                sheet[row][col].value < 0.0:
            window.error_message(f"Neispravna vrijednost '{sheet[row][col].value}' u stupcu '{sheet[1][col].value}'")
            raise Exception(f"Faulty value '{sheet[row][col].value}' in column '{sheet[1][col].value}'")

    @staticmethod
    def same_object_info(window, ws_con, ws_sig, ws_eco, row):
        for col in range(0, 5):
            if ws_con[row][col].value != ws_sig[row][col].value:
                window.error_message(f"Neispravni ćelija '{chr(col + 65)}{row}' u radnom listu 'ZNAČAJ'")
                raise Exception(f"Faulty cell '{chr(col + 65)}{row}' in worksheet 'ZNAČAJ'")
            elif ws_eco is not None and ws_con[row][col].value != ws_eco[row][col].value:
                window.error_message(f"Neispravni ćelija '{chr(col + 65)}{row}' u radnom listu 'EKONOMIJA'")
                raise Exception(f"Faulty cell '{chr(col + 65)}{row}' in worksheet 'EKONOMIJA'")

    @staticmethod
    def weight_factors(main_window, current_window, weight_factors):
        keys = ['condition', 'significance', 'all']
        sums = {'condition': 0, 'significance': 0, 'all': 0}

        for key in keys:
            try:
                weight_factors[key]
            except KeyError:
                current_window.error_message(f"Ne postoji težinski faktor '{key}'")
                raise Exception(f"Weight factor '{key}' doesn't exist")

            for value in weight_factors[key]:
                try:
                    value = float(value)
                    sums[key] += value
                except ValueError:
                    current_window.error_message(f"Težinski faktor '{key}' nije broj veći ili jednak 0: '{value}'")
                    raise Exception(f"Weight factor '{key}' is not higher than 0: '{value}'")

        if main_window == current_window and sums['condition'] != sums['significance']:
            current_window.error_message("Suma težinskih faktora stanja i značaja nije jednaka")
            raise Exception("Sum of condition and significance weight factors isn't equal")
