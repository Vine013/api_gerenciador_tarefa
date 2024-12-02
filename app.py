#Biblioteca necessária
from flask import Flask, render_template, request, jsonify

#Criação de aplicação Flask
app = Flask(__name__)

#Criação de lista para armazenar tarefas - simulando database
tasks = []

#Rota principal para renderizar página inicial
@app.route('/')
def home():
    #Flask busca o arquivo HTML na pasta templates
    return render_template('index.html')

#Rota para listas as tarefas em JSON
@app.route('/tasks', methods=['GET'])
def get_tasks():
    #Retorna as tarefas em JSON
    return jsonify({"tasks": tasks}), 200

#Rota para adicionar uma nova tarefa
@app.route('/tasks', methods=['POST'])
def add_task():
    #Recebe os dados enviados pelo usuário
    data = request.get_json()
    #Valida se o titulo foi fornecido
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    #Criar nova tarefa com ID unico
    task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "status": "A fazer" #Status inicial da tarefa
    }
    tasks.append(task) #Adiciona a tarefa para a lista
    return jsonify(task), 201

#Rota para atualizar o status da tarefa
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    #Busca tarefa pelo ID
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            #Atualiza o status da tarefa
            if 'status' in data:
                task['status'] = data['status']
                return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

#Rota para deletar uma tarefa baseado no ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    #Remove a tarefa baseada no ID fornecido
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"message": f"Task {task_id} deleted"}), 200

@app.route('/tasks/clear_completed', methods=['DELETE'])
def clear_completed_tasks():
    global tasks
    # Remove todas as tarefas que possuem status "Concluído"
    tasks = [task for task in tasks if task['status'] != "Concluído"]
    return jsonify({"message": "Completed tasks cleared"}), 200


#Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
