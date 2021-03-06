#fix******
from werkzeug import url_encode

#Init
from flask import Flask
app = Flask(__name__)

#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
    return "<html><head></head> <body> Hello World! </body></html>"

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)

from flask import render_template

#наша новая функция сайта
@app.route("/data_to")
def data_to():
    #создаем переменные с данными для передачи в шаблон
    some_pars = {'user':'Ivan','color':'red'}
    some_str ='Hello my dear friends!'
    some_value = 10
    #передаем данные в шаблон и вызываем его
    return render_template('simple.html',some_str = some_str,

some_value = some_value,some_pars=some_pars)

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, BooleanField
# модули валидации полей формы
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] ='6Ldp9CMbAAAAACpWJaajNGHDrVxj1nChAljJeOTh'
app.config['RECAPTCHA_PRIVATE_KEY'] ='6Ldp9CMbAAAAAKhvub9yxpRVKtGEqXxx_S5076Qf'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
    # поле для введения строки, валидируется наличием данных
    # валидатор проверяет введение данных после нажатия кнопки submit
    # и указывает пользователю ввести данные если они не введены
    # или неверны
    openid = StringField('openid', validators = [DataRequired()])
    size = IntegerField('size', validators = [DataRequired()])
    color_red = IntegerField('color_red', validators = [NumberRange(min=0,max=1)])
    color_green = IntegerField('color_green', validators = [NumberRange(min=0,max=1)])
    color_blue = IntegerField('color_blue', validators = [NumberRange(min=0,max=1)])
    chb = BooleanField('show frame')
    # поле загрузки файла
    # здесь валидатор укажет ввести правильные файлы
    upload = FileField('Load image', validators=[
        FileRequired(),
        FileAllowed(['jpg','png','jpeg'],'Images only!')])
    # поле формы с capture
    recaptcha = RecaptchaField()
    #кнопка submit, для пользователя отображена как send
    submit = SubmitField('send')

# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os
# подключаем наш модуль и переименовываем
# для исключения конфликта имен
import net as neuronet
# метод обработки запроса GET и POST от клиента
from io import BytesIO
import base64
from PIL import Image
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

@app.route("/net",methods=['GET','POST'])
def net():
    # создаем объект формы
    form = NetForm()
    # обнуляем переменные передаваемые в форму
    filename=None
    neurodic = {}
    
    # Определяем нужные переменные
    image_ = [[]]
    size = 0
    chb = 0
    S = ""
    B = S.encode("UTF-8")
    plot_url = base64.b64encode(B)
    plot_frame = base64.b64encode(B)
    #******
    # проверяем нажатие сабмит и валидацию введенных данных
    if form.validate_on_submit():
        # файлы с изображениями читаются из каталога static
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        fcount, fimage = neuronet.read_image_files(10,'./static')
        # передаем все изображения в каталоге на классификацию
 
        size = form.size.data
    
        color_red = form.color_red.data
        color_green = form.color_green.data
        color_blue = form.color_blue.data
        
        chb = form.chb.data
                
        images_resized = [[]]
        height = 256
        width = 256
        image_ = np.array(fimage[0].resize((height,width)))/255.
        image_ = np.array(image_)
        # Создание представления в оттенках серого
        grey = 0.299*image_[:,:,0] + 0.587*image_[:,:,1] + 0.114*image_[:,:,2]
        img = BytesIO()
        
        # Построение и кодирование гистограммы
        ax = sns.distplot(grey, kde=False, bins=30)
        fig = ax.get_figure()
        fig.savefig(img, format='png')
        #fig.close()
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        # Отрисовка рамки
        if(chb==1):
            plt.axis('off')
            
        img_frame = BytesIO()
        frame = size
        n_image = np.zeros((256+frame*2, 256+frame*2, 3))
        n_image[:,:,0:3] = [color_red, color_green, color_blue]
        for i in range(256):
          for j in range(256):
            n_image[i+frame][j+frame] = image_[i][j]
        ax_frame = plt.imshow(n_image)
        fig_frame = ax_frame.get_figure()
        fig_frame.savefig(img_frame, format='png')


        img_frame.seek(0)
        plot_frame = base64.b64encode(img_frame.getvalue()).decode('utf8')
        #*********
        
        decode = neuronet.getresult(fimage)
        # записываем в словарь данные классификации
        for elem in decode:
            neurodic[elem[0][1]] = elem[0][2]
        # сохраняем загруженный файл
        form.upload.data.save(filename)
    # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
    # сети если был нажат сабмит, либо передадим falsy значения
    return render_template('net.html',form=form,image_name=filename,neurodic=neurodic,
                           plot_url=plot_url, plot_frame=plot_frame, chb=chb)

from flask import request
from flask import Response
import base64
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
#end
