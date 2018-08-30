import time
import pyphen
from gtts import gTTS
import os
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import render_template

import random
from glob import glob
import itertools

palavras = 'animais,urso,gato,pato,cachorro,passaro,tartaruga,dinossauro,elefante,leão,onça,lobo,canguru,peixe,tubarão,baleia,macaco,girafa,'
palavras += 'universo,sol,lua,mercurio,venus,terra,marte,jupiter,saturno,urano,netuno,plutão,estrela,orbita,satelite,'
palavras += 'familia,papai,mamãe,vovô,vovó,titio,titia,tio,tia,sobrinho,sobrinha,primo,prima,cultura,'
palavras += 'carro,caminhão,barco,navio,avião,trem,BRT,metro,barca,'
palavras += 'presidente,governador,senador,politico,sociedade,'
palavras += 'chuva,armario,mesa,quadro,luz,janela,porta,sofa,tapete,televisão,computador,caixa,linha,ferro,bolsa,'
palavras += 'escola,mochila,lapis,borracha,apontador,amigo,colega,amiga,professor,professora,estojo,livro,história,matemática,número,'
palavras += 'osso,cerebro,perna,braço,corpo,barriga,abdomêm,olho,orelha,ouvido,sobrancelha,nariz,narina,pé,mão,cotovelo,joelho,peito,'
palavras += 'natação,futebol,volei,praia,surf,handbol,tenis,'
palavras += 'um,dois,três,quatro,cinco,seis,sete,oite,nove,dez,onze,douze,trezê,quatorze,quinze,dezesseis,dezessete,dezoito,dezenove,vinte,'
palavras += 'morango,pessego,banana,maracuja,melancia,laranja,uva,goiba,pêra,maçã,acerola,açaí,pitaía,mertilo,kiwi,limão,'
palavras += 'beterraba,batata,cenoura,inhame,abobora,tomate,cebola,pimentão,pimenta,azeite,azeitona,'
palavras += 'ovo,pão,macarrão,arroz,feijão,salsicha,espinafre,alface,milho,pipoca,'
palavras += 'flôr,rosa,margarida,bromelha,'
palavras += 'remédio,tosse,espirro,'
palavras += 'incetos,escorpião,grilo,gafanhoto,barata,aranha,minhoca,formiga,lacraia,centopéia,gongolô,'
palavras += 'bactéria,microscópio,saúde,centrifuga,laboratório,ciêntista,'


palavras = palavras.split(',')

app = Flask(__name__)

@app.route("/junta-silabas/<path:palavra>")
def junta_silaba(palavra):
    resp = base(palavra)
    pls = random.choices(palavras, k=3)
    dic = pyphen.Pyphen(lang='pt_BR')
    silabas = '-'.join([dic.inserted(pl) for pl in pls]).split('-') + resp['silabas']
    random.shuffle(silabas)
    resp['silabas_random'] = [x for x in silabas if x]
    return render_template('junta-silabas.html', **resp)

@app.route("/escrever/<path:palavra>")
def escrever(palavra):
    resp = base(palavra)
    return render_template('escrever.html', **resp)


@app.route("/ouvir/<path:palavra>")
def ouvir(palavra):
    resp = base(palavra)
    return render_template('ouvir.html', **resp)
    
@app.route('/sound/<path:path>')
def get_resource(path):
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
        ".mp3": "audio/mpeg"
    }
    complete_path = os.path.join('static', path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = open(complete_path, 'rb')
    return Response(content, mimetype=mimetype)

@app.route('/')
def index():
    return render_template('index.html')


def base(palavra):
    if  palavra == 'random':
        palavra = random.choice(palavras)
    if not os.path.exists('static/%s.mp3' % palavra):
        tts = gTTS(text=palavra, lang='pt-BR')
        tts.save('static/%s.mp3' % palavra)
    dic = pyphen.Pyphen(lang='pt_BR')
    silabas = [x for x in dic.inserted(palavra).split('-') if x]
    for silaba in silabas:
        if not os.path.exists('static/%s.mp3' % silaba):
            tts = gTTS(text=silaba, lang='pt-BR')
            tts.save('static/%s.mp3' % silaba)
    resp = {}
    dic = pyphen.Pyphen(lang='pt_BR')
    #busca = requests.get('https://www.google.com.br/search?q=urso&source=lnms&tbm=isch')
    resp['silabas'] = dic.inserted(palavra).split('-')
    resp['song'] = '%s.mp3' % palavra
    resp['palavra'] = palavra
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
