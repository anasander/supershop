from flask import Flask, render_template, request, url_for, redirect, make_response
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/supershop'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://supershop:1234567890@localhost:3306/supershop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column('usuario_id', db.Integer, primary_key=True)
    name = db.Column('usuario_nome', db.String(100))
    email = db.Column('usuario_email', db.String(100))
    password = db.Column('usuario_senha', db.String(100))
    address = db.Column('usuario_endereco', db.String(200))

    def __init__(self, name, email, password, address):
        self.name = name
        self.email = email
        self.password = password
        self.address = address

@app.route("/")
def index():
    return render_template("index.html", titulo="Página Inicial")

@app.route("/cadastro/usuario")
def usuario():
    return render_template("usuario.html", usuarios = Usuario.query.all(), titulo="Usuário")

@app.route("/cadastro/caduser", methods=["POST"])
def caduser():
    usuario = Usuario(
        request.form.get("name"),
        request.form.get("email"),
        request.form.get("password"),
        request.form.get("address")
    )
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/cadastro/produto")
def cadastroProduto():
    return render_template("cadastroProduto.html", titulo="Cadastro de Produto")

@app.route("/produtos")
def produtos():
    return render_template("produtos.html", titulo="Produtos")

@app.route("/produtos/compra")
def compra():
    print("Produto comprado com sucesso!")
    return render_template("compra.html", titulo="Produto Comprado!")

@app.route("/produtos/venda")
def venda():
    print("Produto vendido com sucesso!")
    return render_template("venda.html", titulo="Produto Vendido!")

@app.route("/produtos/favoritos")
def favoritos():
    print("Produto adicionado aos favoritos!")
    return render_template("favoritos.html", titulo="Produtos Favoritos")

@app.route("/config/categoria")
def configCategoria():
    return render_template("configCategoria.html", titulo="Configuração de Categoria")

@app.route("/relatorios/vendas")
def relatorioVendas():
    return render_template("relatorioVendas.html", titulo="Relatório de Vendas")

@app.route("/relatorios/compras")
def relatorioCompras():
    return render_template("relatorioCompras.html", titulo="Relatório de Compras")

if __name__ == "supershop":
    with app.app_context():
        db.create_all()