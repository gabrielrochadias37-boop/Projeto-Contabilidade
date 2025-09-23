from flask import Blueprint, render_template, request
from app.db import db
from app.models import Setor, Empresa, Usuario, Tarefa, RelacionamentoTarefa, Periodo

bp = Blueprint('gerenciamento', __name__, url_prefix='/gerenciamento')


@bp.get('')
@bp.get('/')
def return_page():
	setor_atual = request.args.get('setor_id', type=int)
	periodo_atual = request.args.get('periodo') or '2025-08'
	empresa_atual = request.args.get('empresa_id', type=int)

	setores = Setor.query.all()
	empresas = Empresa.query.order_by(Empresa.nome).all()

	q = db.session.query(Periodo, RelacionamentoTarefa, Tarefa, Empresa, Usuario).join(
		RelacionamentoTarefa, Periodo.relacionamento_tarefa_id == RelacionamentoTarefa.id
	).join(
		Tarefa, RelacionamentoTarefa.tarefa_id == Tarefa.id
	).join(
		Empresa, RelacionamentoTarefa.empresa_id == Empresa.id
	).outerjoin(
		Usuario, RelacionamentoTarefa.responsavel_id == Usuario.id
	).filter(Periodo.periodo_label == periodo_atual)

	if empresa_atual:
		q = q.filter(Empresa.id == empresa_atual)
	if setor_atual:
		q = q.filter(Tarefa.setor_id == setor_atual)

	resumo = {"pendentes": 0, "fazendo": 0, "concluidas": 0}
	empresas_resumo_map = {}
	responsaveis_tarefas = []

	for p, rel, tar, emp, usu in q.all():
		status = p.status or 'pendente'
		if status == 'pendente':
			resumo['pendentes'] += 1
		elif status == 'concluida':
			resumo['concluidas'] += 1
		else:
			resumo['fazendo'] += 1

		key = emp.id
		if key not in empresas_resumo_map:
			empresas_resumo_map[key] = {"nome": emp.nome, "pendentes": 0, "fazendo": 0, "concluidas": 0}
		empresas_resumo_map[key]['pendentes' if status == 'pendente' else ('concluidas' if status == 'concluida' else 'fazendo')] += 1

		responsaveis_tarefas.append({
			"usuario_nome": (usu.nome if usu else '-'),
			"empresa_nome": emp.nome,
			"tarefa_nome": tar.nome,
			"status": status,
			"periodo_label": p.periodo_label
		})

	empresas_resumo = list(empresas_resumo_map.values())

	periodos_disponiveis = [
		{"value": "2025-08", "label": "2025-08"},
		{"value": "2025-09", "label": "2025-09"},
	]

	return render_template(
		'gerenciamento.html',
		aba='gerenciamento',
		setores=setores,
		periodos_disponiveis=periodos_disponiveis,
		periodo_atual=periodo_atual,
		empresas=empresas,
		empresa_atual=empresa_atual,
		setor_atual=setor_atual,
		resumo=resumo,
		empresas_resumo=empresas_resumo,
		responsaveis_tarefas=responsaveis_tarefas,
	)



