from django import template
import re
register = template.Library()
@register.filter
def digits(value): return re.sub(r'\D', '', value or '')
@register.filter
def whatsapp_url(value): return 'https://wa.me/' + re.sub(r'\D', '', value or '')
