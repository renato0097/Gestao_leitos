# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # @app.route('/')
# # def index():
# #     return "valeu"

# @app.route('/', methods=['POST'])
# def receber_acionamento():
#     data = request.get_json()
#     # processar e salvar...
#     print("Dados API:", data)
#     return jsonify({'success': True}), 200


# # @app.route('/processar', methods=['POST'])




# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=10000, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lista para armazenar acionamentos
acionamentos = []
registros = []
@app.route('/', methods=['POST'])
def receber_acionamento():
    data = request.get_json()
    acionamentos.append(data)
    print("Dados API:", data)
    return jsonify({'success': True}), 200

# @app.route('/registros', methods=['GET'])
# def listar_acionamentos():
#     # Retorna todos os acionamentos (ou filtre por status se quiser)
#     return jsonify(acionamentos), 200

@app.route('/registros', methods=['POST'])
def adicionar_registro():
    data = request.get_json()
    registros.append(data)
    print("Registro adicionado:", data)
    return jsonify({'success': True}), 200

@app.route('/registros', methods=['GET'])
def listar_registros():
    return jsonify(registros), 200



# @app.route('/registros/<int:registro_id>', methods=['PATCH'])
# def atualizar_status(registro_id):
#     data = request.get_json()
#     for a in acionamentos:
#         if a.get('id') == registro_id:
#             a['status'] = data.get('status', a['status'])
#             return jsonify({'success': True}), 200
#     return jsonify({'error': 'Registro não encontrado'}), 404
@app.route('/registros/<int:registro_id>', methods=['PATCH'])
def atualizar_registro(registro_id):
    data = request.get_json()
    for r in registros:
        if r.get('id') == registro_id:
            r.update(data)
            return jsonify({'success': True}), 200
    return jsonify({'error': 'Registro não encontrado'}), 404

@app.route('/registros/<int:registro_id>', methods=['DELETE'])
def deletar_registro(registro_id):
    global registros
    registros = [r for r in registros if ["id"] != registro_id]
    return jsonify({'success': True}), 200

# @app.route('/acionamentos/<int:acionamento_id>', methods=['DELETE'])
# def deletar_acionamento(acionamento_id):
#     global acionamentos
#     acionamentos = [a for a in acionamentos if a.get('id') != acionamento_id]
#     return jsonify({'success': True}), 200


@app.route('/acionamentos/<int:acionamento_id>', methods=['PATCH'])
def atualizar_acionamento(acionamento_id):
    data = request.get_json()
    for a in acionamentos:
        if a.get('id') == acionamento_id:
            a.update(data)
            return jsonify({'success': True}), 200
    return jsonify({'error': 'Acionamento não encontrado'}), 404


@app.route('/acionamentos', methods=['GET'])
def listar_acionamentos():
    return jsonify(acionamentos), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)