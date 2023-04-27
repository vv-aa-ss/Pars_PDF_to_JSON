from download_pdf import get_pdf
import tabula
import json
import os

temp_list_ct = []
temp_list_nct = []

group = ""
directory = 'PDF'
result = {}


def test_pdf(file):
    temp = []
    df = tabula.read_pdf(file, pages="all", encoding='Windows-1251')[0]
    for row in df.itertuples(index=False):
        temp.append([i for i in row])
    if temp[1][5] == "нечетная неделя":
        return 1
    return 0


# Перебираем PDF файлы
def get_file(folder):
    global result
    global temp_list_ct
    global temp_list_nct

    for filename in os.listdir(folder):
        file = os.path.join(folder, filename)
        if os.path.isfile(file):
            # Парсим PDF и добавляем в результат, затем чистим temp
            if test_pdf(file) == 0:
                pars_pdf(file)
                temp_list_ct = []
                temp_list_nct = []
            else:
                print(f"Ошибка распознавания файла ->> {file}")


# Добавление в list
def dict_app(data):
    global temp_list_ct
    global temp_list_nct

    try:
        temp_list_ct.append(
            dict(TimeStartEnd=data[5], Audience=data[7], LessonType=data[9], Teacher=data[11],
                 Discipline=data[13]))
        temp_list_nct.append(
            dict(TimeStartEnd=data[5], Audience=data[21], LessonType=data[19], Teacher=data[17],
                 Discipline=data[15]))
    except:
        print(' ---> Ошибка добавления в структуру!')


def test(file):
    try:
        df = tabula.read_pdf(file, pages="all", encoding='Windows-1251')[0]
        return df
    except:
        print(' ---> Ошибка добавления в структуру!')


def pars_pdf(file):
    global result
    global temp_list_ct
    global temp_list_nct
    day = ""
    result_nct = {}
    result_ct = {}
    text = []

    df = test(file)
    group_name = file[len(directory) + 1:len(file) - 4]
    print(f"PROCESS ->> {group_name}", end="")
    # Pars PDF

    # Вместо пустых данных - 0
    df = df.fillna("0")
    # Распаковываем DataFrame
    for row in df.itertuples(index=False):
        text.append([i for i in row])
    # Перебираем данные, генерируем структуру
    for data in text[1:]:
        # Если в данных нет названия недели
        if data[1] in "0":
            # Add pair
            dict_app(data)
        else:
            # Если прошли день недели
            if day == "":
                # Если первая итерация 
                day = data[1]
                dict_app(data)
            else:
                if data[1] not in "12345":
                    # Если не дошли до субботы, добавляем данные в структуру
                    result_ct[day] = temp_list_ct
                    result_nct[day] = temp_list_nct
                    temp_list_nct = []
                    temp_list_ct = []
                    day = data[1]
                    dict_app(data)
                else:
                    # Обрабатываем субботу
                    temp_list_ct.append(
                        dict(TimeStartEnd=data[3], Audience=data[5], LessonType=data[7], Teacher=data[9],
                             Discipline=data[11]))
                    temp_list_nct.append(
                        dict(TimeStartEnd=data[3], Audience=data[19], LessonType=data[17], Teacher=data[15],
                             Discipline=data[13]))
    result_ct[day] = temp_list_ct
    result_nct[day] = temp_list_nct
    result[group_name] = {"odd": result_ct, "even": result_nct}
    # Clear dict
    result_ct = {}
    result_nct = {}
    print(" >------Ok")


# Create JSON
def get_json(result):
    with open('result.json', 'w') as fp:
        json.dump(result, fp)


def main():
    # get_pdf(url="https://mtuci.ru/time-table/")
    get_file(directory)
    get_json(result)


if __name__ == "__main__":
    main()
    print("Done")
