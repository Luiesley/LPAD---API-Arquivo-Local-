# pip install flask flask_sqlalchemy pymysql
# Permite a conexao da API com o banco de dados
# Flask - permite a criação de API com Python
# Response e Request -> Requisição

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask("vet")

# Rastrear as modificações realizadas
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuração de conexão com o banco
# 1- Usuario (root) 2- Senha (senai%40134) 3- localhost (127.0.0.1) 
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:senai%40134@127.0.0.1/clinicavetbd"

mydb = SQLAlchemy(app)

# Classe para definir o modelo dos dados que correspondem a tabela do banco de dados
class vet_Client(mydb.Model):
    __tablename__ = "tb_clientes"
    id_cliente = mydb.Column(mydb.Integer, primary_key=True)
    nome = mydb.Column(mydb.String(255))
    endereco = mydb.Column(mydb.String(255))
    telefone = mydb.Column(mydb.String(255))

    # Método para converter o objeto em JSON
    def to_json(self):
        return {
            'id_cliente': self.id_cliente,
            'nome': self.nome,
            'endereco': self.endereco,
            'telefone': self.telefone
        }

# ----------------------------------------------------------------------------------- #
# METODO 1 - GET
@app.route('/cliente_get', methods=['GET'])
def seleciona_clientes():
    cliente_selecionado = vet_Client.query.all()
    cliente_json = [cliente.to_json() for cliente in cliente_selecionado]
    return gera_resposta(200, "Lista de clientes", cliente_json)

# ----------------------------------------------------------------------------------- #
# RESPOSTA PADRAO
    # - Status (200, 201)
    # nome do conteudo
    # conteudo
    # mensagem (opcional)

def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body["Lista de Clientes"] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype='application/json')
        # Dumps - Converte o dicionario criado (body) em Json (json.dumps)


# ----------------------------------------------------------------------------------- #
# METODO 2 - GET (POR ID)

@app.route('/cliente_get/<int:id_cliente_pam>', methods=['GET'])
def seleciona_cliente_id(id_cliente_pam):
    cliente_selecionado = vet_Client.query.filter_by(id_cliente = id_cliente_pam).first()
    
    cliente_json = cliente_selecionado.to_json()

    return gera_resposta(200, cliente_json, 'cliente encontrado !')

# ----------------------------------------------------------------------------------- #
# METODO 3 - POST

@app.route('/cliente_post', methods=['POST'])
def criar_cliente():
    requisicao = request.get_json()

    try:
        cliente = vet_Client (
            id_cliente = requisicao['id_cliente'],
            nome = requisicao['nome'],
            endereco = requisicao['endereco'],
            telefone = requisicao['telefone']
        )

        mydb.session.add(cliente)

        # Adiciona ao banco
        mydb.session.commit()

        return gera_resposta(201, cliente.to_json(), 'Criado com sucesso')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta (400, {}, 'Erro ao cadastrar')



# -----------------------------------------------------------
# METODO 4 - DELETE

@app.route('/cliente_delete/<int:id_cliente_pam>', methods=['DELETE'])

def delete_cliente(id_cliente_pam):
    cliente = vet_Client.query.filter_by(id_cliente = id_cliente_pam).first()

    try:
        mydb.session.delete(cliente)
        mydb.session.commit()
        return gera_resposta (200, cliente.to_json(), 'Deletado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, 'Erro ao deletar!')


# -----------------------------------------------------------
# METODO 5 - PUT
@app.route('/cliente_put/<id_cliente_pam>', methods = ['PUT'])
def atualiza_cliente(id_cliente_pam):
    cliente = vet_Client.query.filter_by(id_cliente = id_cliente_pam).first()
    requisicao = request.get_json()

    try:
        if('nome' in requisicao):
            cliente.nome = requisicao['nome']

        if('endereco' in requisicao):
            cliente.endereco = requisicao['endereco']

        if('telefone' in requisicao):
            cliente.telefone = requisicao['telefone']

        mydb.session.add(cliente)
        mydb.session.commit()

        return gera_resposta (200, cliente.to_json(), 'Cliente atualizado com sucesso')
            
    except Exception as e:
            print('Erro', e)
            return gera_resposta(400, {}, 'Erro ao atualizar!')

app.run(port=5000, host='localhost', debug=True)