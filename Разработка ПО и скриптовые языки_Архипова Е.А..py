#Подключаем библиотеки
from bs4 import BeautifulSoup
import requests
import time
#Задаем параметры для того, чтобы программа работала нужное нам время
i = 1
f = True
#Открываем файл с логом по найденым новостям на запись
file = open("parsing_log.txt", "w")
#Задаем список, в котором будем хранить уникальные уже найденые заголовки новостей
uniq1=[]
#Цикл, чтобы замедлить программу
while f:
    #Делаем запрос к сайту
    response = requests.get('https://rb.ru/news/')
    st = response.raise_for_status()
    #Извлекаем данные с веб-страницы
    soup = BeautifulSoup(response.text, 'lxml')
    #Собираем информаци. о дате новости, ее заголовке и содержании
    dt = soup.find_all('time', class_='news-item__date')
    dt_text = [tag.get_text().strip() for tag in dt]
    titl = soup.find_all('h2')
    titl_text = [tag.get_text().strip() for tag in titl]
    detail = soup.find_all('div', class_='news-item__details')
    detail_text = [tag.get_text().strip() for tag in detail]
    j = 0
    #В цикле проходимся по заголовкам и ищем в них ключевые слова, а также сравниваем их со списком уже найденных
    for tag in titl_text:
        if ('России' in tag or 'Евросоюз' in tag) and tag not in uniq1:
            #Найденный заголовок помещаем в список уникальных заголовков
            #а также выводим по найденному заголовку информацию о дате и содержании и записываем в лог файл.
            uniq1.append(titl_text[j])
            print(dt_text[j]+'\n')
            print(titl_text[j] + '\n')
            print(detail_text[j] + '\n')
            file.write(dt_text[j] + '\n')
            file.write(titl_text[j] + '\n')
            file.write(detail_text[j] + '. ' + '\n')
        j +=1
    i += 1
    #Просто смотрим список уникальных заголовков
    print(uniq1)
    #Если прошло достаточное количество прогонов, выходим из цикла
    if i == 8:
        f = False
    #Задерживаем выполнение программы на 30 минут, чтобы новости успели обновиться
    time.sleep(1800)
file.close()