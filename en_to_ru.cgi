#!/usr/bin/env python3

import cgi
import sqlite3

print('Content-type: text/html')
print('')
print('''<!DOCTYPE html>
<html>
<head>
<meta name="robots" content="noindex">
<meta charset="utf-8">
<title>EN_TO_RU</title>
</head>
<body>''')

print('''<form>
<fieldset>
<legend>Новое слово</legend>
<input type="text" name="en_word" placeholder="English word:    "><br>
<input type="text" name="ru_word" placeholder="Русское слово:    "><br>
<input type="submit" value="Записать">
</fieldset>
</form>''')

words = cgi.FieldStorage()
en_word = words.getfirst("en_word")
ru_word = words.getfirst("ru_word")

file_dictionary = sqlite3.connect("en_to_ru.db")

def write_dictionary(en_word, ru_word):
    if en_word != None and ru_word != None:
        w_dictionary = file_dictionary.cursor()
        w_dictionary.execute("INSERT INTO dictionary (en, ru) VALUES (?, ?);", (en_word, ru_word))
        file_dictionary.commit()
        w_dictionary.close()
        del w_dictionary

def read_dictionary():
    r_dictionary = file_dictionary.cursor()
    my_dictionary = r_dictionary.execute("SELECT * FROM dictionary;").fetchall()
    return sorted(my_dictionary)

en_words = []
for i in range(len(read_dictionary())):
    en_words.append(read_dictionary()[i][0])

if en_word not in en_words:
    write_dictionary(en_word, ru_word)

print('<form>')
for i in range(len(read_dictionary())):
    print(f'<p><input type="checkbox" name="id{i}"><strong>{read_dictionary()[i][0]}</strong> <em>{read_dictionary()[i][1]}</em></p>')
print('</form')

significance = cgi.FieldStorage()
def replace_significance():
    pass

print('<p>_________________________________________________</p>')
print(f'<p>В словаре имеется {len(read_dictionary())} слов.</p>')

print('''</body></html>''')
