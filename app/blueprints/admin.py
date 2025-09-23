from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import db
from app.models import Usuario, Setor, Empresa, Tributacao

bp = Blueprint('admin', __name__, url_prefix='/admin')


def require_admin():
	if session.get('user_tipo') != 'admin':
		return redirect(url_for('dashboard.return_dashboard'))
	return None


@bp.get('')
@bp.get('/')

def admin_page():
	guard = require_admin()
	if guard:
		return guard
	setores = Setor.query.all()
	tributacoes = Tributacao.query.all()
	usuarios = Usuario.query.order_by(Usuario.nome).all()
	empresas = Empresa.query.order_by(Empresa.nome).all()
	return render_template('admin.html', aba='admin', setores=setores, tributacoes=tributacoes, usuarios=usuarios, empresas=empresas)


@bp.post('/usuarios')

def create_user():
	guard = require_admin()
	if guard:
		return guard
	u = Usuario(
		nome=request.form.get('nome'),
		login=request.form.get('login'),
		senha=request.form.get('senha'),
		tipo=request.form.get('tipo'),
		setor_id=request.form.get('setor_id', type=int),
		ativo=True
	)
	db.session.add(u)
	db.session.commit()
	flash('Usuário cadastrado!')
	return redirect(url_for('admin.admin_page'))


@bp.post('/empresas')

def create_company():
	guard = require_admin()
	if guard:
		return guard
	e = Empresa(
		codigo=request.form.get('codigo'),
		nome=request.form.get('nome'),
		tributacao_id=request.form.get('tributacao_id', type=int),
		ativo=True
	)
	db.session.add(e)
	db.session.commit()
	flash('Empresa cadastrada!')
	return redirect(url_for('admin.admin_page'))


@bp.post('/usuarios/<int:user_id>/toggle')

def toggle_user(user_id: int):
	guard = require_admin()
	if guard:
		return guard
	u = Usuario.query.get(user_id)
	if not u:
		flash('Usuário não encontrado')
		return redirect(url_for('admin.admin_page'))
	u.ativo = not bool(u.ativo)
	db.session.commit()
	flash('Usuário ativado' if u.ativo else 'Usuário desativado')
	return redirect(url_for('admin.admin_page'))


@bp.post('/empresas/<int:empresa_id>/toggle')

def toggle_company(empresa_id: int):
	guard = require_admin()
	if guard:
		return guard
	e = Empresa.query.get(empresa_id)
	if not e:
		flash('Empresa não encontrada')
		return redirect(url_for('admin.admin_page'))
	e.ativo = not bool(e.ativo)
	db.session.commit()
	flash('Empresa ativada' if e.ativo else 'Empresa desativada')
	return redirect(url_for('admin.admin_page'))
