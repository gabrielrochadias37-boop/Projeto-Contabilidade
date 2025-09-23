from flask import Blueprint, render_template
from app.models import Empresa

bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')


@bp.get('')
@bp.get('/')
def return_page():
	empresas_opts = [{"id": e.id, "nome": e.nome} for e in Empresa.query.order_by(Empresa.nome).all()]
	return render_template('relatorios.html', aba='relatorios', empresas=empresas_opts)
