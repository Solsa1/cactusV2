from flask import *
import sqlite3

app = Flask(__name__)

database = 'database.db'

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

def getDb():
    db = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = getDb()
        with app.open_resource('bdcreate.sql', mode='r') as bd: 
            script = bd.read() 
            db.cursor().executescript(script)
        db.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/criarEmpresa', methods=['POST'])
def criarEmpresa():
    nome = request.form['nomeEmpresa']
    email = request.form['emailEmpresa']
    senha = request.form['senhaEmpresa']
    logo = request.form['logo']
    descricao = request.form['descricaoEmpresa']
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('INSERT INTO empresa(nome, email, senha, logo, descricao) VALUES (?, ?, ?, ?, ?)', (nome, email, senha, logo, descricao))
        db.commit()
    except sqlite3.Error as e:
        print('Houve um erro na inserção da empresa')
        print(e)
    finally:
        db.close()
        return redirect('/')

@app.route('/atualizarEmpresa', methods=['POST'])
def atualizarEmpresa():
    nome_antigo = request.form['antigoNomeEmpresa']
    identificador = getIdEmpresa(nome_antigo)
    nome_novo = request.form['novoNomeEmpresa']
    email_novo = request.form['novoEmailEmpresa']
    senha_nova = request.form['novaSenhaEmpresa']
    logo_nova = request.form['novoLogo']
    desc_nova = request.form['novaDescricaoEmpresa']
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None:
            cursor.execute('UPDATE empresa SET nome = ?, email = ?, senha =?, logo = ?, descricao = ? WHERE id = ?', (nome_novo, email_novo, senha_nova, logo_nova, desc_nova, identificador))
        else:
            print('Houve uma falha na atualização dos dados')
        db.commit()
    except sqlite3.Error as e:
        print('Ocorreu um erro na busca no banco de dados')
        print(e)
    finally:
        db.close()
        return redirect('/')
    
@app.route('/deletarEmpresa', methods=['POST'])
def deletarEmpresa():
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

@app.route('/criarUsuario', methods=['POST'])
def criarUsuario():
    nome = request.form['nomeUsuario']
    email = request.form['emailUsuario']
    senha = request.form['senhaUsuario']
    foto = request.form['fotoUsuario']
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute('INSERT INTO usuario(nome, email, senha, foto) VALUES (?, ?, ?, ?)', (nome, email, senha, foto))
        db.commit()
    except sqlite3.Error as e:
        print('Erro na criação do usuario')
        print(e)
    finally:
        db.close()
        return redirect('/')
    
@app.route('/atualizarUsuario', methods=['POST'])
def atualizarUsuario():
    nome_antigo = request.form['antigoNomeUsuario']
    identificador = getIdUsuario(nome_antigo)
    nome_novo = request.form['novoNomeUsuario']
    email_novo = request.form['novoEmailUsuario']
    senha_nova = request.form['novaSenhaUsuario']
    foto_nova = request.form['novoFotoUsuario']
    try:
        db = getDb()
        cursor = db.cursor()
        if identificador is not None:
            cursor.execute('UPDATE usuario SET nome = ?, email = ?, senha =?, foto =? WHERE id=?', (nome_novo, email_novo, senha_nova, foto_nova, identificador))
        else:
            print('Falha na atualização dos dados do usuario')
        db.commit()
    except sqlite3.Error as e:
        print('Houve um erro na atualização dos dados')
        print(e)
    finally:
        db.close()
        return redirect('/')
    
@app.route('/deletarUsuario', methods=['POST'])
def deletarUsuario():
    nome_antigo = request.form['antigoNomeUsuario']
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

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', debug=True)