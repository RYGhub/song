import datetime as dt
from flask import Flask, session, request, render_template, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)

app.secret_key = "4pippo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


class Song(db.Model):
    __tablename__ = "song"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    word = db.Column(db.String, nullable=False)


@app.route('/', methods=["GET", "POST"])
def page_main():
    if request.method == "GET":
        if session.get("last_entry") and session["last_entry"] < dt.datetime.now() + dt.timedelta(1):
            done = True
        else:
            done = False
            session["last_entry"] = None
            session.permanent = True
        last_words = db.engine.execute("SELECT * FROM song ORDER BY time").fetchall()
        return render_template("song.html", last_words=last_words, done=done)
    elif request.method == "POST":
        if session.get("last_entry") and session["last_entry"] < dt.datetime.now() + dt.timedelta(1):
            abort(403)
        new_word = Song(time=dt.datetime.now(), word=request.form["word"].split(" ")[0])
        db.session.add(new_word)
        db.session.commit()
        session["last_entry"] = dt.datetime.now()
        session.permanent = True
        return redirect(url_for("page_main"))


if __name__ == '__main__':
    db.create_all()
    app.run()
