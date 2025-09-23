from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import db
from app.models import Empresa, RelacionamentoTarefa, Periodo, Tarefa, Usuario

bp = Blueprint('dashboard', __name__, url_prefix='')


def _build_periodos(empresa_id, periodo_label, user_id, tarefa_id):
	query = db.session.query(Periodo, RelacionamentoTarefa, Tarefa, Empresa).join(
		RelacionamentoTarefa, Periodo.relacionamento_tarefa_id == RelacionamentoTarefa.id
	).join(
		Tarefa, RelacionamentoTarefa.tarefa_id == Tarefa.id
	).join(
		Empresa, RelacionamentoTarefa.empresa_id == Empresa.id
	)
	if periodo_label:
		query = query.filter(Periodo.periodo_label == periodo_label)
	if empresa_id:
		query = query.filter(RelacionamentoTarefa.empresa_id == empresa_id)
	if user_id:
		query = query.filter(RelacionamentoTarefa.responsavel_id == user_id)
	if tarefa_id:
		query = query.filter(RelacionamentoTarefa.tarefa_id == tarefa_id)
	itens = []
	for p, rel, tar, emp in query.all():
		itens.append({
			"periodo_id": p.id,
			"nome": tar.nome,
			"tipo": tar.tipo,
			"status": p.status or 'pendente',
			"vencimento": p.fim.isoformat() if p.fim else None,
			"empresa_ativa": bool(getattr(emp, 'ativo', True)),
			"empresa_nome": emp.nome
		})
	return itens


@bp.get('/')
@bp.get('/dashboard')
def return_dashboard():
	periodo_atual = request.args.get('periodo') or '2025-08'
	empresa_id = request.args.get('empresa_id', type=int)
	tarefa_id = request.args.get('tarefa_id', type=int)
	user_id = session.get('user_id')

	empresas_usuario = db.session.query(Empresa).order_by(Empresa.nome).all()

	# tarefas vinculadas ao usuário (para popular o filtro)
	tarefas_usuario = db.session.query(Tarefa).join(
		RelacionamentoTarefa, RelacionamentoTarefa.tarefa_id == Tarefa.id
	).filter(RelacionamentoTarefa.responsavel_id == user_id)
	if empresa_id:
		tarefas_usuario = tarefas_usuario.filter(RelacionamentoTarefa.empresa_id == empresa_id)
	tarefas_usuario = tarefas_usuario.distinct().order_by(Tarefa.nome).all()

	tarefas = _build_periodos(empresa_id, periodo_atual, user_id, tarefa_id)
	resumo = {"pendentes": 0, "fazendo": 0, "concluidas": 0}
	for t in tarefas:
		if t['status'] == 'pendente':
			resumo['pendentes'] += 1
		elif t['status'] == 'concluida':
			resumo['concluidas'] += 1
		else:
			resumo['fazendo'] += 1

	periodos_disponiveis = [
		{"value": "2025-08", "label": "2025-08"},
		{"value": "2025-09", "label": "2025-09"},
	]

	return render_template(
		'dashboard.html',
		aba='dashboard',
		periodos_disponiveis=periodos_disponiveis,
		periodo_atual=periodo_atual,
		empresas_usuario=empresas_usuario,
		empresa_atual=empresa_id,
		tarefas=tarefas,
		tarefas_usuario=tarefas_usuario,
		tarefa_atual=tarefa_id,
		resumo=resumo,
	)


@bp.post('/dashboard/concluir')
def concluir_tarefa():
	periodo_id = request.form.get('periodo_id', type=int)
	p = db.session.get(Periodo, periodo_id)
	if not p:
		return redirect(url_for('dashboard.return_dashboard'))

	rel = db.session.get(RelacionamentoTarefa, p.relacionamento_tarefa_id)
	emp = db.session.get(Empresa, rel.empresa_id) if rel else None
	user = db.session.get(Usuario, session.get('user_id')) if session.get('user_id') else None
	if (emp and getattr(emp, 'ativo', True) is False) or (user and getattr(user, 'ativo', True) is False):
		flash('Ação não permitida: usuário ou empresa inativos')
		return redirect(url_for('dashboard.return_dashboard'))
	# garante que só o responsável conclua
	if rel and user and rel.responsavel_id != user.id:
		flash('Ação não permitida para este usuário')
		return redirect(url_for('dashboard.return_dashboard'))

	p.status = 'concluida'
	db.session.commit()
	flash('Tarefa concluída com sucesso!')
	return redirect(url_for('dashboard.return_dashboard'))


@bp.post('/dashboard/retificar')
def retificar_tarefa():
	periodo_id = request.form.get('periodo_id', type=int)
	p = db.session.get(Periodo, periodo_id)
	if not p:
		return redirect(url_for('dashboard.return_dashboard'))

	rel = db.session.get(RelacionamentoTarefa, p.relacionamento_tarefa_id)
	emp = db.session.get(Empresa, rel.empresa_id) if rel else None
	user = db.session.get(Usuario, session.get('user_id')) if session.get('user_id') else None
	if (emp and getattr(emp, 'ativo', True) is False) or (user and getattr(user, 'ativo', True) is False):
		flash('Ação não permitida: usuário ou empresa inativos')
		return redirect(url_for('dashboard.return_dashboard'))
	if rel and user and rel.responsavel_id != user.id:
		flash('Ação não permitida para este usuário')
		return redirect(url_for('dashboard.return_dashboard'))

	p.status = 'pendente'
	db.session.commit()
	flash('Tarefa reaberta para retificação!')
	return redirect(url_for('dashboard.return_dashboard'))



