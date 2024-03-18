from django import template


register = template.Library()


@register.filter()
def censor(value):
    yuck = ['-----------',
                'ваыупап',
                'нпосн',
                'папркерщж',
                ]
    length = len(yuck)
    filtered_text = ''
    string = ''
    pattern = '*'
    for i in value:
        string += i
        string2 = string.lower()

        clear = 0
        for j in yuck:
            if not string2 in j:
                clear += 1
            if string2 == j:
                filtered_text += pattern * len(string)
                clear -= 1
                string = ''

        if clear == length:
            filtered_text += string
            string = ''

    if string2 != '' and string2 not in yuck:
        filtered_text += string
    elif string2 != '':
        filtered_text += pattern * len(string)

    return filtered_text

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()