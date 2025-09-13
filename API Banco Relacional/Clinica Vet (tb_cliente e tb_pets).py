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
@app.route('/clientes_get', methods=['GET'])
def seleciona_clientes():
    cliente_selecionado = vet_Client.query.all()   # SELECT * FROM tb_clientes
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


# ---------------------------------------------------------------------------- #
# MODELO PET
# ---------------------------------------------------------------------------- #

# Classe para definir o modelo dos dados que correspondem a tabela do banco de dados
class vet_Pet(mydb.Model):
    __tablename__ = "tb_pets"
    id_pet= mydb.Column(mydb.Integer, primary_key=True)
    id_cliente = mydb.Column(mydb.Integer, mydb.ForeignKey('tb_clientes.id_cliente'), nullable=False)
    nome = mydb.Column(mydb.String(255))
    tipo = mydb.Column(mydb.String(255))
    raca = mydb.Column(mydb.String(255))
    data_nascimento = mydb.Column(mydb.String(255))
    idade = mydb.Column(mydb.String(255))

    # Método para converter o objeto em JSON
    def to_json2(self):
        return {
            'id_pet': self.id_pet,
            'id_cliente': self.id_cliente,
            'nome': self.nome,
            'tipo': self.tipo,
            'raca': self.raca,
            'data_nascimento': str(self.data_nascimento),
            'idade': self.idade,
        }

# ----------------------------------------------------------------------------------- #
# METODO 1 - GET
@app.route('/pets_get', methods=['GET'])
def seleciona_pet():
    pet_selecionado = vet_Pet.query.all()
    pet_json = [pet.to_json2() for pet in pet_selecionado]
    return gera_resposta_pets(200, pet_json)

# ----------------------------------------------------------------------------------- #
# RESPOSTA PADRAO
    # - Status (200, 201)
    # nome do conteudo
    # conteudo
    # mensagem (opcional)

def gera_resposta_pets(status, conteudo, mensagem=False):
    body = {}
    body["Lista de Pets"] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype='application/json')
        # Dumps - Converte o dicionario criado (body) em Json (json.dumps)

# ----------------------------------------------------------------------------------- #
# METODO 2 - GET (POR ID)

@app.route('/pets_get/<int:id_pet_pam>', methods=['GET'])
def seleciona_pet_id(id_pet_pam):
    pet_selecionado = vet_Pet.query.filter_by(id_pet = id_pet_pam).first()
    
    pet_json = pet_selecionado.to_json2()

    return gera_resposta(200, pet_json, 'pet encontrado !')

# ----------------------------------------------------------------------------------- #
# METODO 3 - POST

@app.route('/pets_post', methods=['POST'])
def criar_pet():
    requisicao = request.get_json()

    try:
        pet = vet_Pet(
            id_pet = requisicao['id_pet'],
            id_cliente = requisicao['id_cliente'],
            nome = requisicao['nome'],
            tipo = requisicao['tipo'],
            raca = requisicao['raca'],
            data_nascimento = requisicao['data_nascimento'],
            idade = requisicao['idade']
        )

        mydb.session.add(pet)

        # Adiciona ao banco
        mydb.session.commit()

        return gera_resposta_pets(201, pet.to_json2(), 'Criado com sucesso')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta_pets (400, {}, 'Erro ao cadastrar')

# -----------------------------------------------------------
# METODO 4 - DELETE

@app.route('/pet_delete/<int:id_pet_pam>', methods=['DELETE'])

def delete_pet(id_pet_pam):
    pet = vet_Pet.query.filter_by(id_pet = id_pet_pam).first()

    try:
        mydb.session.delete(pet)
        mydb.session.commit()
        return gera_resposta (200, pet.to_json2(), 'Deletado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, 'Erro ao deletar!')

# -----------------------------------------------------------
# METODO 5 - PUT
@app.route('/pet_put/<id_pet_pam>', methods = ['PUT'])
def atualiza_pet(id_pet_pam):
    pet = vet_Pet.query.filter_by(id_pet = id_pet_pam).first()
    requisicao = request.get_json()

    try:
        if('id_cliente' in requisicao):
            pet.id_cliente = requisicao['id_cliente']

        if('nome' in requisicao):
            pet.nome = requisicao['nome']

        if('tipo' in requisicao):
            pet.tipo = requisicao['tipo']

        if('raca' in requisicao):
            pet.raca = requisicao['raca']
        
        if('data_nascimento' in requisicao):
            pet.data_nascimento = requisicao['data_nascimento']
        
        if('idade' in requisicao):
            pet.idade = requisicao['idade']

        mydb.session.add(pet)
        mydb.session.commit()

        return gera_resposta_pets(200, pet.to_json2(), 'Pet atualizado com sucesso')
            
    except Exception as e:
            print('Erro', e)
            return gera_resposta_pets(400, {}, 'Erro ao atualizar!')



app.run(port=5000, host='localhost', debug=True)

