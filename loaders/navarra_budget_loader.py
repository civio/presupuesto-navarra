# -*- coding: UTF-8 -*-

from budget_app.models import *
from budget_app.loaders.budget_loader import BudgetLoader
import csv
import os.path
import re


class NavarraBudgetLoader(BudgetLoader):

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

    # TODO: Temporary, while we sort out why so many codes are missing
    def get_default_institutional_categories(self):
        categories = BudgetLoader.get_default_funding_categories(self)
        categories.append({
                        'institution': 'XX',
                        'section': 'XXX',
                        'department': 'XXXXX',
                        'description': 'Gobierno de Navarra'
                    })
        return categories

    def add_institutional_category(self, items, line):
        description = line[2] if line[3] == "" else line[3]
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
        # The columns are not consistent across the years
        description = line[6] if line[0] in ['2010', '2011'] else line[5]
        items.append({
                'area': (line[1] if len(line[1])>=1 else None),
                'policy': (line[1]+line[2] if len(line[2])>=1 else None),
                'function': (line[1]+line[2]+line[3] if len(line[3])>=1 else None),
                'programme': (line[1]+line[2]+line[3]+line[4] if len(line[4])>=1 else None),
                'description': description
            })


    def add_economic_category(self, items, line):
        description = line[6]

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
        # The columns are not consistent across the years
        ic_code = line[1] if not is_actual and (line[0] in ['2010', '2011', '2012'] or (line[0]=='2013' and not is_expense)) else line[2]

        # Something weird happened with the 2013 revenue data files
        amount = self._read_spanish_number(line[6])
        if line[0]=='2013' and not is_expense:
            amount = -amount

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
                'item_number': fc_code[-2:],    # Last two digits
                # We leave it blank, so the base loader will fill it in using the economica category
                'description': line[5],
                'amount': amount
            })

    def _get_delimiter(self):
        return ','

    # An artifact of the in2csv conversion of the original XLS files is a trailing '.0', which we remove here
    def _clean(self, s):
        return s.split('.')[0]
