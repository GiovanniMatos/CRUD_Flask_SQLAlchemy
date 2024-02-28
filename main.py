from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funcionarios.db'
db = SQLAlchemy(app)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return render_template('funcionarios.html')

@app.route('/funcionarios', methods=['GET', 'POST'])
def mostrar_funcionarios():
    if request.method == 'POST':
        novo_nome = request.form['nome']
        novo_cargo = request.form['cargo']
        novo_funcionario = Funcionario(nome=novo_nome, cargo=novo_cargo)
        db.session.add(novo_funcionario)
        db.session.commit()

    funcionarios = Funcionario.query.all()
    return render_template('funcionarios.html', funcionarios=funcionarios)

@app.route('/apagar/<int:id>', methods=['POST'])
def apagar_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    db.session.delete(funcionario)
    db.session.commit()
    return redirect(url_for('mostrar_funcionarios'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    if request.method == 'POST':
        novo_nome = request.form['nome']
        novo_cargo = request.form['cargo']
        funcionario.nome = novo_nome
        funcionario.cargo = novo_cargo
        db.session.commit()
    return redirect(url_for('mostrar_funcionarios'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
