from flask import Flask
from flask import request
from flask import render_template, render_template_string
from flask import Flask, flash, redirect, render_template, \
     request, url_for

from search_bar import SearchBar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/')
def rien():
    return redirect('/MusicSearch')

@app.route('/MusicSearch', methods=('GET', 'POST'))
def MusicSearch():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success/'+form.typing.data)
    return render_template('sub.html', form=form)

@app.route('/success/<search_word>')
def sucess(search_word):
    return "Salut " + search_word + ".\nTu es arrivé jusque là. \n <a href='/MusicSearch'> Retour </a>"


@app.route('/results', methods=['GET', 'POST'])
def results():
  return 'succeed'


if __name__ == '__main__':
    app.run(debug=True, port=2745) 
