from fastapi import FastAPI, HTTPException
from typing import List
from Usuario import Usuario, UsuarioCreate
from fastapi.middleware.cors import CORSMiddleware
import oracledb
import os
from dotenv import load_dotenv


# Carrega as variáveis do .env
load_dotenv()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode colocar domínios específicos aqui no futuro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SID = os.getenv("DB_SID")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


proximo_id: int = 0  # contador de ID automático

@app.get("/ola")
def katia():
    return({
        "mensagem": "alguma coisa"
    })

# Rota para criar uma nova tarefa (ID gerado automaticamente no backend Python)
@app.post("/usuario", response_model=Usuario)
def criar_usuario(usuario: UsuarioCreate):
    global proximo_id
    proximo_id += 1
    nova_usuario = Usuario(id_usuario=proximo_id, **usuario.dict())


    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()


    cursor.execute("INSERT INTO T_UFS_USUARIO (ID_USUARIO, NOME, SENHA, ULTIMO_LOGIN, CARGO) VALUES (:valor1, :valor2, :valor3, :valor4, :valor5)", valor1=nova_usuario.id_usuario, valor2=nova_usuario.nome, valor3=nova_usuario.senha, valor4=nova_usuario.ultimo_login, valor5=nova_usuario.cargo)
    conn.commit()


    cursor.close()
    conn.close()


    return nova_usuario    
   


# Rota para listar todas as tarefas
@app.get("/usuario", response_model=List[Usuario])
def listar_usuario():


    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()


    cursor.execute('SELECT * FROM T_UFS_USUARIO')


    rows = cursor.fetchall()


    cursor.close()
    conn.close()

    return[
        {
            "id_usuario": row[0],
            "nome": row[1],
            "senha": row[2],
            "ultimo_login": row[3],
            "cargo":row[4]
        }
        for row in rows
    ]



# Rota para obter uma tarefa específica
@app.get("/usuario/{usuario_id_usuario}", response_model=Usuario)
def obter_usuario(usuario_id_usuario: int):
    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()


    cursor.execute('SELECT * FROM T_UFS_USUARIO WHERE ID_USUARIO = :valor1', valor1=usuario_id_usuario)

    row = cursor.fetchone()
   
    if row:
        return {
            "id_usuario": row[0],
            "nome": row[1],
            "senha": row[2],
            "ultimo_login": row[3],
            "cargo":row[4]
        }
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")

# Rota para atualizar uma tarefa completa
@app.put("/usuario/{usuario_id_usuario}")
def atualizar_manutencao(usuario_id_usuario: int, nova_usuario: UsuarioCreate):
    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()

    cursor.execute("UPDATE T_UFS_USUARIO SET NOME=:valor2, SENHA=:valor3, ULTIMO_LOGIN=valor4, CARGO=:valor5 WHERE: ID_USUARIO=:valor1",valor1=usuario_id_usuario, valor2=nova_usuario.nome, valor3=nova_usuario.senha, valor4=nova_usuario.ultimo_login, valor5=nova_usuario.cargo)
    conn.commit()


    cursor.close()
    conn.close()


    return {"mensagem": "Usuario atualizado com sucesso!"}


# Rota para excluir uma tarefa
@app.delete("/usuario/{usuario_id_usuario}")
def deletar_Manutencao(usuario_id_usuario: int):
    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()


    cursor.execute("DELETE FROM T_UFS_USUARIO WHERE ID_USUARIO=:valor1", valor1=usuario_id_usuario)
    conn.commit()


    cursor.close()
    conn.close()


    return {"mensagem": "Usuario excluído com sucesso"}
