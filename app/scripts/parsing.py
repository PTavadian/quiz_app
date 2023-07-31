

class Parsing:
    text: str
    'Осноной текст'
    dict_words: dict[int|dict[str|str]]
    'Данные текста'


    def __init__(self) -> None:
        self.dict_words = dict()
        

    def convert(self, name: str, text: str) -> None:
        'Преобразует текст УП в словарь. Key - номер строки, Value - словарь'

        if not text:
           return
        
        text = text.strip()
        end_line: int = 0 # индекс последнего символа строки
        count_line: int = 1 # счетчик строк
        for i, word in enumerate(text):
            if word == '\n' or i == len(text) - 1:
                
                line = text[end_line:i+1].strip()
                end_line = i + 1

                if not self.dict_words.get(count_line):
                    self.dict_words[count_line] = {name: line, "line": count_line}
                else:
                    self.dict_words[count_line][name] = line

                count_line += 1


    def get_dict(self) -> dict[int | dict[str|str]]:
        '''Возвращает сформированный словать, заполняет пустые колонки'''

        for i in range(1, len(self.dict_words) + 1):

            if not self.dict_words[i].get('column_1'):
                self.dict_words[i]['column_1'] = ''

            if not self.dict_words[i].get('column_2'):
                self.dict_words[i]['column_2'] = ''

            if not self.dict_words[i].get('column_3'):
                self.dict_words[i]['column_3'] = ''

            if not self.dict_words[i].get('column_4'):
                self.dict_words[i]['column_4'] = ''

        return self.dict_words


    def __repr__(self):
        
        width: int = 35
        text: str = '\n+' + '-----+' + ('-' * width + '+') * 4 + '\n'
        
        for i in range(1, len(self.dict_words) + 1):
            line = str(self.dict_words[i]['line']).ljust(5, ' ')
            word_1 = self.dict_words[i]['column_1'].ljust(width, ' ')
            word_2 = self.dict_words[i]['column_2'].ljust(width, ' ')
            word_3 = self.dict_words[i]['column_3'].ljust(width, ' ')
            word_4 = self.dict_words[i]['column_4'].ljust(width, ' ')

            text += '|' + line + '|' + word_1 + '|' + word_2 + '|' + word_3 + '|' + word_4 + '|' +'\n' 
            text += '+-----+' + ('-' * width + '+') * 4 + '\n'
        return text


    def lesson_dict(self, words) -> dict[int | dict[str|None]]:
        '''Преобразует в словать с ключем = № урока'''

        self.dict_words
        for word in words:
            if not self.dict_words.get(word.lesson):
                self.dict_words[word.lesson] = {word.word_id: {'column_1': word.first_lng,
                                                               'column_2': word.second_lng,
                                                               'column_3': word.third_lng,
                                                               'column_4': word.fourth_lng,}}

            else:
                self.dict_words[word.lesson][word.word_id] = {'column_1': word.first_lng,
                                                              'column_2': word.second_lng,
                                                              'column_3': word.third_lng,
                                                              'column_4': word.fourth_lng,}

        return self.dict_words



def change_column(last_column: str, dict_words: dict, id_lesson: int, id_word: int) -> str:
    '''Возвращяет название актуального столбца'''
    
    if last_column == 'column_1' and dict_words[id_lesson][id_word]['column_2']:
        column = 'column_2'

    elif last_column == 'column_1' and dict_words[id_lesson][id_word]['column_3']:
        column = 'column_3'

    elif last_column == 'column_1' and dict_words[id_lesson][id_word]['column_4']:
        column = 'column_4'
        
    elif last_column == 'column_2' and dict_words[id_lesson][id_word]['column_3']:
        column = 'column_3'

    elif last_column == 'column_2' and dict_words[id_lesson][id_word]['column_4']:
        column = 'column_4'

    elif last_column == 'column_2' and dict_words[id_lesson][id_word]['column_1']:
        column = 'column_1'
        
    elif last_column == 'column_3' and dict_words[id_lesson][id_word]['column_4']:
        column = 'column_4'

    elif last_column == 'column_3' and dict_words[id_lesson][id_word]['column_1']:
        column = 'column_1'

    elif last_column == 'column_3' and dict_words[id_lesson][id_word]['column_2']:
        column = 'column_2'
        
    elif last_column == 'column_4' and dict_words[id_lesson][id_word]['column_1']:
        column = 'column_1'

    elif last_column == 'column_4' and dict_words[id_lesson][id_word]['column_2']:
        column = 'column_2'

    elif last_column == 'column_4' and dict_words[id_lesson][id_word]['column_3']:
        column = 'column_3'

    else:
        column = 'column_1'

    return column



def next_column(dict_words: dict, id_lesson: int, id_word: int) -> str:
    '''Возвращяет название актуального столбца''' 

    if dict_words[id_lesson][id_word]['column_1']:
        column = 'column_1'

    elif dict_words[id_lesson][id_word]['column_2']:
        column = 'column_2'

    elif dict_words[id_lesson][id_word]['column_3']:
        column = 'column_3'
        
    elif dict_words[id_lesson][id_word]['column_4']:
        column = 'column_4'

    else:
        column = 'column_1'

    return column



def replace(word: str | None) -> str:
    if not word or word == 'None':
        word = ''
    return word









def test_2():

    d = {'1': 'one', '2': 'two', '3': 'three', '5': 'five'}

    for i in range(1, len(d) + 1):
        if d.get(str(i)):
            pass



if __name__ == '__main__':
    
    text_1 = '''булочка
    масло сливочное
    сыр
    бутерброд с сыром
    варенье
    ветчина
    яйца
    голодный
    есть
    нравится
    просыпаться
    часов
    вставать
    принамать душ
    от
    '''

    text_2 = '''et rundtykke
    smør
    ost
    ei skive dem ost
    syltetøy
    skinke
    et egg
    sulten
    spise
    liker
    våkne
    klokka
    står opp
    en dusj
    fra

    '''

    tt = Parsing()

    tt.convert(name='column_1', text=text_1)
    tt.convert(name='column_2', text=text_2)

    t = tt.get_dict()

    print(t, '\n')
    print(tt)

    test_2()