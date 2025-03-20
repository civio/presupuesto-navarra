import six

if six.PY2:
    from guidedvisit import guidedvisit
    from covid import covid
else:
    from .guidedvisit import guidedvisit
    from .covid import covid
