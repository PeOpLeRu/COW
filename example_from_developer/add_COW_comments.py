name_file = input("Enter name of file: ")

key_words = {
                "MoO" : "значение текущей ячейки увеличить на 1",
                "MOo" : "значение текущей ячейки уменьшить на 1",
                "moO" : "следующая ячейка",
                "mOo" : "предыдущая ячейка",
                "moo" : "начало цикла",
                "MOO" : "конец цикла",
                "OOM" : "вывод значения текущей ячейки",
                "oom" : "ввод значения в текущую ячейку",
                "mOO" : "выполнить инструкцию с номером из текущей ячейки",
                "Moo" : "если значение в ячейке равно 0, то ввести с клавиатуры, если значение не 0, то вывести на экран",
                "OOO" : "обнулить значение в ячейке",
            }

f = open(name_file, encoding='utf8')
f_out = open("res.cow", 'w')

for str in f:
    clear_str = str.replace("\t", "")
    key = clear_str[0 : 3]
    
    if (len(str) >= 3 and key in key_words):
        f_out.write(str.replace('\n', '') + f"\t// {key_words[key]}\n")
    else:
        f_out.write(str.replace('\n', '') + '\n')