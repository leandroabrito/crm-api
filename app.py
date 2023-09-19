from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Cliente
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API CRM Mini", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação Swagger", description="Documentação estilo Swagger.")
cliente_tag = Tag(name="Cliente", description="Adição, visualização e remoção de clientes na base de dados")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para documentação da API no estilo Swagger.
    """
    return redirect('/openapi/swagger')


@app.post('/cadastrar_cliente', tags=[cliente_tag],
    responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """Adiciona um novo cliente à base de dados

    Retorna uma representação dos clientes e comentários associados.
    """

    cliente = Cliente(
        nome=form.nome,
        email=form.email,
        celular=form.celular,
        cidade=form.cidade
    )
    
    logger.warning(f"Adicionando cliente de nome: '{cliente.nome}'")
    try:        
        session = Session()        
        session.add(cliente)                
        session.commit()
        logger.debug(f"Adicionado cliente de nome: '{cliente.nome}'")
        return apresenta_cliente(cliente), 200    

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/clientes', tags=[cliente_tag],
    responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def get_clientes():
    """Faz a busca por todos os clientes cadastrados

    Retorna uma representação da listagem de clientes.
    """
    logger.debug(f"Coletando clientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Cliente).all()        

    if not clientes:
        # se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.debug(f"%d clientes encontrados" % len(clientes))
        # retorna a representação de cliente
        print(clientes)
        return apresenta_clientes(clientes), 200

@app.delete('/deletar_cliente', tags=[cliente_tag],
    responses={"200": ClienteDelSchema, "404": ErrorSchema})
def del_cliente(query: ClienteBuscaSchema):
    """Deleta um cliente a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_nome = unquote(unquote(query.nome))
    print(cliente_nome)
    logger.debug(f"Deletando dados sobre cliente #{cliente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.nome == cliente_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando cliente #{cliente_nome}")
        return {"message": "Cliente removido", "nome": cliente_nome}
    else:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente #'{cliente_nome}', {error_msg}")
        return {"message": error_msg}, 404


# @app.get('/buscar_cliente_por_nome', tags=[cliente_tag],
#          responses={"200": ClienteViewSchema, "404": ErrorSchema})
# def get_cliente(query: ClienteBuscaSchema):
#     """Faz a busca por um cliente a partir do nome do cliente

#     Retorna uma representação dos clientes e comentários associados.
#     """
#     cliente_nome = query.nome
#     logger.debug(f"Coletando dados sobre cliente #{cliente_nome}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     cliente = session.query(Cliente).filter(Cliente.nome == cliente_nome).first()

#     if not cliente:
#         # se o cliente não foi encontrado
#         error_msg = "Cliente não encontrado na base :/"
#         logger.warning(f"Erro ao buscar cliente '{cliente_nome}', {error_msg}")
#         return {"message": error_msg}, 404
#     else:
#         logger.debug(f"Cliente econtrado: '{cliente.nome}'")
#         # retorna a representação de cliente 
#         return apresenta_cliente(cliente), 200