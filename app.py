import datetime
import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importe o CORS
import json
app = Flask(__name__)
CORS(app)  # Ativar o CORS para todas as rotas
# !ricardoPW402

ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
ALLOWED_FILE_EXTENSIONS = {'.pdf', '.word', '.txt'}

UPLOAD_FOLDER_URL = "static/uploads/"
LOCATION_FOLDER_URL = "static/location/"

class User:
    def __init__(self):
        self.id = 0
        self.nome = ""
        self.morada = ""
        self.dataNascimento = ""
        self.especialidade = ""
        self.email = ""
        self.telemovel = 0
        self.listaAuditorias = []


class Material:
    def __init__(self):
        self.id = 0
        self.nome = ""
        self.tipo = ""
        self.descricao = ""
        self.quant = ""
        self.preco = ""
        self.visible = True

class Auditoria:
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
        self.date = ""
        self.visible = True


# Fazer funcao para ver o ultimo id no array
user_id = 0
material_id = 0
auditoria_id = 0
material_id = 0

userList = []
materialList = []
auditoriasList = []
auditoriaList = []

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
def get_last_auditoria_id():
    global auditoria_id
    if len(auditoriaList) > 0:
        auditoria_id = auditoriaList[-1]['id'] + 1
    else:
        auditoria_id = 0        



@app.route('/')
def home():
    return "😁"


@app.route('/user/add', methods=['POST'])
def add_user():
    global user_id
    data = request.get_json()
    user = User()
    if data == None:
        return jsonify({"error": "No data provided"}), 400

    user.id = user_id
    user.nome = data.get('nome')
    user.morada = data.get('morada')    
    user.dataNascimento = data.get('dataNascimento')
    user.especialidade = data.get('especialidade')
    user.email = data.get('email')
    user.telemovel = data.get('telemovel')
    user.listaAuditorias = data.get('listaAuditorias')

    if not isinstance(user.listaAuditorias, list):
        return jsonify({"error": "listaAuditorias must be a list"}), 400
    # if not isinstance(user.telemovel, int):
    #     return jsonify({"error": "telemovel must be an integer"}), 400

    if isinstance(user.dataNascimento, int):
        user.dataNascimento = str(user.dataNascimento)

    if isinstance(user.dataNascimento, str):
        data = ''.join(filter(str.isdigit, user.dataNascimento))  # remove barras ou outros símbolos
        if len(data) == 8:
            user.dataNascimento = f"{data[0:2]}/{data[2:4]}/{data[4:8]}"
        else:
            return jsonify({"error": "dataNascimento deve ter 8 dígitos (ddmmaaaa ou dd/mm/aaaa)"}), 400

        
    userList.append(user.__dict__)

    user_id += 1

    saveUserData()
    print(user.__dict__)
    return jsonify({"message": "User added successfully", "user": user.__dict__}), 201

@app.route('/user/get', methods=['GET'])
def get_users():
    if len(userList) == 0:
        return jsonify({"message": "No users found",'data': userList}), 200
    
    return jsonify(userList), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    global userList
    for user in userList:
        if user['id'] == user_id:
            return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/user/edit/<int:id>', methods=['PUT'])
def edit_user(id):
    global userList

    data = request.get_json()
    if data == None:
        return jsonify({"error": "No data provided"}), 400
    
    for user in userList:
        if user['listaAuditorias'] > 3:
            return jsonify({"error": "User cant be in more Auditorias","Auditorias": user['listaAuditorias']}), 401
        if user['id'] == id:
            user['listaAuditorias'] = data.get('listaAuditorias')
            saveUserData()
            return jsonify({"message": "User updated successfully", "user": user}), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/user/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    global userList
    for user in userList:
        if user['id'] == id:
            userList.remove(user)
            saveUserData()
            return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/material/add', methods=['POST'])
def add_material():
    global material_id
    data = request.get_json()
    material = Material()
    if data == None:
        return jsonify({"error": "No data provided"}), 400

    material.id = material_id
    material.nome = data.get('nome')
    material.tipo = data.get('tipo')
    material.descricao = data.get('descricao')
    material.quant = data.get('quant')
    material.preco = data.get('preco')
    material.visible = True

    materialList.append(material.__dict__)

    print(materialList)
    material_id += 1

    saveMaterialData()

    return jsonify({"message": "Material added successfully", "Material": material.__dict__}), 201

@app.route('/material/get', methods=['GET'])
def get_materials():
    global materialList
    visibleList = []
    if len(materialList) == 0:
        return jsonify({"message": "No materials found"}), 404
    else:
        for material in materialList:
            if material['visible'] == True:
                visibleList.append(material)
    return jsonify(visibleList), 200

@app.route('/material/<int:material_id>', methods=['GET'])
def get_material(material_id):
    global materialList
    for material in materialList:
        if material['id'] == material_id:
            return jsonify(material), 200
    return jsonify({"message": "Material not found"}), 404

@app.route('/material/edit/<int:id>', methods=['PUT'])
def edit_material(id):
    global materialList

    data = request.get_json()
    if data == None:
        return jsonify({"error": "No data provided"}), 400
    for material in materialList:
        if material['id'] == id:
            material['visible'] = data.get('visible')
            print(material['visible'])
            saveMaterialData()
            return jsonify({"message": "Material updated successfully", "material": material}), 200
    return jsonify({"message": "Material not found"}), 404

@app.route('/auditoria/upload', methods=['POST'])
def upload():
    global auditoriaList, auditoria_id
    json_str = request.form.get('json_data')
    if not json_str:
        return {"error": "json_data não enviado"}, 400

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "JSON inválido"}, 400

    date = datetime.datetime.now().strftime("%d-%m-%Y  %H-%M-%S")
    folder_name = f"{auditoria_id} [{date}]"
    pasta_destino = os.path.join(UPLOAD_FOLDER_URL, folder_name)
    os.makedirs(pasta_destino, exist_ok=True)  # Garante que a pasta existe

    # Aceder aos ficheiros enviados
    ficheiros = request.files
    ficheiros_guardados = []
    imagens_guardadas = []


    for nome, ficheiro in ficheiros.items():
        if not ficheiro:
            continue
        caminho = os.path.join(pasta_destino, ficheiro.filename)
        ficheiro.save(caminho)
        if is_allowed_file(ficheiro.filename):
            ficheiros_guardados.append(f"{folder_name}/{ficheiro.filename}")
        if is_allowed_image(ficheiro.filename):
            imagens_guardadas.append(f"{folder_name}/{ficheiro.filename}")

    auditoria = Auditoria()
    auditoria.id = auditoria_id
    auditoria.nome = data["nome"]
    auditoria.tipo = data["tipo"]
    auditoria.descricao = data["descricao"]
    auditoria.images = imagens_guardadas
    auditoria.files = ficheiros_guardados
    auditoria.dnome = data["dnome"]
    auditoria.dnif = data["dnif"]
    auditoria.dcontacto = data["dcontacto"]
    auditoria.demail = data["demail"]
    auditoria.location = data["location"]
    auditoria.date = str(date)
    auditoria.visible = True



    auditoriaList.append(auditoria.__dict__)
    auditoria_id += 1

    saveauditoriaData()

    return {
        "mensagem": "Recebido com sucesso!",
        "dados": auditoria.__dict__,
        "ficheiros": ficheiros_guardados,
        "imagens": imagens_guardadas,
    }, 200

@app.route('/auditoria/get', methods=['GET'])
def get_auditorias():
    global auditoriaList
    if len(auditoriaList) == 0:
        return jsonify({"message": "No auditorias found"}), 404
    
    return jsonify(auditoriaList), 200

@app.route('/auditoria/<int:auditoria_id>', methods=['GET'])
def get_auditoria(auditoria_id):
    global auditoriaList
    for auditoria in auditoriaList:
        if auditoria['id'] == auditoria_id:
            return jsonify(auditoria), 200
    return jsonify({"message": "Auditoria not found"}), 404


@app.route('/auditoria/edit/<int:id>', methods=['PUT'])
def edit_auditoria(id):
    global auditoriaList

    data = request.get_json()
    if data == None:
        return jsonify({"error": "No data provided"}), 400
    for auditoria in auditoriaList:
        if auditoria['id'] == id:
            auditoria['status'] = data.get('status')
            saveauditoriaData()
            return jsonify({"message": "Ocorrência updated successfully", "auditoria": auditoria}), 200
    return jsonify({"message": "Ocorrência not found"}), 404


#Backend PWA
@app.route('/location/send', methods=['POST'])
def send_location():
    date = datetime.datetime.now().strftime("%d-%m-%Y - %H-%M-%S")
    data = request.get_json()
    if not data:
        return "No data received", 400
    if 'location'not in data or 'auditoria_id' not in data or 'user_id' not in data:
        return "Missing Data", 400
    
    auditoria_id = data['auditoria_id']
    user_id = data['user_id']
    location = data['location']
    
    auditoria = Auditoria()
    user = User()

    auditoria = next((a for a in auditoriaList if a['id'] == auditoria_id), None)
    user = next((u for u in userList if u['id'] == user_id), None)

    info = {
        "auditoria_id": auditoria_id,
        "auditoria": auditoria['nome'],
        "user_id": user_id,
        "user": user['nome'],
        "location": location,
    }

    folder_name = f"{auditoria['nome']}"
    pasta_destino = os.path.join(LOCATION_FOLDER_URL, folder_name)
    os.makedirs(pasta_destino, exist_ok=True)
    caminho = os.path.join(pasta_destino, f"{user_id}.json")
    with open(caminho, "w", encoding="utf-8") as file:
        json.dump(info, file, indent=4,ensure_ascii=False)
    
    return jsonify({"message": "Location sent successfully", "info": info}), 200

@app.route('/auditoria/users', methods=['GET'])
def get_users_auditoria():
    global userList
    auditoria_id = request.args.get('auditoria_id')
    if not auditoria_id:
        return jsonify({"error": "No auditoria_id provided"}), 400

    if len(userList) == 0:
        return jsonify({"message": "No users found"}), 404
    users = []
    for user in userList:
        for auditoria in user['listaAuditorias']:
            if auditoria == int(auditoria_id):
                users.append(user)
                break
    return jsonify(users), 200

#File Management
#Load Data
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
def loadauditoriaData():
    global auditoriaList
    try:
        with open("auditorias.json", "r", encoding="utf-8") as file:
            auditoriaList = json.load(file)
    except FileNotFoundError:
        auditoriaList = []
    except json.JSONDecodeError:
        auditoriaList = []
#Save Data
def saveUserData():
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(userList, file, indent=4)

    return jsonify({"message": "Data saved successfully"}), 200

def saveMaterialData():
    with open("materials.json", "w", encoding="utf-8") as file:
        json.dump(materialList, file, indent=4)

    return jsonify({"message": "Data saved successfully"}), 200

def saveauditoriaData():
    with open("auditorias.json", "w", encoding="utf-8") as file:
        json.dump(auditoriaList, file, indent=4)

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
    loadauditoriaData()
    app.run(debug=True)