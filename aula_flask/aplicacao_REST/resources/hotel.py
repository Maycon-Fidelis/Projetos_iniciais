from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
    'hotel_id': 'alpha',
    'nome': 'Alpha hotel',
    'estrelas': 4.3,
    'diaria': 420.34,
    'cidade': 'Rio de Janeiro'
    },    
    {
    'hotel_id': 'bravo',
    'nome': 'Alpha bravo',
    'estrelas': 4.3,
    'diaria': 380.90,
    'cidade': 'Santa Catarina'
    },
    {
    'hotel_id': 'charlie',
    'nome': 'Charlie hotel',
    'estrelas': 3.9,
    'diaria': 320.20,
    'cidade': 'Santa Catarina'
    }
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis' : [hotel.json() for hotel in HotelModel.query.all()]}
    
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float,required=True,help="The field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    # def find_hotel(hotel_id):
    #     for hotel in hoteis:
    #         if hotel['hotel_id'] == hotel_id:
    #             return hotel
    #     return None

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel não encontrado'}, 404

    def post(self,hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel com id {hotel_id} já existe.'}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json()

    def put(self,hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id,**dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json(), 201

    def delete(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel.'}, 500
            return {'message': 'Hotel deletado com sucesso'}
        return {'message': 'Hotel não encontrado'}, 404