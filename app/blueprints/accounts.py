from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import db
from app.models import Setor, Tributacao, Empresa, Usuario, Tarefa, RelacionamentoTarefa

bp = Blueprint('accounts', __name__, url_prefix='/tarefas')


@bp.get('')
@bp.get('/')
@bp.get('/page')
def return_page():
	setores = Setor.query.all()
	tributacoes = Tributacao.query.all()
	empresas = Empresa.query.order_by(Empresa.nome).all()
	usuarios = Usuario.query.order_by(Usuario.nome).all()

	# tarefas com nomes
	tarefas = []
	for t in Tarefa.query.all():
		setor = next((s for s in setores if s.id == t.setor_id), None)
		trib = next((tr for tr in tributacoes if tr.id == t.tributacao_id), None)
		tarefas.append({
			"id": t.id,
			"nome": t.nome,
			"tipo": t.tipo,
			"descricao": t.descricao,
			"setor_id": t.setor_id,
			"setor_nome": setor.nome if setor else '-',
			"tributacao_id": t.tributacao_id,
			"tributacao_nome": trib.nome if trib else '-',
		})

	# relacionamentos
	rels = []
	for r in RelacionamentoTarefa.query.all():
		emp = next((e for e in empresas if e.id == r.empresa_id), None)
		tarefa = Tarefa.query.get(r.tarefa_id)
		resp = Usuario.query.get(r.responsavel_id) if r.responsavel_id else None
		rels.append({
			"id": r.id,
			"empresa_nome": emp.nome if emp else '-',
			"tarefa_nome": tarefa.nome if tarefa else '-',
			"responsavel_nome": resp.nome if resp else None,
			"responsavel_id": r.responsavel_id,
			"status": r.status,
			"dia_vencimento": r.dia_vencimento,
			"prazo_especifico": r.prazo_especifico.isoformat() if r.prazo_especifico else None,
		})

	return render_template(
		'accounts.html',
		aba='contas',
		setores=setores,
		tributacoes=tributacoes,
		empresas=empresas,
		usuarios=usuarios,
		tarefas=tarefas,
		rels=rels,
	)


@bp.post('/create')
def create_task():
	t = Tarefa(
		nome=request.form.get('nome'),
		tipo=request.form.get('tipo'),
		descricao=request.form.get('descricao'),
		tributacao_id=request.form.get('tributacao_id', type=int),
		setor_id=request.form.get('setor_id', type=int)
	)
	db.session.add(t)
	db.session.commit()
	flash('Tarefa criada com sucesso!')
	return redirect(url_for('accounts.return_page'))


@bp.post('/edit')
def edit_task():
	tid = request.form.get('id', type=int)
	t = Tarefa.query.get(tid)
	if t:
		t.nome = request.form.get('nome')
		t.tipo = request.form.get('tipo')
		t.descricao = request.form.get('descricao')
		t.setor_id = request.form.get('setor_id', type=int)
		t.tributacao_id = request.form.get('tributacao_id', type=int)
		db.session.commit()
		flash('Tarefa atualizada!')
	return redirect(url_for('accounts.return_page'))


@bp.post('/delete')
def delete_task():
	tid = request.form.get('id', type=int)
	t = Tarefa.query.get(tid)
	if t:
		db.session.delete(t)
		db.session.commit()
		flash('Tarefa excluída!')
	return redirect(url_for('accounts.return_page'))


@bp.post('/link')
def link_task():
	rel = RelacionamentoTarefa(
		empresa_id=request.form.get('empresa_id', type=int),
		tarefa_id=request.form.get('tarefa_id', type=int),
		responsavel_id=request.form.get('responsavel_id', type=int),
		status='ativa',
		dia_vencimento=request.form.get('dia_vencimento', type=int),
		prazo_especifico=request.form.get('prazo_especifico') or None,
	)
	db.session.add(rel)
	db.session.commit()
	flash('Vínculo criado!')
	return redirect(url_for('accounts.return_page'))


@bp.post('/edit-link')
def edit_link():
	rid = request.form.get('id', type=int)
	r = RelacionamentoTarefa.query.get(rid)
	if r:
		r.status = request.form.get('status')
		r.responsavel_id = request.form.get('responsavel_id', type=int)
		r.dia_vencimento = request.form.get('dia_vencimento', type=int)
		r.prazo_especifico = request.form.get('prazo_especifico') or None
		db.session.commit()
		flash('Vínculo atualizado!')
	return redirect(url_for('accounts.return_page'))


@bp.post('/delete-link')
def delete_link():
	rid = request.form.get('id', type=int)
	r = RelacionamentoTarefa.query.get(rid)
	if r:
		db.session.delete(r)
		db.session.commit()
		flash('Vínculo excluído!')
	return redirect(url_for('accounts.return_page'))



