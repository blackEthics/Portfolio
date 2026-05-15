import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='render_markdown')
def render_markdown(value):
    if not value:
        return ''
    extensions = ['fenced_code', 'tables', 'attr_list']
    return mark_safe(md.markdown(value, extensions=extensions))
