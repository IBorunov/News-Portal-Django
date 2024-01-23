from django import template


register = template.Library()


@register.filter()
def censor(value):
    yuck = ['-----------',
                'ваыупап',
                'нпосн',
                'папркерщж',
                ]  # гадости
    length = len(yuck)  # записываем кол-во гадостей
    filtered_text = ''  # отфильтрованный текст
    string = ''  # переменная, где будем хранить проверяемую строку
    pattern = '*'  # чем заменять гадости
    for i in value:  # проходимся циклом по тексту
        string += i  # записываем полученные строки в переменную
        string2 = string.lower()  # приводим строки к нижн. регистру

        clear = 0  # "чистые строки"
        for j in yuck:  # ищем гадости в тексте
            if not string2 in j:  # если не нашли гадость:
                clear += 1  # запоминаем и ищем следующее плохое слово
            if string2 == j:  # а если нашли:
                filtered_text += pattern * len(string)  # заменяем его на звездочки и записываем в отфильтрованные
                clear -= 1
                string = ''  # обнуляем строку

        if clear == length:  # после того как просмотрели все варианты гадостей:
            filtered_text += string  # добавляем строку в отфильтрованный текст
            string = ''  # обнуляем значение переменной со строкой и проверяем дальше

    if string2 != '' and string2 not in yuck:
        filtered_text += string #если гадости не встретились, записываем эту строку
    elif string2 != '':
        filtered_text += pattern * len(string) #иначе заменяем плохие слова на звездочки

    return filtered_text