# pip install flask_sqlalchemy
# Permite a conexao da API com o banco de dados
# Flask - permite a criação de API com Python
# Response e Request -> Requisição

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask("carros")

# Rastrear as modificacoes realizadas
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Configuração de conexão com o banco
# %40 -> faz o papel do @
# 1- Usuario (root) 2- Senha (senai%40134) 3- localhost (127.0.0.1) 
 
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:senai%40134@127.0.0.1/db_carro"

mydb = SQLAlchemy(app)

# Classe para definir o modelo dos dados que correspondem a tabela do banco de dados
class Carros(mydb.Model):
    __tablename__ = "tb_carro"
    id_carro = mydb.Column(mydb.Integer, primary_key = True)
    marca = mydb.Column(mydb.String(255))
    modelo = mydb.Column(mydb.String(255))
    ano = mydb.Column(mydb.String(255))
    cor = mydb.Column(mydb.String(255))
    valor = mydb.Column(mydb.String(255))
    numero_Vendas = mydb.Column(mydb.String(255))

# Esse metodo to_json vai ser usado para converter o objeto em json
    def to_json(self):
        return {
            'id_carro': self.id_carro,
            'marca': self.marca,
            'modelo': self.modelo,
            'ano': self.ano,
            'cor': self.cor,
            'valor': float(self.valor),
            'numero_Vendas': self.numero_Vendas
        }

# ----------------------------------------------------------------------------------- #

# METODO 1 - GET
@app.route('/carros', methods = ['GET'])

def seleciona_carro():
    carro_selecionado  = Carros.query.all()
    # Executa uma consulta no banco de dados (SELECT * FROM tb_carros)

    carro_json = [ carro.to_json()
                  for carro in carro_selecionado]

    return gera_resposta (200, "Lista de Carros", carro_json)

# ----------------------------------------------------------------------------------- #
# RESPOSTA PADRAO
    # - Status (200, 201)
    # nome do conteudo
    # conteudo
    # mensagem (opcional)

def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body["Lista de Carro"] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype='application/json')
        # Dumps - Converte o dicionario criado (body) em Json (json.dumps)


# ----------------------------------------------------------------------------------- #
# METODO 2 - GET (POR ID)

@app.route('/carros/<int:id_carro_pam>', methods=['GET'])
def seleciona_carro_id(id_carro_pam):
    carro_selecionado = Carros.query.filter_by(id_carro = id_carro_pam).first()
    # SELECT * FROM  tb_carros WHERE id_carro = 5
    carro_json = carro_selecionado.to_json()

    return gera_resposta(200, carro_json, 'carro encontrado !')

# ----------------------------------------------------------------------------------- #
# METODO 3 - POST

@app.route('/carros', methods=['POST'])
def criar_carro():
    requisicao = request.get_json()

    try:
        carro = Carros (
            id_carro = requisicao['id_carro'],
            marca = requisicao['marca'],
            modelo = requisicao['modelo'],
            ano = requisicao['ano'],
            valor = requisicao['valor'],
            cor = requisicao['cor'],
            numero_Vendas = requisicao['numero_Vendas']
        )

        mydb.session.add(carro)

        # Adiciona ao banco
        mydb.session.commit()

        return gera_resposta(201, carro.to_json(), 'Criado com sucesso')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta (400, {}, 'Erro ao cadastrar')



# -----------------------------------------------------------
# METODO 4 - DELETE

@app.route('/carros/<int:id_carro_pam>', methods=['DELETE'])

def delete_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro = id_carro_pam).first()

    try:
        mydb.session.delete(carro)
        mydb.session.commit()
        return gera_resposta (200, carro.to_json(), 'Deletado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, 'Erro ao deletar!')


# -----------------------------------------------------------
# METODO 5 - PUT
@app.route('/carros/<id_carro_pam>', methods = ['PUT'])
def atualiza_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro = id_carro_pam).first()
    requisicao = request.get_json()

    try:
        if('marca' in requisicao):
            carro.marca = requisicao['marca']

        if('modelo' in requisicao):
            carro.modelo = requisicao['modelo']

        if('ano' in requisicao):
            carro.ano = requisicao['ano']
        
        if('valor' in requisicao):
            carro.valor = requisicao['valor']

        if('cor' in requisicao):
            carro.cor = requisicao['cor']

        if('numero_Vendas' in requisicao):
            carro.numero_Vendas = requisicao['numero_Vendas']

        mydb.session.add(carro)
        mydb.session.commit()

        return gera_resposta (200, carro.to_json(), 'Carro atualizado com sucesso')
            
    except Exception as e:
            print('Erro', e)
            return gera_resposta(400, {}, 'Erro ao atualizar!')

app.run(port=5000, host='localhost', debug=True)