from flask import Flask, request, jsonify
import json
app = Flask(__name__)

class User:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.morada = ""
        self.dataNascimento = ""
        self.especialidade = ""
        self.email = ""
        self.telemovel = 0
        self.listaAuditorias = ""


id = 0

userList = []
materialList = []
auditoriasList = []

@app.route('/')
def home():
    return "😁"


@app.route('/addUser', methods=['POST'])
def add_user():
    global id
    data = request.get_json()
    user = User()
    if data == None:
        return jsonify({"error": "No data provided"}), 400

    user.id = id
    user.name = data.get('name')
    user.morada = data.get('morada')    
    user.dataNascimento = data.get('dataNascimento')
    user.especialidade = data.get('especialidade')
    user.email = data.get('email')
    user.telemovel = data.get('telemovel')
    user.listaAuditorias = data.get('listaAuditorias')

    userList.append(user.__dict__)

    id += 1

    # Salva os dados no ficheiro JSON
    saveData()

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

def loadData():
    global userList
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            userList = json.load(file)
    except FileNotFoundError:
        userList = []
    except json.JSONDecodeError:
        userList = []

def saveData():
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(userList, file, indent=4)

    return jsonify({"message": "Data saved successfully"}), 200


if __name__ == '__main__':
    loadData()
    app.run(debug=True)