from flask import Flask, render_template, request, make_response
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", titulo="Página Inicial")

@app.route("/cadastro/usuario")
def cadastroUsuario():
    return render_template("usuario.html", titulo="Cadastro de usuário")

@app.route("/cadastro/caduser", methods=["POST"])
def caduser():
    return request.form

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