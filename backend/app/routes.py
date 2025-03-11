# backend/app/routes.py
from flask import Blueprint, jsonify, request
from app.models import Receita, Despesa, CategoriaReceita, CategoriaDespesa
from app import db
from datetime import datetime
from sqlalchemy import extract

api = Blueprint('api', __name__)

# Rotas para Receitas
@api.route('/api/receitas', methods=['GET'])
def listar_receitas():
    receitas = Receita.query.all()
    return jsonify([{
        'id': r.id,
        'valor': r.valor,
        'descricao': r.descricao,
        'data': r.data.strftime('%Y-%m-%d'),
        'categoria': r.categoria,
        'recebido': r.recebido,
        'fixo': r.fixo
    } for r in receitas])

@api.route('/api/receitas', methods=['POST'])
def criar_receita():
    data = request.json
    try:
        nova_receita = Receita(
            valor=float(data['valor']),
            descricao=data['descricao'],
            data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
            categoria=data['categoria'],
            recebido=data.get('recebido', False),
            fixo=data.get('fixo', False)
        )
        db.session.add(nova_receita)
        db.session.commit()
        return jsonify({'message': 'Receita adicionada com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/api/receitas/<int:id>', methods=['PUT'])
def atualizar_receita(id):
    receita = Receita.query.get_or_404(id)
    data = request.json
    try:
        receita.valor = float(data.get('valor', receita.valor))
        receita.descricao = data.get('descricao', receita.descricao)
        receita.categoria = data.get('categoria', receita.categoria)
        receita.recebido = data.get('recebido', receita.recebido)
        receita.fixo = data.get('fixo', receita.fixo)
        if 'data' in data:
            receita.data = datetime.strptime(data['data'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'message': 'Receita atualizada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@api.route('/api/receitas/<int:id>', methods=['DELETE'])
def deletar_receita(id):
    receita = Receita.query.get_or_404(id)
    try:
        db.session.delete(receita)
        db.session.commit()
        return jsonify({'message': 'Receita deletada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rotas para Despesas
@api.route('/api/despesas', methods=['GET'])
def listar_despesas():
    despesas = Despesa.query.all()
    return jsonify([{
        'id': d.id,
        'valor': d.valor,
        'descricao': d.descricao,
        'data': d.data.strftime('%Y-%m-%d'),
        'categoria': d.categoria,
        'pago': d.pago,
        'fixo': d.fixo
    } for d in despesas])

@api.route('/api/despesas', methods=['POST'])
def criar_despesa():
    data = request.json
    try:
        nova_despesa = Despesa(
            valor=float(data['valor']),
            descricao=data['descricao'],
            data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
            categoria=data['categoria'],
            pago=data.get('pago', False),
            fixo=data.get('fixo', False)
        )
        db.session.add(nova_despesa)
        db.session.commit()
        return jsonify({'message': 'Despesa adicionada com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rotas para Categorias
@api.route('/api/categorias/receitas', methods=['GET'])
def listar_categorias_receitas():
    categorias = CategoriaReceita.query.all()
    return jsonify([{'id': c.id, 'nome': c.nome} for c in categorias])

@api.route('/api/categorias/receitas', methods=['POST'])
def criar_categoria_receita():
    data = request.json
    try:
        nova_categoria = CategoriaReceita(nome=data['nome'])
        db.session.add(nova_categoria)
        db.session.commit()
        return jsonify({'message': 'Categoria adicionada com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Rotas para Dashboard
@api.route('/api/dashboard/resumo', methods=['GET'])
def get_resumo():
    try:
        # Total de receitas
        total_receitas = db.session.query(db.func.sum(Receita.valor)).scalar() or 0
        
        # Total de despesas
        total_despesas = db.session.query(db.func.sum(Despesa.valor)).scalar() or 0
        
        # Saldo
        saldo = total_receitas - total_despesas
        
        # Receitas por categoria
        receitas_categoria = db.session.query(
            Receita.categoria,
            db.func.sum(Receita.valor)
        ).group_by(Receita.categoria).all()
        
        # Despesas por categoria
        despesas_categoria = db.session.query(
            Despesa.categoria,
            db.func.sum(Despesa.valor)
        ).group_by(Despesa.categoria).all()
        
        return jsonify({
            'saldo': saldo,
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'receitas_categoria': dict(receitas_categoria),
            'despesas_categoria': dict(despesas_categoria)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para relatórios mensais
@api.route('/api/relatorios/mensal/<int:ano>/<int:mes>', methods=['GET'])
def relatorio_mensal(ano, mes):
    try:
        # Receitas do mês
        receitas = Receita.query.filter(
            extract('year', Receita.data) == ano,
            extract('month', Receita.data) == mes
        ).all()
        
        # Despesas do mês
        despesas = Despesa.query.filter(
            extract('year', Despesa.data) == ano,
            extract('month', Despesa.data) == mes
        ).all()
        
        return jsonify({
            'receitas': [{
                'id': r.id,
                'valor': r.valor,
                'descricao': r.descricao,
                'data': r.data.strftime('%Y-%m-%d'),
                'categoria': r.categoria,
                'recebido': r.recebido,
                'fixo': r.fixo
            } for r in receitas],
            'despesas': [{
                'id': d.id,
                'valor': d.valor,
                'descricao': d.descricao,
                'data': d.data.strftime('%Y-%m-%d'),
                'categoria': d.categoria,
                'pago': d.pago,
                'fixo': d.fixo
            } for d in despesas]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    
    # Adicione estas novas rotas após as rotas existentes

@api.route('/api/transacoes', methods=['GET'])
def listar_transacoes():
    try:
        # Obter parâmetros de filtro
        tipo = request.args.get('tipo')
        categoria = request.args.get('categoria')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        # Iniciar queries
        receitas_query = Receita.query
        despesas_query = Despesa.query
        
        # Aplicar filtros
        if categoria and categoria != 'Todas':
            receitas_query = receitas_query.filter(Receita.categoria == categoria)
            despesas_query = despesas_query.filter(Despesa.categoria == categoria)
            
        if data_inicio and data_fim:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            receitas_query = receitas_query.filter(Receita.data.between(data_inicio, data_fim))
            despesas_query = despesas_query.filter(Despesa.data.between(data_inicio, data_fim))
        
        # Executar queries baseado no tipo
        transacoes = []
        if tipo is None or tipo == 'receita':
            receitas = receitas_query.all()
            transacoes.extend([{
                'id': r.id,
                'tipo': 'receita',
                'valor': r.valor,
                'descricao': r.descricao,
                'data': r.data.strftime('%Y-%m-%d'),
                'categoria': r.categoria,
                'status': 'Recebido' if r.recebido else 'Pendente',
                'fixo': r.fixo
            } for r in receitas])
            
        if tipo is None or tipo == 'despesa':
            despesas = despesas_query.all()
            transacoes.extend([{
                'id': d.id,
                'tipo': 'despesa',
                'valor': d.valor,
                'descricao': d.descricao,
                'data': d.data.strftime('%Y-%m-%d'),
                'categoria': d.categoria,
                'status': 'Pago' if d.pago else 'Pendente',
                'fixo': d.fixo
            } for d in despesas])
        
        # Ordenar por data
        transacoes.sort(key=lambda x: x['data'], reverse=True)
        
        return jsonify(transacoes)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/api/transacoes/<string:tipo>/<int:id>', methods=['DELETE'])
def deletar_transacao(tipo, id):
    try:
        if tipo == 'receita':
            transacao = Receita.query.get_or_404(id)
        elif tipo == 'despesa':
            transacao = Despesa.query.get_or_404(id)
        else:
            return jsonify({'error': 'Tipo inválido'}), 400
        
        db.session.delete(transacao)
        db.session.commit()
        return jsonify({'message': 'Transação excluída com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400