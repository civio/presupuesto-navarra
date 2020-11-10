# -*- coding: UTF-8 -*-

from budget_app.models import *
from budget_app.loaders.budget_loader import BudgetLoader
import csv
import os.path
import re


class NavarraBudgetLoader(BudgetLoader):

    def __init__(self):
        self.descriptions = []

    # We don't have funding categories, so create a dummy one and assign everything to it
    def get_default_funding_categories(self):
        categories = BudgetLoader.get_default_funding_categories(self)
        categories.append({ 
                        'expense': True,
                        'source': 'X',
                        'fund_class': 'XX',
                        'fund': 'XXX',
                        'description': 'Gastos'
                    })
        categories.append({ 
                        'expense': False,
                        'source': 'X',
                        'fund_class': 'XX',
                        'fund': 'XXX',
                        'description': 'Ingresos'
                    })
        return categories

    def add_institutional_category(self, items, line):
        description = line[2]
        description = self._escape_unicode(description)

        # Navarra has too many levels of institutional hierarchy. We're just going
        # to pick the two-, three- and five-digit ones
        if len(line[1])==1 or len(line[1])==4:
            return

        items.append({
                'institution': line[1][0:2],
                'section': (line[1][0:3] if len(line[1]) > 2 else None),
                'department': (line[1] if len(line[1]) > 4 else None),
                'description': description
            })

    def add_functional_category(self, items, line):
        line[3] = self._clean(line[3])
        line[4] = self._clean(line[4])
        description = line[5]
        items.append({
                'area': (line[1] if len(line[1])>=1 else None),
                'policy': (line[1]+line[2] if len(line[2])>=1 else None),
                'function': (line[1]+line[2]+line[3] if len(line[3])>=1 else None),
                'programme': (line[1]+line[2]+line[3]+line[4] if len(line[4])>=1 else None),
                'description': description
            })


    def add_economic_category(self, items, line):
        description = line[6].strip()

        items.append({
                'expense': (line[1].upper() == 'GASTO'),
                'chapter': (line[2] if len(line[2])>=1 else None),
                'article': (line[2]+line[3] if len(line[3])>=1 else None),
                'heading': (line[2]+line[3]+line[4] if len(line[4])>=1 else None),
                'subheading': (line[2]+line[3]+line[4]+line[5] if len(line[5])>=1 else None),
                'description': description
            })

    #
    def add_data_item(self, items, line, is_expense, is_actual):
        # Parse functional code
        fc_code = line[4]
        if is_expense:
            fc_area = fc_code[0:1]
            fc_policy = fc_code[0:2]
            fc_function = fc_code[0:3]
            fc_programme = fc_code[0:4]
        else:
            fc_area = 'X'
            fc_policy = 'XX'
            fc_function = 'XXX'
            fc_programme = 'XXXX'

        # Gather all the relevant bits and store them to be processed
        ec_code = line[3]
        ic_code = line[2]
        raw_amount = line[8 if is_actual else 6]
        # Temporary patch. See civio/presupuesto-management#1046
        amount = self._read_english_number(raw_amount)
        # amount = self._read_english_number(raw_amount) if line[0]=='2011' else self._read_spanish_number(raw_amount)

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

        # Load the data item
        items.append({
                'ic_institution': ic_code[0:2],
                'ic_section': ic_code[0:3],
                'ic_department': ic_code,
                'ic_code': ic_code,
                'fc_area': fc_area,
                'fc_policy': fc_policy,
                'fc_function': fc_function,
                'fc_programme': fc_programme,
                'ec_chapter': ec_code[0],
                'ec_article': (ec_code[0:2] if len(ec_code)>=2 else None),
                'ec_heading': (ec_code[0:3] if len(ec_code)>=3 else None),
                'ec_subheading': (ec_code if len(ec_code)>=4 else None),
                'ec_code': ec_code, # Redundant, but convenient
                'fdc_code': 'XXX',  # Not used
                'item_number': item_number,
                'description': line[5],
                'amount': amount
            })

    def _get_delimiter(self):
        return ','

    # An artifact of the in2csv conversion of the original XLS files is a trailing '.0', which we remove here
    def _clean(self, s):
        return s.split('.')[0]
