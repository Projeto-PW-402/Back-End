import datetime
import os
from flask import Flask, request, jsonify
import json
app = Flask(__name__)
# !ricardoPW402

ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
ALLOWED_FILE_EXTENSIONS = {'.pdf', '.word', '.txt'}

class User:
    def __init__(self):
        self.id = 0
        self.nome = ""
        self.morada = ""
        self.dataNascimento = ""
        self.especialidade = ""
        self.email = ""
        self.telemovel = 0
        self.listaAuditorias = ""


class Material:
    def __init__(self):
        self.id = 0
        self.nome = ""
        self.tipo = ""
        self.descricao = ""
        self.quant = ""
        self.preco = ""

class Ocorrencia:
    def __init__(self):
        self.id = 0
        self.nome = ""
        self.tipo = ""
        self.descricao = ""
        self.images = []
        self.files = []
        self.dnome = ""
        self.dnif = ""
        self.dcontacto = ""
        self.demail = ""
        self.location = ""
        self.status = -1


# Fazer funcao para ver o ultimo id no array
user_id = 0
material_id = 0
ocorrencia_id = 0

userList = []
materialList = []
auditoriasList = []
ocorrenciaList = []

def get_last_user_id():
    global user_id
    if len(userList) > 0:
        user_id = userList[-1]['id'] + 1
    else:
        user_id = 0
def get_last_material_id():
    global material_id
    if len(materialList) > 0:
        material_id = materialList[-1]['id'] + 1
    else:
        material_id = 0
def get_last_ocorrencia_id():
    global ocorrencia_id
    if len(ocorrenciaList) > 0:
        ocorrencia_id = ocorrenciaList[-1]['id'] + 1
    else:
        ocorrencia_id = 0        



@app.route('/')
def home():
    return "😁"


@app.route('/addUser', methods=['POST'])
def add_user():
    global user_id
    data = request.get_json()
    user = User()
    if data == None:
        return jsonify({"error": "No data provided"}), 400

    user.id = user_id
    user.nome = data.get('name')
    user.morada = data.get('morada')    
    user.dataNascimento = data.get('dataNascimento')
    user.especialidade = data.get('especialidade')
    user.email = data.get('email')
    user.telemovel = data.get('telemovel')
    user.listaAuditorias = data.get('listaAuditorias')

    userList.append(user.__dict__)

    user_id += 1

    saveUserData()

    return jsonify({"message": "User added successfully", "user": user.__dict__}), 201

@app.route('/getUsers', methods=['GET'])
def get_users():
    if len(userList) == 0:
        return jsonify({"message": "No users found"}), 404
    
    return jsonify(userList), 200

@app.route('/getUser/<int:user_id>', methods=['GET'])
def get_user(user_id):
    global userList
    for user in userList:
        if user['id'] == user_id:
            return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/addMaterial', methods=['POST'])
def add_material():
    global material_id
    data = request.get_json()
    material = Material()
    if data == None:
        return jsonify({"error": "No data provided"}), 400

    material.id = material_id
    material.nome = data.get('name')
    material.tipo = data.get('tipo')
    material.descricao = data.get('descricao')
    material.quant = data.get('quant')
    material.preco = data.get('preco')

    materialList.append(material.__dict__)

    material_id += 1

    saveMaterialData()

    return jsonify({"message": "Material added successfully", "user": material.__dict__}), 201

@app.route('/getMaterials', methods=['GET'])
def get_materials():
    if len(materialList) == 0:
        return jsonify({"message": "No materials found"}), 404
    
    return jsonify(materialList), 200

@app.route('/getMaterial/<int:material_id>', methods=['GET'])
def get_material(material_id):
    global materialList
    for material in materialList:
        if material['id'] == material_id:
            return jsonify(material), 200
    return jsonify({"message": "Material not found"}), 404

@app.route('/upload', methods=['POST'])
def upload():
    global ocorrenciaList, ocorrencia_id
    json_str = request.form.get('json_data')
    if not json_str:
        return {"error": "json_data não enviado"}, 400

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "JSON inválido"}, 400

    date = datetime.datetime.now().strftime("%d-%m-%Y  %H-%M-%S")
    folder_name = f"{ocorrencia_id} [{date}]"
    pasta_destino = os.path.join("uploads", folder_name)
    os.makedirs(pasta_destino, exist_ok=True)  # Garante que a pasta existe

    # Aceder aos ficheiros enviados
    ficheiros = request.files
    ficheiros_guardados = []
    imagens_guardadas = []


    for nome, ficheiro in ficheiros.items():
        caminho = os.path.join(pasta_destino, ficheiro.filename)
        ficheiro.save(caminho)
        if is_allowed_file(ficheiro.filename):
            ficheiros_guardados.append(f"{folder_name}/{ficheiro.filename}")
        if is_allowed_image(ficheiro.filename):
            imagens_guardadas.append(f"{folder_name}/{ficheiro.filename}")

    ocorrencia = Ocorrencia()
    ocorrencia.id = ocorrencia_id
    ocorrencia.nome = data["nome"]
    ocorrencia.tipo = data["tipo"]
    ocorrencia.descricao = data["descricao"]
    ocorrencia.images = imagens_guardadas
    ocorrencia.files = ficheiros_guardados
    ocorrencia.dnome = data["dnome"]
    ocorrencia.dnif = data["dnif"]
    ocorrencia.dcontacto = data["dcontacto"]
    ocorrencia.demail = data["demail"]
    ocorrencia.location = data["location"]


    ocorrenciaList.append(ocorrencia.__dict__)
    ocorrencia_id += 1

    return {
        "mensagem": "Recebido com sucesso!",
        "dados": data,
        "ficheiros": ficheiros_guardados,
        "imagens": imagens_guardadas,
    }, 200


def loadUserData():
    global userList
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            userList = json.load(file)
    except FileNotFoundError:
        userList = []
    except json.JSONDecodeError:
        userList = []
def loadMaterialData():
    global materialList
    try:
        with open("materials.json", "r", encoding="utf-8") as file:
            materialList = json.load(file)
    except FileNotFoundError:
        materialList = []
    except json.JSONDecodeError:
        materialList = []
def loadOcorrenciaData():
    global materialList
    try:
        with open("materials.json", "r", encoding="utf-8") as file:
            materialList = json.load(file)
    except FileNotFoundError:
        materialList = []
    except json.JSONDecodeError:
        materialList = []

def saveUserData():
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(userList, file, indent=4)

    return jsonify({"message": "Data saved successfully"}), 200

def saveMaterialData():
    with open("materials.json", "w", encoding="utf-8") as file:
        json.dump(userList, file, indent=4)

    return jsonify({"message": "Data saved successfully"}), 200

def saveOcorrenciaData():
    with open("ocorrencias.json", "w", encoding="utf-8") as file:
        json.dump(userList, file, indent=4)

    return jsonify({"message": "Data saved successfully"}), 200

def is_allowed_file(file):
    ext = os.path.splitext(file)[1].lower()
    return ext in ALLOWED_FILE_EXTENSIONS
def is_allowed_image(file):
    ext = os.path.splitext(file)[1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS

if __name__ == '__main__':
    loadUserData()
    loadMaterialData()
    app.run(debug=True)