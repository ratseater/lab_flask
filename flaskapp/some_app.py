
from flask import request
from flask import Response
import base
from PIL import Image
from io import BytesIO
import json
# метод для обработки запроса от пользователя
@app.route("/apinet",methods=['GET','POST'])
def apinet():
    # проверяем что в запросе json данные
    if request.mimetype =='application/json':
        # получаем json данные
        data = request.get_json()
        # берем содержимое по ключу, где хранится файл
        # закодированный строкой base
        # декодируем строку в массив байт используя кодировку utf-
        # первые 128 байт ascii и utf-8 совпадают, потому можно
        filebytes = data['imagebin'].encode('utf-8')
        # декодируем массив байт base64 в исходный файл изображение
        cfile = base64.b64decode(filebytes)
        # чтобы считать изображение как файл из памяти используем BytesIO
        img = Image.open(BytesIO(cfile))
        decode = neuronet.getresult([img])
        neurodic = {}
        for elem in decode:
            neurodic[elem[0][1]] = str(elem[0][2])
            print(elem)
        # пример сохранения переданного файла
        # handle = open( _'_ ./static/f.png _'_ , _'_ wb _'_ )
        # handle.write(cfile)
        # handle.close()
        # преобразуем словарь в json строку
        ret = json.dumps(neurodic)
        # готовим ответ пользователю
        resp = Response(response=ret,
        status=200,
        mimetype="application/json")
    # возвращаем ответ
    return resp

import lxml.etree as ET

@app.route("/apixml",methods=['GET','POST'])
def apixml():
    #парсим xml файл в dom
    dom = ET.parse("./static/xml/file.xml")
    #парсим шаблон в dom
    xslt = ET.parse("./static/xml/file.xslt")
    #получаем трансформер
    transform = ET.XSLT(xslt)
    #преобразуем xml с помощью трансформера xslt
    newhtml = transform(dom)
    #преобразуем из памяти dom в строку, возможно, понадобится указать кодировку
    strfile = ET.tostring(newhtml)
    return strfile
