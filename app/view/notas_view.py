from app.flask_app import api
from flask_restplus import Resource, reqparse
from flask import jsonify, request

from app.service.notas_service import NotasService


nota_parser = reqparse.RequestParser()
nota_parser.add_argument('filial', type=int, help='Numero da Filial', required=True)
nota_parser.add_argument('serie', type=str, help='Serie', required=True)
nota_parser.add_argument('nota', type=int, help='Numero da Nota', required=True)
@api.route('/nota')
@api.expect(nota_parser)
class Nota(Resource):
    service = NotasService()

    def post(self):
        filial = request.args['filial']
        serie = request.args['serie']
        nota = request.args['nota']
        return jsonify(self.service.get_by_nota(filial,serie,nota))
