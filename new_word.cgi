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
<title><NEW WORD</title>
</head>
<body>''')

my_dictionary = []
en_words = []

print('''<form action="" method="get">
<fieldset><legend>Новое слово</legend>
<input type="text" name="en_word" placeholder="English word:    "><br>
<input type="text" name="ru_word" placeholder="Русское слово:    "><br><br>
<input type="submit" value="Записать">
</fieldset>
</form>''')

new_word = cgi.FieldStorage()
en_word = new_word.getfirst("en_word")
ru_word = new_word.getfirst("ru_word")
significance_new_word = None

file_dictionary = sqlite3.connect("en_to_ru.db") # ex.db для опытов

def read_dictionary():
    r_dictionary = file_dictionary.cursor()
    my_dictionary = r_dictionary.execute("SELECT * FROM dictionary;").fetchall()
    r_dictionary.close()
    del r_dictionary
    return sorted(my_dictionary)

my_dictionary = read_dictionary()

for i in range(len(my_dictionary)):
    en_words.append(my_dictionary[i][0])

def write_dictionary(en_word, ru_word, significance_new_word):
    w_dictionary = file_dictionary.cursor()
    w_dictionary.execute("INSERT INTO dictionary (en, ru, significance) VALUES (?,?,?);", (en_word, ru_word, bool(significance_new_word)))
    file_dictionary.commit()
    w_dictionary.close()
    del w_dictionary

if (en_word != None and ru_word != None) and (en_word not in en_words):
     write_dictionary(en_word, ru_word, significance_new_word)

print(f'<p><a href="en_to_ru.cgi">Словарь</a></p>')

print(f'''</body>
</html>''')
