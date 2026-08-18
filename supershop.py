from flask import Flask, render_template, request, url_for, redirect, make_response
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/supershop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = 'supersecretkey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# CLASSES
class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usuario_id', db.Integer, primary_key=True)
    name = db.Column('usuario_nome', db.String(100))
    email = db.Column('usuario_email', db.String(100))
    password = db.Column('usuario_senha', db.String(255))
    address = db.Column('usuario_endereco', db.String(200))

    def __init__(self, name, email, password, address):
        self.name = name
        self.email = email
        self.password = password
        self.address = address

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

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
        self.category = category_id
        self.user = user_id

# TRATAMENTO DE ERROS
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', titulo="Página não encontrada"), 404

# LOGIN MANAGER
@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

# --- ROTAS ---

# INDEX
@app.route("/")
def index():
    return render_template("index.html", titulo="Página Inicial")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = hashlib.sha512(str(request.form.get("password")).encode('utf-8')).hexdigest()

        usuario = Usuario.query.filter_by(email=email, password=password).first()
        if usuario and usuario.password == password:
            login_user(usuario)
            return redirect(url_for("usuario"))
        else:
            return render_template("login.html", titulo="Login", error="Credenciais inválidas")
    return render_template("login.html", titulo="Login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# USUÁRIO
@app.route("/cadastro/usuario")
@login_required
def usuario():
    return render_template("usuario.html", usuarios=Usuario.query.all(), titulo="Usuário")

@app.route("/usuario/novo", methods=["POST"])
def novoUsuario():
    hash = hashlib.sha512(str(request.form.get("password")).encode('utf-8')).hexdigest()
    
    usuario = Usuario(
        request.form.get("name"),
        request.form.get("email"),
        hash, 
        request.form.get("address")
    )
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
        usuario.password = hashlib.sha512(str(request.form.get("password")).encode('utf-8')).hexdigest()
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
 
# PRODUTOS
@app.route("/cadastro/produto")
@login_required
def produtos():
    return render_template("produtos.html", produtos = Produto.query.all(), categorias = Categoria.query.all(), titulo="Produtos")

@app.route("/produto/novo", methods=["POST"])
def novoProduto():
    produto = Produto(request.form.get('name'), request.form.get('description'),request.form.get('quantity'),request.form.get('price'),request.form.get('category'),request.form.get('user'))
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('produtos'))

@app.route("/produto/editar/<int:id>", methods=['GET','POST'])
def editarProduto(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        produto.name = request.form.get('name')
        produto.description = request.form.get('description')
        produto.quantity = request.form.get('quantity')
        produto.price = request.form.get('price')
        produto.category = request.form.get('category')
        produto.user = request.form.get('user')
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('produtos'))

    categorias = Categoria.query.all()

    return render_template('editarProduto.html', produto=produto, categorias=categorias, titulo="Editar Produto")

@app.route("/produto/deletar/<int:id>")
def deletarProduto(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('produtos'))

# @app.route("/produtos/compra")
# def compra():
#     print("Produto comprado com sucesso!")
#     return render_template("compra.html", titulo="Produto Comprado!")

# @app.route("/produtos/venda")
# def venda():
#     print("Produto vendido com sucesso!")
#     return render_template("venda.html", titulo="Produto Vendido!")

@app.route("/produtos/favoritos")
@login_required
def favoritos():
    print("Produto adicionado aos favoritos!")
    return render_template("favoritos.html", titulo="Produtos Favoritos")

# CATEGORIAS
@app.route("/cadastro/categoria")
@login_required
def categoria():
    return render_template('cadastroCategoria.html', categorias = Categoria.query.all(), titulo='Cadastro de Categorias')
    
@app.route("/categoria/novo", methods=['POST'])
def novaCategoria():
    categoria = Categoria(request.form.get('name'), request.form.get('description'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/categoria/editar/<int:id>", methods=['GET','POST'])
def editarCategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.name = request.form.get('name')
        categoria.description = request.form.get('description')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))

    return render_template('editarCategoria.html', categoria=categoria, titulo="Editar Categoria")

@app.route("/categoria/deletar/<int:id>")
def deletarCategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

# RELATÓRIOS
@app.route("/relatorios/vendas")
@login_required
def relatorioVendas():
    return render_template("relatorioVendas.html", titulo="Relatório de Vendas")

@app.route("/relatorios/compras")
@login_required
def relatorioCompras():
    return render_template("relatorioCompras.html", titulo="Relatório de Compras")

# RENDERIZAÇÃO
if __name__ == "supershop":
    with app.app_context():
        db.create_all()