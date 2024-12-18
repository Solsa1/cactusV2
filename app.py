from flask import *
from flask_session import Session
import sqlite3
import base64
import io

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]  = "filesystem"
Session(app)

session = {}

jogos = [] # Váriavel para mostrar os jogos dentro da biblioteca do usuario

database = 'database.db'
#USER
#-----------------------------------------------------------------------------------

@app.route('/atualizarUsuario')
def atualizarUsuario():
    return render_template('/user/atualizarUsuario.html', user=session)

@app.route('/comprasUsuario')
def comprasUsuario():
    return render_template('/user/compras.html')

@app.route('/usuario')
def usuario():
    return render_template('/user/usuario.html', user = session)


# Rota que devolve a tela de cadastro para adicionar os USUARIOS
@app.route("/cadastroUsuario")
def cadastroUsuario():
    return render_template("/user/cadastroUser.html")

@app.route('/deletarUsuario')
def deletarUsuario():
    return render_template('/user/deletar.html')

#------------------------------------------------------------------------------------------------------------------
# Rota que inicia o codigo no index.html
@app.route('/')
def home():
    return render_template('landingpage.html')

# Rota para facilitar o uso de url_for para voltar a pagina inicial
@app.route('/home')
def casa():
    return render_template('index.html')

# rota pra landing page
@app.route('/landing')
def landing():
    return render_template('landingpage.html')

@app.route('/login')
def login():
    return render_template('login.html')


# EMPRESA
#-------------------------------------------------------------------------------------------
@app.route('/cadastroEmpresa')
def cadastroEmpresa():
    return render_template('empresa/cadastrar.html')

@app.route('/empresa')
def empresa():
    return render_template('empresa/main.html', empresa=session)

@app.route('/atualizarEmpresa')
def atualizarEmpresa():
    return render_template('empresa/atualizar.html')

@app.route('/deletarEmpresa')
def deletarEmpresa():
    return render_template('empresa/deletar.html')

#-------------------------------------------------------------------------------------------

# rota para página usuario.html que tem a biblioteca do usuáriox'x
@app.route('/minhaConta', methods=["GET"], endpoint="minhaConta")
def lib():
    emailUser = session['email']
    print(session)
    
    identificador = getIddUsuario(emailUser)
    if identificador is None:
        flash('usuario nao encontrado')
        return redirect(url_for('login'))
    else:

        db = getDb()

        cursor = db.cursor()
        cursor.execute('SELECT * from usuario where id = ?', (identificador, ))

        usuariolog = (cursor.fetchone())
        print(usuariolog)
        db.commit()

    #cursor.execute('SELECT * FROM biblioteca where id_user = ?', (id, ))
    #biblioteca = dict(cursor.fetchone)


    return render_template('/user/usuario.html', user=dict(usuariolog))


# Função que PEGA o ID do USUARIO para checar a sua BIBLIOTECA
# SOMENTE deve ser USADA para MOSTRAR os JOGOS da BIBLIOTECA do USUARIO LOGADO
# PASSIVEL DE MUDANÇAS
def verLib (nomeUser):
    identificador = getIdUsuario(nomeUser)
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('SELECT id_jogo FROM biblioteca WHERE id_user = ?', (identificador,))
        jogo_ids = cursor.fetchall()
        jogos = []
        for jogo_id in jogo_ids:
            cursor.execute('SELECT * FROM jogo WHERE id = ?', (jogo_id[0],))
            jogo = dict(cursor.fetchone())
            if jogo['foto'] != None:
                jogo['foto'] = base64.b64encode(io.BytesIO(jogo['foto']).getvalue()).decode()
            jogos.append(jogo)
        db.commit()
        return jogos
    except sqlite3.Error as e:
        print('Falha na busca')
        print(e)
    finally:
        db.close()

#Função que pega o ID das EMPRESAS com base no nome do JOGO
def getIdEmpresaJogo(nome):
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('SELECT id_empre FROM jogo WHERE nome = ?', (nome, ))
        jogo1 = cursor.fetchone()
        return jogo1[0]
    except sqlite3.Error as e:
        print("Erro ao buscar o ID do jogo:")
        print(e)
    finally:
        db.close()


#Função que pega o ID das EMPRESAS com base no seu próprio NOME
#Passivel a mudanças
def getIdEmpresa(nome):
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('SELECT id FROM empresa WHERE nome = ?', (nome, ))
        empresa1 = cursor.fetchone()
        return empresa1[0]
    except sqlite3.Error as e:
        print('Erro para conseguir o id da empresa desejada')
        print(e)
    finally:
        db.close()


#Função que adquire o ID do JOGO com base no seu NOME
#Passivel a mudanças
def getIdJogo(nome):
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('SELECT id FROM jogo WHERE nome = ?', (nome,))
        jogo = cursor.fetchone()
        return jogo[0]
    except sqlite3.Error as e:
        print("Erro ao buscar o ID do jogo:")
        print(e)
    finally:
        db.close()


#Função que adquire o ID do USUARIO com base no seu EMAIL
#Passivel a ser adicionado um novo parametro com a SENHA
def getIddUsuario(email):
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('SELECT id FROM usuario WHERE email = ?', (email, ))
        usuario1 = cursor.fetchone()
        if usuario1 is None:
            return None
        else:
            return usuario1[0]
    
    except sqlite3.Error as e:
        print('Erro para conseguir o id do usuario desejado')
        print(e)
    finally:
        db.close()


#Função que adquire o ID do USUARIO com base no seu NOME
#Passivel a mudanças
def getIdUsuario(nome):
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('SELECT id FROM usuario WHERE nome = ?', (nome, ))
        usuario1 = cursor.fetchone()
        return usuario1[0]
    except sqlite3.Error as e:
        print('Erro para conseguir o id do usuario desejado')
        print(e)
    finally:
        db.close()


#Função chave para a conexão com o banco de dados
#QUALQUER MUDANÇA NESTA FUNÇÃO PODE QUEBRAR O CÓDIGO POR COMPLETO CUIDADO
def getDb():
    db = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    return db


#Função chave para a criação das tabelas do banco de dados
#QUALQUER MUDANÇA NESTA FUNÇÃO PODE QUEBRAR O CÓDIGO POR COMPLETO CUIDADO
def init_db():
    with app.app_context():
        db = getDb()
        with app.open_resource('bdcreate.sql', mode='r') as bd: 
            script = bd.read() 
            db.cursor().executescript(script)
        db.commit()

# SESSION
# Passivel a ser modificado para adicionar um novo parametro com a SENHA
@app.route('/setcookie', methods=['POST'])
def setCookie():
#def setCookie():
    '''session['email'] = request.form['loginEmail']
    session['password'] = request.form['senhaEmail']
    password = session['password']'''
    email = request.form['loginEmail']
    identificador = getIddUsuario(email)
    if type(identificador) is not None:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('SELECT * from usuario where id = ?', (identificador, ))
        usuariolog = cursor.fetchone()
        usuario = dict(usuariolog)
        for i in usuario.keys():
            session[i] = usuario[i]
        print(session['nome'])
        db.commit()
        return redirect(url_for('minhaConta'))
    else:
        print('erro em encontrar o usuario')
        return redirect(url_for('login'))
    

        

# Rota que confere se a SESSION está funcionando

# TOTALMENTE DESNECESSÁRIO **** NA PRODUÇÃO ****
# assinado: Idinaldo
"""
@app.route('/getcookie')
def getVariable():
#def getCookie():
    uname = session.get("username", None)
    return f"The username is {uname}"
"""


#Função para a CRIAÇÃO de EMPRESA
#Deve ser utilizada SOMENTE na tela de CADASTRO de EMPRESAS
@app.route('/criarEmpresa', methods=['POST'])
def criarEmpresa():
    nome = request.form['nomeEmpresa']
    email = request.form['emailEmpresa']
    senha = request.form['senhaEmpresa']
    logo = request.files['logo']
    imagem = logo.read()
    descricao = request.form['descricaoEmpresa']
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('INSERT INTO empresa(nome, email, senha, logo, descricao) VALUES (?, ?, ?, ?, ?)', (nome, email, senha, imagem, descricao))
        db.commit()
        return 
    except sqlite3.Error as e:
        print('Houve um erro na inserção da empresa')
        print(e)
    finally:
        db.close()


# Função que ATUALIZA todos os DADOS DE EMRPRESA
# SOMENTE deve ser utilizada para EMPRESAS logadas no mommento, entender como faz isso utilizando SESSION
@app.route('/atualizarEmpre', methods=['POST'])
def atualizarEmpre():
    nome_antigo = request.form['antigoNomeEmpresa']
    identificador = getIdEmpresa(nome_antigo)
    nome_novo = request.form['novoNomeEmpresa']
    email_novo = request.form['novoEmailEmpresa']
    senha_nova = request.form['novaSenhaEmpresa']
    logo_nova = request.files['novoLogo']
    imagem = logo_nova.read()
    desc_nova = request.form['novaDescricaoEmpresa']
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None:
            cursor.execute('UPDATE empresa SET nome = ?, email = ?, senha =?, logo = ?, descricao = ? WHERE id = ?', (nome_novo, email_novo, senha_nova, imagem, desc_nova, identificador))
        else:
            print('Houve uma falha na atualização dos dados')
        db.commit()
    except sqlite3.Error as e:
        print('Ocorreu um erro na busca no banco de dados')
        print(e)
    finally:
        db.close()
        return redirect('/')


# Função que DELETA todos os dados de EMPRESAS
# SOMENTE deve ser usada por EMPRESAS logadas no momento
@app.route('/deletarEmpre', methods=['POST'])
def deletarEmpre():
    nome_antigo = request.form['antigoNomeEmpresa']
    identificador = getIdEmpresa(nome_antigo)
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None:
            cursor.execute('DELETE FROM empresa WHERE id = ?', (identificador, ))
        else:
            print('Ocorreu um erro no processo de deletar a empresa')
        db.commit()
    except sqlite3.Error as e:
        print('Não foi possivel deletar a empresa')
        print(e)
    finally:
        db.close()
        return redirect('/')


# Funçãp que CRIA USUARIOS
# SOMENTE deve ser usada na tela de CADASTRO de USUARIOS
@app.route('/criarUsuario', methods=['POST'])
def criarUsuario():
    nome = request.form['nomeUsuario']
    email = request.form['emailUsuario']
    senha = request.form['senhaUsuario']
    foto = request.files['fotoUsuario']
    imagem = foto.read()
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('INSERT INTO usuario(nome, email, senha, foto) VALUES (?, ?, ?, ?)', (nome, email, senha, imagem))
        db.commit()
    except sqlite3.Error as e:
        print('Erro na criação do usuario')
        print(e)
    finally:
        db.close()
        return redirect('/')

# Função que ATUALIZA USUARIOS
# SOMENTE deve ser USADA pelo USUARIO LOGADO no momento
@app.route('/atualizarUser', methods=['POST'])
def atualizarUser():
    nome_antigo = session['nome']
    identificador = getIdUsuario(nome_antigo)
    nome_novo = request.form['novoNomeUsuario']
    email_novo = request.form['novoEmailUsuario']
    senha_nova = request.form['novaSenhaUsuario']
    foto_nova = request.files['novoFotoUsuario']
    imagem = foto_nova.read()
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None:
            cursor.execute('UPDATE usuario SET nome = ?, email = ?, senha =?, foto =? WHERE id=?', (nome_novo, email_novo, senha_nova, imagem, identificador))
            db.commit()
            return render_template('usuario.html')
        else:
            print('Falha na atualização dos dados do usuario')
        db.close()
    except sqlite3.Error as e:
        print('Houve um erro na atualização dos dados')
        print(e)




# Função que DELETA USUARIOS
# SOMENTE deve ser USADA por USUARIOS LOGADOS no momento
app.route('/deletarUser', methods=['POST'])
def deletarUser():
    nome_antigo = session['nome']
    identificador = getIdUsuario(nome_antigo)
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None:
            cursor.execute('DELETE FROM usuario WHERE id =?', (identificador, ))
        else:
            print('Houve um erro na remoção do usuario')
        db.commit()
    except sqlite3.Error as e:
        print('Houve um erro no banco de dados')
        print(e)
    finally:
        db.close()
        return redirect('/')

# Função que CRIA JOGOS
# SOMENTE deve ser UTILIZADA por EMPRESAS LOGADAS no momento
# PASSIVEL A MUDANÇAS
@app.route('/criarJogos', methods=['POST'])
def criarJogos():
    nome_empresa = request.form['nomeEmpresa']
    identificador = getIdEmpresa(nome_empresa)
    nome_jogo = request.form['nomeJogos']
    preco_jogo = request.form['precoJogo']
    descricao_jogo = request.form['descricaoJogo']
    foto_jogo = request.files['fotoJogo']
    imagem = foto_jogo.read()
    dataL_jogo = request.form['dataLJogo']
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador:
            cursor.execute('INSERT INTO jogo(id_empre, nome, preco, descricao, foto, data_lancamento) VALUES (?,?,?,?,?,?)', (identificador, nome_jogo, preco_jogo, descricao_jogo, imagem, dataL_jogo))
        else:
            print('HOUVE UM ERRO NA INSERÇÃO DO JOGO')
        db.commit()
    except sqlite3.Error as e:
        print('ERRO NO BANCO')
        print(e)
    finally:
        db.close()
        return redirect('/')

# Função que ATUALIZA JOGOS
# SOMENTE deve ser UTILIZADA por EMPRESAS LOGADAS
# PASSIVEL A MUDANÇAS
@app.route('/atualizarJogos', methods=['POST'])
def atualizarJogos():
    nome_antigo = request.form['nomeAntigoJogo']
    identificador = getIdJogo(nome_antigo)
    nome_novo = request.form['nomeNovoJogo']
    preco_novo = request.form['precoNovoJogo']
    descricao_nova = request.form['descricaoNovoJogo']
    foto_nova = request.files['fotoNovoJogo']
    imagem = foto_nova.read()
    dataL_nova = request.form['dataLNovoJogo']
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None:
            cursor.execute('UPDATE jogo SET nome = ?, preco = ?, descricao =?, foto =?, data_lancamento =? WHERE id=?', (nome_novo, preco_novo, descricao_nova, imagem, dataL_nova, identificador))
        else:
            print('Falha na atualização dos dados do jogo')
        db.commit()
    except sqlite3.Error as e:
        print('Houve um erro na atualização dos dados')
        print(e)
    finally:
        db.close()
        return redirect('/')

# Função que DELETA JOGOS
# SOMENTE deve ser UTILIZADA por EMPRESAS LOGADAS
# PASSIVEL A MUDANÇAS
@app.route('/deletarJogo', methods=['POST'])
def deletarJogo():
    name = request.form['antigoNomeJogo']
    identificador = getIdJogo(name)
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None:
            cursor.execute('DELETE FROM jogo WHERE id =?', (identificador, ))
        else:
            print('Houve um erro na remoção do usuario')
        db.commit()
    except sqlite3.Error as e:
        print('Houve um erro no banco de dados')
        print(e)
    finally:
        db.close()
        return redirect('/')

# Função para efetuar COMPRAS de JOGOS
# Possivelmente adicionar uma API para efetuação de pagamento
@app.route('/comprarJogo', methods=['POST'])
def comprarJogo():
    comprador = session['nome']
    jogocomprado = request.form['jogoComprado']
    identificador = getIdJogo(jogocomprado)
    idenComp = getIdUsuario(comprador)
    idenVen = getIdEmpresaJogo(jogocomprado)
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('INSERT INTO vendas(id_jogo, id_comprador, id_vendedor) VALUES (?, ?, ?)', (identificador, idenComp, idenVen))
        cursor.execute('INSERT INTO biblioteca(id_jogo, id_user) VALUES (?, ?)', (identificador, idenComp))
        db.commit()
        db.close()
        return render_template('/user/usuario.html', user=session)
    except sqlite3.Error as e:
        print('Erro ao realizar compra')
        print(e)
        return render_template('/user/compras.html', comprador=session['nome'])


# Rota que ABRE a BIBLIOTECA do USUARIO LOGADO
# PASSIVEL A MUDANÇAS
@app.route('/bibliotecaUsuario')
def bibliotecaUsuario():
    jogos = verLib(session['nome'])
    return render_template('/user/biblioteca.html', jogos=jogos)



@app.route('/teste')
def teste():
    return render_template('teste-cookies.html', user=getIddUsuario())



# if para inicar o flask, sem isso não funciona.
if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', debug=True)
