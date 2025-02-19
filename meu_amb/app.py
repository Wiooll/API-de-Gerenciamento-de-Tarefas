from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do banco de dados
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    concluida = db.Column(db.Boolean, default=False)

# Criar o banco de dados
with app.app_context():
    db.create_all()

# Rota para criar uma nova tarefa (POST)
@app.route('/instance/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.get_json()
    nova_tarefa = Tarefa(titulo=dados['titulo'], descricao=dados.get('descricao', ''), concluida=False)
    db.session.add(nova_tarefa)
    db.session.commit()
    return jsonify({'mensagem': 'Tarefa criada com sucesso!'}), 201

# Rota para listar todas as tarefas (GET)
@app.route('/instance/tarefas', methods=['GET'])
def listar_tarefas():
    tarefas = Tarefa.query.all()
    return jsonify([{'id': t.id, 'titulo': t.titulo, 'descricao': t.descricao, 'concluida': t.concluida} for t in tarefas])

# Rota para atualizar uma tarefa (PUT)
@app.route('/instance/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    dados = request.get_json()
    tarefa.titulo = dados.get('titulo', tarefa.titulo)
    tarefa.descricao = dados.get('descricao', tarefa.descricao)
    tarefa.concluida = dados.get('concluida', tarefa.concluida)
    db.session.commit()
    return jsonify({'mensagem': 'Tarefa atualizada com sucesso!'})

# Rota para deletar uma tarefa (DELETE)
@app.route('/instance/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({'mensagem': 'Tarefa deletada com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
    
