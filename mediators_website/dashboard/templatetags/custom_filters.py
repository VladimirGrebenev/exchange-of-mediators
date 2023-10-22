from django import template

register = template.Library()


@register.filter
def feedback_error(value):
    value.error_class += ' invalid-feedback'
    return value


@register.filter
def input_error(value):
    classes = value.field.widget.attrs.get('class')
    classes += ' is-invalid'
    value.field.widget.attrs['class'] = classes
    return value
