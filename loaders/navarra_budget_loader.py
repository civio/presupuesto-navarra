# -*- coding: UTF-8 -*-

from budget_app.loaders import SimpleBudgetLoader


class NavarraBudgetLoader(SimpleBudgetLoader):

    def __init__(self):
        super().__init__()
        self.descriptions = []

    # Navarra's economic codes go down to subheadings (four digits)
    def _split_economic_code(self, ec_code):
        chapter, article, heading, _ = super()._split_economic_code(ec_code)
        return chapter, article, heading, (ec_code if len(ec_code) >= 4 else None)

    # The classifications change every year, so there's one in each year's folder,
    # in Navarra's own format, with the year in the first column
    def parse_institutional_category(self, line):
        _, code, description = line

        # Navarra has too many levels of institutional hierarchy. We're just going
        # to pick the two-, three- and five-digit ones
        if len(code) in (1, 4):
            return None

        return {
            'institution': code[0:2],
            'section': code[0:3] if len(code) > 2 else None,
            'department': code if len(code) > 4 else None,
            'description': description
        }

    def parse_functional_category(self, line):
        _, area, policy, group, programme, description = line
        area, policy, group, programme = self._join_codes(area, policy, self._clean(group), self._clean(programme))
        return {
            'area': area,
            'policy': policy,
            'function': group,
            'programme': programme,
            'description': description
        }

    def parse_economic_category(self, line):
        _, income_or_expense, chapter, article, heading, subheading, description = line
        chapter, article, heading, subheading = self._join_codes(chapter, article, heading, subheading)
        return {
            'expense': income_or_expense.upper() == 'GASTO',
            'chapter': chapter,
            'article': article,
            'heading': heading,
            'subheading': subheading,
            'description': description.strip()
        }

    def parse_item(self, filename, line):
        is_expense = (filename.find('gastos.csv') != -1)
        is_actual = (filename.find('/ejecucion_') != -1)

        # Only expenses are classified functionally, and we use programmes, the first four digits
        fc_code = line[4][0:4] if is_expense else None

        ec_code = line[3]
        ic_code = line[2]
        raw_amount = line[8 if is_actual else 6]
        amount = self._read_english_number(raw_amount) if line[0]=='2011' else self._read_spanish_number(raw_amount)

        # The final 2016 execution data for revenues is in negative, for unknown reasons
        if not is_expense and line[0]=='2016':
            amount = -amount

        # We need subheading+item_number to be consistent across departments,
        # since we're grouping all different items together using economic_uid().
        # That's not the case in Navarra, so we make sure each description
        # gets a unique item number.
        description = line[5]
        if description in self.descriptions:
            item_number = self.descriptions.index(description)
        else:
            item_number = len(self.descriptions)
            self.descriptions.append(description)

        return {
            'is_expense': is_expense,
            'is_actual': is_actual,
            'ic_code': ic_code,
            'ic_institution': ic_code[0:2],
            'ic_section': ic_code[0:3],
            'ic_department': ic_code,
            'fc_code': fc_code,
            'ec_code': ec_code,
            'item_number': item_number,
            'description': description,
            'amount': amount
        }

    def _get_delimiter(self):
        return ','

    # An artifact of the in2csv conversion of the original XLS files is a trailing '.0', which we remove here
    def _clean(self, s):
        return s.split('.')[0]
