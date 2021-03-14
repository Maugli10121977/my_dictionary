#!/usr/bin/env python3

import cgi
import sqlite3
import os

my_dictionary = []
c = 'checked'

file_dictionary = sqlite3.connect("en_to_ru.db") # ex.db для опытов

def read_dictionary():
    r_dictionary = file_dictionary.cursor()
    my_dictionary = r_dictionary.execute("SELECT * FROM dictionary;").fetchall()
    r_dictionary.close()
    del r_dictionary
    return sorted(my_dictionary)

my_dictionary = read_dictionary()

en_words = []
for i in range(len(my_dictionary)):
    en_words.append(my_dictionary[i][0])

def read_current_address():
    r_c_a = open('.current_address.txt','r')
    current_address = r_c_a.read()
    r_c_a.close()
    del r_c_a
    return current_address

current_address = read_current_address()

print('Content-type: text/html')
print('')
print(f'''<!DOCTYPE html>
<html>
<head>
<meta name="robots" content="noindex">
<meta charset="utf-8">
<meta http-equiv="refresh" url="{current_address}">
<title>EN_TO_RU</title>
</head>
<body>''')

print('<p><a href="new_word.cgi">Новое слово</a></p>')

print(f'''<form action="" method="get">
<fieldset><legend>Словарь</legend>''')

for i in range(len(my_dictionary)):
    if bool(my_dictionary[i][2]) == bool('on'):
        print(f'<p><input type="checkbox" {c} name="id{i}"><strong>{my_dictionary[i][0]}</strong> <em>{my_dictionary[i][1]}</em></p>')
    else:
        print(f'<p><input type="checkbox" name="id{i}"><strong>{my_dictionary[i][0]}</strong> <em>{my_dictionary[i][1]}</em></p>')

print(f'<input type="submit" value="Изменить важность"><br>')
print(f'''</fieldset>
</form>''')

c_sign = cgi.FieldStorage()

def update_significance():
    u_dictionary = file_dictionary.cursor()
    for i in range(len(my_dictionary)):
        word_significance = c_sign.getfirst(f"id{i}")
        if bool(my_dictionary[i][2]) != bool(word_significance):
            u_dictionary.execute("UPDATE dictionary SET significance=? WHERE en=?;", (bool(word_significance), my_dictionary[i][0]))
            file_dictionary.commit()
    u_dictionary.close()
    del u_dictionary

print('<p>_________________________________________________</p>')
print(f'<p>В словаре имеется {len(my_dictionary)} слов.</p>')
print('<p></p>')

def write_current_address():
    w_c_a = open('.current_address.txt','w')
    w_c_a.write(f'http://{os.environ["HTTP_HOST"]}{os.environ["SCRIPT_NAME"]}?{os.environ["QUERY_STRING"]}')
    w_c_a.close()
    del w_c_a

if bool(os.environ["QUERY_STRING"]) == True: # Приделать сюда регулярку на соответствие 'id*' в os.environ["QUERY_STRING"], и вернуть форму с новым словом
    update_significance()
    write_current_address()

print(f'''</body>
</html>''')

