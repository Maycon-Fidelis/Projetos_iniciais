# resources/hotel.py
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
from flask_jwt_extended import jwt_required
from models.site import SiteModel
import sqlite3

# define os parâmetros esperados via query string
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str, location='args')
path_params.add_argument('estrelas_min', type=float, location='args')
path_params.add_argument('estrelas_max', type=float, location='args')
path_params.add_argument('diaria_min', type=float, location='args')
path_params.add_argument('diaria_max', type=float, location='args')
path_params.add_argument('limit', type=int, location='args')
path_params.add_argument('offset', type=int, location='args')

class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('instance/banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}

        # Se nenhum parâmetro for passado, retorna todos os hotéis
        if not dados_validos:
            resultado = cursor.execute("SELECT * FROM hoteis")
        else:
            parametros = normalize_path_params(**dados_validos)
            if not parametros.get('cidade'):
                consulta = consulta_sem_cidade
                tupla = (
                    parametros['estrelas_min'],
                    parametros['estrelas_max'],
                    parametros['diaria_min'],
                    parametros['diaria_max'],
                    parametros['limit'],
                    parametros['offset']
                )
            else:
                consulta = consulta_com_cidade
                tupla = (
                    parametros['estrelas_min'],
                    parametros['estrelas_max'],
                    parametros['diaria_min'],
                    parametros['diaria_max'],
                    parametros['cidade'],
                    parametros['limit'],
                    parametros['offset']
                )

            resultado = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
            })

        connection.close()
        return {'hoteis': hoteis}, 200


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria', type=float, required=True, help="The field 'diaria' cannot be left blank")
    argumentos.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be left blank")
    argumentos.add_argument('site_id', type=int, required=True, help='Every hotel need to be linked with site')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel não encontrado'}, 404

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel com id {hotel_id} já existe.'}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'The Hotel must be associated to a valid site id.'}, 400

        try:
            hotel.save_hotel()
        except:
            return {'message': 'Erro interno ao salvar o hotel.'}, 500
        return hotel.json(), 201

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Erro interno ao salvar o hotel.'}, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'Erro interno ao deletar o hotel.'}, 500
            return {'message': 'Hotel deletado com sucesso'}
        return {'message': 'Hotel não encontrado'}, 404
