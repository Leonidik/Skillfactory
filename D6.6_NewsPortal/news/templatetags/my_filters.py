from django import template
#from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter()
def toxic(text):
#    text = 5    # Для тестирования
    if isinstance(text, str) is False:
        value = "метод toxic: имеем на входе "+str(type(text))+", а должен быть <class 'str'>"
        raise TypeError(value)

    voc = ['терять','титул','схода','опережает',
           'получить','визу','документы','категорий',
           'Иван','Ургант','телеведущий','актер',
           'расширила','подданных','Лондона','вооруженных', 
           'Явлинский','Яблоко','руководитель','Игорь',]
    for word in voc:
        text = text.replace( word, word[0]+'*'*(len(word)-1))
    
    return f'{text}'

