#!/usr/bin/python3

from flask import Flask, request, render_template, redirect
import yt_dlp as youtube_dl
import pandas as pd
import numpy as np
import os
import guigolock as ggl

app = Flask(__name__)
if os.path.exists("/home/pi/karaokeApplication/catalogo.csv"):
    df = pd.read_csv("/home/pi/karaokeApplication/catalogo.csv", delimiter =',', encoding = 'utf-8', dtype=str)
else:
    df = pd.read_csv("./catalogo.csv", delimiter=',', encoding='utf-8', dtype=str)
if os.path.exists("catalogo_custom.csv"):
    dfc = pd.read_csv("catalogo_custom.csv", delimiter =',', encoding = 'utf-8', dtype=str)
    dt = pd.concat([df, dfc])
else:
    dfc = pd.DataFrame(columns=df.columns)
    dt = df

def downloadYouTube(videourl, path, name):
    ydl_opts = {
        'outtmpl': name + ".mp4" , 'format' : 'mp4'
    }
    os.chdir(path)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videourl])
    if os.path.exists("/home/pi/karaokeApplication/"):
        os.chdir("/home/pi/karaokeApplication/")
    else:
        os.chdir("../")

@app.route('/', methods=['GET', 'POST'])
def html_table():
    text = request.form.get('textbox') 
    print(text)
    if text is None:
        return render_template('cataLogo.html',  tables=[dt.iloc[:,[0,2,3,4]].to_html(classes='data', index=False)], titles=dt.iloc[:,[0,2,3,4]].columns.values)
    else:
        rows = np.column_stack([dt[col].str.contains(text, na=False, case=False) for col in dt])
        return render_template('cataLogo.html',  tables=[dt.iloc[:,[0,2,3,4]][rows.any(axis=1)].to_html(classes='data', index=False)], titles=dt.iloc[:,[0,2,3,4]].columns.values)

@app.route('/fila', methods=['GET', 'POST'])
def filas():
    fila = pd.read_csv('./filomena', index_col=[0])
    print(fila)
    return render_template('fila.html',  tables=fila, titles=fila.columns.values)

@app.route('/fila_adm', methods=['GET', 'POST'])
def fila_adm():
    fila = pd.read_csv('./filomena', index_col=[0])
    print(fila)
    return render_template('fila_adm.html',  tables=fila)

@app.route('/delete/<musc_id>', methods=['POST'])
def delete_music(musc_id):
    print(musc_id)
    a = musc_id.split('_')
    b = int(a[0])
    c = int(a[1])
    while ggl.check_free('./filomena', 'ctp') != True:
        print('filomena presa')
    fila = pd.read_csv('./filomena', index_col=[0])
    if len(fila['codigo']) > 1 and fila['codigo'].iloc[b] == c:
        fila = fila.drop(b)
        fila = fila.reset_index(drop=True)
    elif len(fila['codigo']) == 1 and int(fila['codigo']) == c:
        fila = fila.drop(b)
        fila = fila.reset_index(drop=True)
    else:
        print("tamo deletano coisa errada irmao")
    fila.to_csv('./filomena')
    while ggl.release('./filomena', 'ctp') != True:
        print('incapaz de liberar filomena')
    return redirect('/fila_adm')

@app.route('/up/<musc_id>', methods=['POST'])
def up_music(musc_id):
    print(musc_id)
    a = musc_id.split('_')
    b = int(a[0])
    c = int(a[1])
    while ggl.check_free('./filomena', 'ctp') != True:
        print('filomena presa')
    fila = pd.read_csv('./filomena', index_col=[0])
    if len(fila['codigo']) > 1 and b != 0 and fila['codigo'].iloc[b] == c:
        tempind = fila.index.values.copy()
        tempind[b] = b-1
        tempind[b-1] = b
        fila = fila.reindex(tempind)
        fila = fila.reset_index(drop=True)
    else:
        print("tamo movendo coisa errada irmao")
    fila.to_csv('./filomena')
    while ggl.release('./filomena', 'ctp') != True:
        print('incapaz de liberar filomena')
    return redirect('/fila_adm')

@app.route('/down/<musc_id>', methods=['POST'])
def down_music(musc_id):
    print(musc_id)
    a = musc_id.split('_')
    b = int(a[0])
    c = int(a[1])
    while ggl.check_free('./filomena', 'ctp') != True:
        print('filomena presa')
    fila = pd.read_csv('./filomena', index_col=[0])
    if len(fila['codigo']) > 1 and b < len(fila['codigo'])-1 and fila['codigo'].iloc[b] == c:
        tempind = fila.index.values.copy()
        tempind[b] = b+1
        tempind[b+1] = b
        fila = fila.reindex(tempind)
        fila = fila.reset_index(drop=True)
    else:
        print("tamo movendo coisa errada irmao")
    fila.to_csv('./filomena')
    while ggl.release('./filomena', 'ctp') != True:
        print('incapaz de liberar filomena')
    return redirect('/fila_adm')

@app.route('/download', methods=['GET', 'POST'])
def download():
    return render_template('download.html')

@app.route('/handle_download', methods=['GET', 'POST'])
def handle_download():
    global dfc
    global dt
    global df
    url = request.form.get('URL')
    artista = request.form.get('artista')
    musica = request.form.get('musica')
    number = '90000'
    if not dfc.empty:
        number = str(int(dfc['code'].max()) + 1)
    if os.path.exists("/media/pi/Elements/karaoke/musicas/"):
        downloadYouTube(url, "/media/pi/Elements/karaoke/musicas/", number)
    else:
        downloadYouTube(url, "./musicas/", number)
    dfc = dfc.append(pd.Series([number, number + ".mp4" , artista, musica, "nan"], index=dfc.columns ), ignore_index=True)
    dfc.to_csv('catalogo_custom.csv', index=False, sep =',')
    dt = pd.concat([df, dfc])
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')



    
