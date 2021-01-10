import requests
import re
import json
from bs4 import BeautifulSoup
import os

obj = []
qualificationKeys = {'bak': 'Бакалавриат', 'pbak': 'Прикладной бакалавриат', 'mag': 'Магистратура', 'pmag': 'Прикладная магистратура', 'spec': 'Специалитет', 'asp': 'Аспирантура'}
formOfStudyKeys = {'ofo': 'Очная', 'zfo': 'Заочная', 'vqp': 'Заочная (ускоренная)', 'ozfo': 'Очно-заочная'}
viewKeys = {'sem': 'Рассписание занятий', 'sese': 'Промежуточная аттестация в форме экзамена', 'sesz': 'Промежуточная аттестация в форме зачета', 'glaz': 'График ликвидации академической задолженности', 'ses': 'Промежуточная аттестация'}
instituteKeys = {'iiif': 'Институт социальных и гуманитарных наук', 'ikit': 'Институт культуры и туризма', 'imeikn': 'Институт математики, естественных и компьютерных наук', 'imeit': 'Институт машиностроения, энергетики и транспорта', 'ippifv': 'Институт педагогики, психологии и физического воспитания', 'isi': 'Инженерно-строительный институт', 'iueiu': 'Институт управления, экономики и юриспруденции'}

print('Заходим на главную страницу')
response = requests.get('https://tt.vogu35.ru/')
soup = BeautifulSoup(response.text, features = "html.parser")

for a in soup.find_all('a'):
    link = a.get('href')
    
    if 'tt.vogu35.ru/files/' in link :
       
        name = re.search(r'(?<=files/).+', link).group(0)
        info = re.findall(r'[A-Za-z0-9.]+', name) 
        rusProfile = a.parent.parent.parent.find('h3').text

        [institute, qualification, formOfStudy, direction, profile, view, clas] = info
        clas = clas[0] + clas[1]
        pathFolder = qualification + '/' + formOfStudy + '/' + institute  + '/' + profile + '/' + direction + '/' + clas 
        path = pathFolder + '/' + view + '.pdf'
        print('Открываем ' + path)

        try:
            with open(os.getcwd() + '/files/' + path, 'wb') as f:
                print('Заходим на ' + link)
                f.write(requests.get(link).content)
        except FileNotFoundError:
            print('Создаем ' + os.getcwd() + '/files/' + pathFolder)
            os.makedirs(os.getcwd() + '/files/' + pathFolder)
            with open(os.getcwd() + '/files/' + path, 'wb') as f:
                print('Заходим на ' + link)
                f.write(requests.get(link).content)
       
        datadict = {'direction': direction, 'url': link, 'profile': rusProfile, 'clas': clas[1] + ' курс', 'view': viewKeys[view], 'qualification': qualificationKeys[qualification], 'formOfStudy': formOfStudyKeys[formOfStudy], 'institute': instituteKeys[institute], 'path': path}
        obj.append(datadict)
        
with open('./files/data.json', 'w') as fl:
    fl.write(json.dumps(obj))


