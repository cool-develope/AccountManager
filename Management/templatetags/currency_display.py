from django import template

register = template.Library()

@register.filter("currency")
def display_as_currency(value):
    value = str(int(float(value)))
    res = []
    for i in range(len(value)):
      res.append(value[len(value) - i - 1])
      if i % 3 == 2 and i < len(value) - 1 and value[len(value) - i - 2] != '-':
        res.append(',')
    return ''.join(reversed(res))