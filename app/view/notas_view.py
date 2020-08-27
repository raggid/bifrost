from flask_restplus import Resource, fields

from app.container import Container
from app.flask_app import api

ns = api.namespace('notas', description='Operações com notas')
notas_service = Container.notas_service()

nota = api.model('Nota', {
    'filial': fields.Integer(required=True),
    'serie': fields.String(required=True),
    'nota': fields.Integer(required=True)
})


@ns.route('/')
class Notas(Resource):
    @ns.expect(nota)
    @ns.doc('get_nota')
    def post(self):
        return notas_service.get_by_nota(nota['filial'], nota['serie'], nota['nota'])
