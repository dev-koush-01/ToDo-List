from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class ToDo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def myTodo():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    allTodo=ToDo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    Todo=ToDo.query.filter_by(sno=sno).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>",methods=['GET', 'POST'])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=ToDo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    Todo=ToDo.query.filter_by(sno=sno).first()
    return render_template("update.html", Todo=Todo)

@app.route("/show")
def production():
    allTodo=ToDo.query.all()
    print(allTodo)
    return "This is for production!"

if __name__=="__main__":
    # with app.app_context():
    #     print("Creating database...")
    #     db.create_all()
    #     print("Database created.")
    app.run(debug=True, port=3000)