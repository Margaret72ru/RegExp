import csv
import re

if __name__ == '__main__':
    # Открытие справочника
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    pattern = r'(\+7|8|7)?\s*\(?(\d{3})\)?\s*[- ]?(\d{1,3})[- ]?(\d{2})[- ]?(\d{2})\s?\(?(доб.)?\s?(\d{4})?\)?'
    new_pattern = r'+7(\2)\3-\4-\5 \6\7'

    for i in range(1, len(contacts_list)):
        r = contacts_list[i]
        # Разделение ФИО
        fio = list((str(r[0] + " " + r[1] + " " + r[2]).strip(" ")).split(sep=" "))
        r[0] = fio[0]
        del fio[0]
        r[1] = fio[0]
        del fio[0]
        r[2] = " ".join(fio)

        # Форматирование тел. номера
        r[5] = re.sub(pattern, new_pattern, r[5]).strip(" ")

    # Объединение повторяющихся строк
    for i in range(1, len(contacts_list)):
        for j in range(i + 1, len(contacts_list)):
            if i == j:
                continue
            r1 = contacts_list[i]
            r2 = contacts_list[j]
            if r1[0] == r2[0] and r1[1] == r2[1]:
                for k in range(0, len(r1)):
                    r1[k] = r1[k] if len(r1[k]) is not None and len(r1[k]) > 0 else r2[k]
                    r2[k] = None

    phonebook = list(filter(lambda r: r[0] is not None, contacts_list))

    # Запись результата
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(phonebook)
