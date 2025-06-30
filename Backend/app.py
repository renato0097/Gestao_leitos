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
import os
from dotenv import load_dotenv
app = Flask(__name__)
CORS(app)

load_dotenv()

TOKENS_POR_SETOR = {
    "UTI 1": os.getenv("TOKEN_UTI_1"),
    "UTI 2": os.getenv("TOKEN_UTI_2"),
    "UTI 3": os.getenv("TOKEN_UTI_3"),
    "UTI NEO": os.getenv("TOKEN_UTI_NEO"),
    "CENTRO CIRURGICO": os.getenv("TOKEN_CENTRO_CIRURGICO"),
    "UNIDADE INTERNACAO 4": os.getenv("TOKEN_UNIDADE_INTERNACAO_4"),
    "UNIDADE INTERNACAO 4 / CLINICA CIRURGICA": os.getenv("TOKEN_UNIDADE_INTERNACAO_4_CLINICA_CIRURGICA"),
    "UNIDADE INTERNACAO 2": os.getenv("TOKEN_UNIDADE_INTERNACAO_2"),
    "PEDIATRIA": os.getenv("TOKEN_PEDIATRIA"),
    "MATERNIDADE": os.getenv("TOKEN_MATERNIDADE"),
    "PRONTO SOCORRO": os.getenv("TOKEN_PRONTO_SOCORRO"),
}

VISUALIZACAO_TOKENS = {
    os.getenv("TOKEN_VISUALIZACAO_TI"),
    os.getenv("TOKEN_VISUALIZACAO_GL"),
    os.getenv("TOKEN_VISUALIZACAO_SHL"),
}
# ate aqui ta certo
def validar_token(token):
    for setor, t in TOKENS_POR_SETOR.items():
        if token == t:
            return setor
    return None

def require_token(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        setor = validar_token(token)
        if not setor:
            return jsonify({'error': 'Token inválido ou ausente'}), 401
        request.setor = setor
        return f(*args, **kwargs)
    return decorated

def normalize_setor(s):
    import unicodedata
    if not s:
        return ''
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8').strip().lower()

# Lista para armazenar acionamentos
acionamentos = []
registros = []

@app.route('/', methods=['POST'])
def receber_acionamento():
    data = request.get_json()
    # Padroniza o setor antes de salvar
    if 'setor' in data:
        data['setor'] = normalize_setor(data['setor'])
    acionamentos.append(data)
    print("Dados API:", data)
    return jsonify({'success': True}), 200

@app.route('/registros', methods=['POST'])
@require_token
def adicionar_registro():
    data = request.get_json()
    # Padroniza o setor antes de comparar e salvar
    setor_registro = normalize_setor(data.get('setor', ''))
    setor_token = normalize_setor(request.setor)
    if setor_registro != setor_token:
        return jsonify({'error': 'Setor do registro não corresponde ao setor do token'}), 403
    data['setor'] = setor_registro
    registros.append(data)
    print("Registro adicionado:", data)
    return jsonify({'success': True}), 200

@app.route('/registros', methods=['GET'])
@require_token
def listar_registros():
    setor = normalize_setor(request.setor)
    registros_do_setor = [r for r in registros if normalize_setor(r.get('setor')) == setor]
    return jsonify(registros_do_setor), 200

@app.route('/registros_admin', methods=['GET'])
def listar_registros_admin():
    token = request.headers.get('Authorization')
    if not token or token not in VISUALIZACAO_TOKENS:
        return jsonify({'error': 'Token de visualização inválido ou ausente'}), 401
    return jsonify(registros), 200


@app.route('/registros/<int:registro_id>', methods=['PATCH'])
@require_token
def atualizar_registro(registro_id):
    setor = request.setor
    data = request.get_json()
    for r in registros:
        if r.get('id') == registro_id and r.get('setor') == setor:
            r.update(data)
            return jsonify({'success': True}), 200
    return jsonify({'error': 'Registro não encontrado ou sem permissão'}), 404

@app.route('/registros/<int:registro_id>', methods=['DELETE'])
@require_token
def deletar_registro(registro_id):
    global registros
    setor = request.setor
    registros = [r for r in registros if not (r.get('id') == registro_id and r.get('setor') == setor)]
    return jsonify({'Registro removido com sucesso!': True}), 200

@app.route('/acionamentos/<int:acionamento_id>', methods=['DELETE'])
def deletar_acionamento(acionamento_id):
    global acionamentos
    acionamentos = [a for a in acionamentos if a.get('id') != acionamento_id]
    return jsonify({'Acionamento removido com sucesso!': True}), 200

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