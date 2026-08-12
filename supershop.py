from flask import Flask, render_template, request, url_for, redirect, make_response
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/supershop'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://supershop:1234567890@localhost:3306/supershop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
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

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('categoria_id', db.Integer, primary_key=True)
    name = db.Column('categoria_nome', db.String(256))
    description = db.Column('categoria_desc', db.String(256))

    def __init__ (self, name, description):
        self.name = name
        self.description = description

class Produto(db.Model):
    __tablename__ = "produto"
    id = db.Column('produto_id', db.Integer, primary_key=True)
    name = db.Column('produto_nome', db.String(256))
    description = db.Column('produto_desc', db.String(256))
    quantity = db.Column('produto_qtd', db.Integer)
    price = db.Column('produto_preco', db.Float)
    category = db.Column('categoria_id',db.Integer, db.ForeignKey("categoria.categoria_id"))
    user = db.Column('usuario_id',db.Integer, db.ForeignKey("usuario.usuario_id"))

    def __init__(self, name, description, quantity, price, category_id, user_id):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.category_id = category_id
        self.user_id = user_id

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', titulo="Página não encontrada"), 404

@app.route("/")
def index():
    return render_template("index.html", titulo="Página Inicial")

@app.route("/cadastro/usuario")
def usuario():
    return render_template("usuario.html", usuarios = Usuario.query.all(), titulo="Usuário")

@app.route("/usuario/novo", methods=["POST"])
def novoUsuario():
    usuario = Usuario(
        request.form.get("name"),
        request.form.get("email"),
        request.form.get("password"),
        request.form.get("address")
    )
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/criar", methods=['POST'])
def criarUsuario():
    usuario = Usuario(request.form.get('user'), request.form.get('email'),request.form.get('password'),request.form.get('address'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhes/<int:id>")
def buscarUsuario(id):
    usuario = Usuario.query.get(id)
    return usuario.name

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarUsuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.name = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.password = request.form.get('password')
        usuario.address = request.form.get('address')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))

    return render_template('editarUsuario.html', usuario=usuario, titulo="Editar Usuário")

@app.route("/usuario/deletar/<int:id>")
def deletarUsuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))     

@app.route("/cadastro/produto")
def produtos():
    return render_template("produtos.html", produtos = Produto.query.all(), categorias = Categoria.query.all(), titulo="Produtos")

@app.route("/produto/novo", methods=["POST"])
def novoProduto():
    produto = Produto(request.form.get('name'), request.form.get('description'),request.form.get('quantity'),request.form.get('price'),request.form.get('category'),request.form.get('user'))
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('produtos'))

# @app.route("/produtos")
# def produtos():
#     return render_template("produtos.html", titulo="Produtos")

# @app.route("/produtos/compra")
# def compra():
#     print("Produto comprado com sucesso!")
#     return render_template("compra.html", titulo="Produto Comprado!")

# @app.route("/produtos/venda")
# def venda():
#     print("Produto vendido com sucesso!")
#     return render_template("venda.html", titulo="Produto Vendido!")

@app.route("/produtos/favoritos")
def favoritos():
    print("Produto adicionado aos favoritos!")
    return render_template("favoritos.html", titulo="Produtos Favoritos")

@app.route("/config/categoria")
def categoria():
    return render_template('configCategoria.html', categorias = Categoria.query.all(), titulo='Cadastro de Categorias')
    
@app.route("/categoria/novo", methods=['POST'])
def novaCategoria():
    categoria = Categoria(request.form.get('name'), request.form.get('description'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/relatorios/vendas")
def relatorioVendas():
    return render_template("relatorioVendas.html", titulo="Relatório de Vendas")

@app.route("/relatorios/compras")
def relatorioCompras():
    return render_template("relatorioCompras.html", titulo="Relatório de Compras")

if __name__ == "supershop":
    with app.app_context():
        db.create_all()