from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter(name='addclass')
def addclass(field, css_classes):
    """Add CSS classes to form field."""
    if field.field.widget.attrs.get('class'):
        css_classes = f"{field.field.widget.attrs['class']} {css_classes}"
    return field.as_widget(attrs={"class": css_classes})

@register.filter(name='get_type')
def get_type(value):
    """Return the type of the value."""
    return type(value).__name__
