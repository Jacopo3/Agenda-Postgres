import psycopg2
import psycopg2.extras
import logging
import datetime
from crypt import methods
from flask import Flask, flash, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from wtforms import(
    StringField,
    SubmitField,
    DateField,
    TextAreaField,
    RadioField,
    validators
)

from database import (
    tasks,
    task_clo,
    leggi,
    scrivi,
    fatto_db,
    leggi_id,
    modifica_task)

app = Flask(__name__)
app.config["SECRET_KEY"] = 'qwertyuiop'


# , onchange="submit()"
class index_form_data(FlaskForm):
    data = DateField("Data: ")

@app.route("/index", methods=["GET","POST"])
@app.route("/", methods=["GET","POST"])
def index(data=None):
    if data == None: data = str(datetime.date.today())
    form_data = index_form_data()

    
    if form_data.is_submitted():
        data = form_data.data.data
    
    conn, cur = tasks()
    dati = leggi(cur, data)
    #app.logger.info(dati[0].get('titolo'))
    task_clo(conn, cur)
    
    return render_template("//index.html", dati = dati ,form_data = form_data ,data = data)


class nuovo_form(FlaskForm):
    titolo = StringField("Titolo della task",[validators.DataRequired()])
    descrizione = TextAreaField("Descrizione della task")
    data_task = DateField("Data task")
    Ripetizione_sett = RadioField('Ripetizione_settimanale', choices=[(0,'Lunedi'),
                                                                      (1,'martedi'),
                                                                      (2,'mercoledi'),
                                                                      (3,'giovedi'),
                                                                      (4,'venerdi'),
                                                                      (5,'sabato'),
                                                                      (6,'domenica'),
                                                                      ])
    Ripetizione_ann = DateField("Data Rp Annua")
    
    submit = SubmitField("Salva")


@app.route("/new/", methods=["GET","POST"])
def nuova():
    titolo = None
    descrizione = None
    data_task = None
    Ripetizione_sett = None
    Ripetizione_ann = None
    form = nuovo_form()

    if form.is_submitted():
        titolo = form.titolo.data
        descrizione = form.descrizione.data
        data_task = form.data_task.data
        Ripetizione_sett = form.Ripetizione_sett.data
        Ripetizione_ann = form.Ripetizione_ann.data
        app.logger.info([titolo, descrizione, data_task, Ripetizione_sett, Ripetizione_ann])
        if not (data_task != None or Ripetizione_sett != None or Ripetizione_ann != None):
            app.logger.info("Inserire uno degli ultimi dei 3 campi")
            flash("Manca una data")
        else:
            conn, cur = tasks()
            scrivi(conn, cur, [titolo, descrizione, data_task, Ripetizione_sett, Ripetizione_ann])
            task_clo(conn, cur)
            return redirect("/")
            

    
    return render_template("//nuovo.html", 
                            course_simple_form= form
                                )

@app.route("/fatto/", methods=["GET","POST"])
def fatto():
    id_task = request.args.get("id")
    value = request.args.get("check")
    data = request.args.get("data")
    
    conn, cur = tasks()
    fatto_db(conn, cur, id_task, value)
    task_clo(conn, cur)
    return index(data)


@app.route("/modifica/", methods=["GET", "POST"])
def modifica():
    id_task = request.args.get("id")

    conn, cur = tasks()
    task = leggi_id(cur, id_task)
    
    titolo = None
    descrizione = None
    data_task = None
    Ripetizione_sett = None
    Ripetizione_ann = None
    form = nuovo_form()
    
    if form.is_submitted():
        titolo = form.titolo.data
        descrizione = form.descrizione.data
        data_task = form.data_task.data
        Ripetizione_sett = form.Ripetizione_sett.data
        Ripetizione_ann = form.Ripetizione_ann.data

        if not (data_task != None or Ripetizione_sett != None or Ripetizione_ann != None):
            app.logger.info("Inserire uno degli ultimi dei 3 campi")
            flash("Manca una data")
        else:
            modifica_task(conn, cur, int(task[0].get('id')), [titolo, descrizione, data_task, Ripetizione_sett, Ripetizione_ann])
            return redirect("/")
    else:
        #app.logger.info(dati[0].get('titolo'))
        form.titolo.data            = task[0].get("titolo")
        form.descrizione.data       = task[0].get("descrizione")
        form.data_task.data         = task[0].get("data")
        giorno_sett_rp = task[0].get("giorno_sett_rp")
        if giorno_sett_rp != None:
            flash(f"Viene ripetuto settimanalmente ogni {dict([(0,'Lunedi'), (1,'martedi'), (2,'mercoledi'), (3,'giovedi'), (4,'venerdi'), (5,'sabato'),(6,'domenica'),]).get(int(giorno_sett_rp))}")
        form.Ripetizione_ann.data   = task[0].get("annua_rp")
        flash(f"Id in modifica: {task[0].get('id')}")
        
    task_clo(conn, cur)
    return render_template("//modifica.html", course_simple_form= form)


if __name__ == "__main__":
    app.run(debug=True)
    