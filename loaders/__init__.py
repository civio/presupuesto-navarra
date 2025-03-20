import six

if six.PY2:
    from navarra_budget_loader import NavarraBudgetLoader
else:
    from .navarra_budget_loader import NavarraBudgetLoader
