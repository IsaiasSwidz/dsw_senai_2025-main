from flask import Flask, jsonify, request

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

tarefas = [
    {
        'id': 1,
        'titulo': 'Aprender a criar API com Flask',
        'concluida': True
    },
    {
        'id': 2,
        'titulo': 'Testar a API no Hoppscoth',
        'concluida': False
    }
]

# >>> Construção de Rotas <<<

# Rota para obter todas as tarefas (GET /tarefas)

@app.route('/tarefas', methods=['GET'])
def obter_tarefas():
    return jsonify(tarefas)

# Rota para obter uma tarefa específica pelo ID (GET /tarefas/<int:id> | /tarefas/2)
@app.route('/tarefas/<int:tarefa_id>', methods=['GET'])
def obter_tarefa(tarefa_id):
    tarefa = next((t for t in tarefas if t['id'] == tarefa_id), None)
    if tarefa == None:
        return jsonify({'Erro': 'Tarefa não encontrada'}), 404
    return jsonify(tarefa)

# Rota para criar uma nova tarefa (POST /tarefas)

@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    if not request.json or not 'titulo' in request.json:
        return jsonify({'Erro': 'A requisição deve ser um Json e conter um atributo chamado titulo.'}), 400
    nova_tarefa = {
        'id': tarefas[-1]['id'] + 1 if tarefas else 1,
        'titulo': request.json['titulo'],
        'concluida': False
    }
    tarefas.append(nova_tarefa)
    return jsonify(nova_tarefa), 201

# Rota para atualizar uma tarefa existente (PUT /tarefas/<int:id> | /tarefas/2)

@app.route('/tarefas/<int:tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    tarefa = next((t for t in tarefas if t['id'] == tarefa_id), None)
    if tarefa == None:
        return jsonify({'Erro': 'Tarefa não encontrada'}), 404
    if not request.json:
        return jsonify({'Erro': 'A requisição deve ser um Json.'}), 400
    tarefa['titulo'] = request.json.get('titulo', tarefa['titulo'])
    tarefa['concluida'] = request.json.get('concluida', tarefa['concluida'])
    return jsonify(tarefa)

# Rota para deletar uma tarefa (DELETE /tarefas/<int:id> | /tarefas/2)

@app.route('/tarefas/<int:tarefa_id>', methods=['DELETE'])
def deletar_tarefa(tarefa_id):
    global tarefas
    tarefa = next((t for t in tarefas if t['id'] == tarefa_id), None)
    if tarefa == None:
        return jsonify({'Erro': 'Tarefa não encontrada'}), 404
    tarefas = [t for t in tarefas if t['id'] != tarefa_id]
    return jsonify({'Resultado': 'Tarefa deletada com sucesso'})
# >>> Fim da Construção de Rotas <<<

if __name__ == '__main__':
    app.run(debug=True)
