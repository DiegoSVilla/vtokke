from flask import Flask, request, render_template
import youtube_dl
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
df = pd.read_csv("catalogo.csv", delimiter =',', encoding = 'utf-8', dtype=str)
if os.path.exists("catalogo_custom.csv"):
    dfc = pd.read_csv("catalogo_custom.csv", delimiter =',', encoding = 'utf-8', dtype=str)
    dt = pd.concat([df, dfc])
else:
    dfc = pd.DataFrame(columns=df.columns)
    dt = df

def downloadYouTube(videourl, path, name):
    ydl_opts = {
        'outtmpl': name + ".mp4" , 'format' : '137'
    }
    os.chdir(path)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videourl])
    os.chdir("/home/pi/karaokeApplication/")

@app.route('/', methods=['GET', 'POST'])
def html_table():
    text = request.form.get('textbox') 
    print(text)
    if text is None:
        return render_template('cataLogo.html',  tables=[dt.ix[:,[0,2,3,4]].to_html(classes='data', index=False)], titles=dt.ix[:,[0,2,3,4]].columns.values)
    else:
        rows = np.column_stack([dt[col].str.contains(text, na=False, case=False) for col in dt])
        return render_template('cataLogo.html',  tables=[dt.ix[:,[0,2,3,4]][rows.any(axis=1)].to_html(classes='data', index=False)], titles=dt.ix[:,[0,2,3,4]].columns.values)

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
    downloadYouTube(url, "/media/pi/Elements/karaoke/musicas/", number)
    dfc = dfc.append(pd.Series([number, number + ".mp4" , artista, musica, "nan"], index=dfc.columns ), ignore_index=True)
    dfc.to_csv('catalogo_custom.csv', index=False, sep =',')
    dt = pd.concat([df, dfc])
    return render_template('download.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')



    
