from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.usuario import UsuarioModel
import hmac  # ✅ substitui o werkzeug
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='The field login cannot be blank')
atributos.add_argument('senha', type=str, required=True, help='The field senha cannot be blank')

class Usuario(Resource):
    def get(self, user_id):
        usuario = UsuarioModel.find_user(user_id)
        if usuario:
            return usuario.json()
        return {'message': 'Usuário não encontrado'}, 404
    
    @jwt_required()
    def delete(self, user_id):
        usuario = UsuarioModel.find_user(user_id)
        if usuario:
            try:
                usuario.delete_user()
            except:
                return {'message': 'An internal error occurred trying to delete user.'}, 500
            return {'message': 'Usuário deletado com sucesso'}
        return {'message': 'Usuário não encontrado'}, 404 

class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UsuarioModel.find_by_login(dados['login']):
            return {"mensagem": f"The login '{dados['login']}' already exists."}
        
        user = UsuarioModel(**dados)
        user.save_user()
        return {'mensagem': 'User created successfully!'}, 201

class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UsuarioModel.find_by_login(dados['login'])

        if user and hmac.compare_digest(user.senha, dados['senha']):  # ✅ substituição
            token_de_acesso = create_access_token(identity=str(user.user_id))
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'logged out successfully!'}, 200