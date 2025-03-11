# backend/app/routes.py
from flask import Blueprint, jsonify, request
from app.models import Receita, Despesa, CategoriaReceita, CategoriaDespesa
from app import db
from datetime import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract, func

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
        # Obtém a data atual
        data_atual = datetime.now()
        
        # Cria uma lista com os últimos 6 meses
        meses = []
        receitas_mensais = []
        despesas_mensais = []
        
        for i in range(5, -1, -1):
            data_mes = data_atual - relativedelta(months=i)
            primeiro_dia = data_mes.replace(day=1)
            if i > 0:
                ultimo_dia = (data_mes.replace(day=1) + relativedelta(months=1) - relativedelta(days=1))
            else:
                ultimo_dia = data_atual
            
            # Adiciona o nome do mês em inglês (será traduzido no frontend)
            meses.append(data_mes.strftime('%B'))
            
            # Calcula receitas do mês
            receitas_mes = db.session.query(func.coalesce(func.sum(Receita.valor), 0))\
                .filter(Receita.data.between(primeiro_dia, ultimo_dia))\
                .scalar()
            
            # Calcula despesas do mês
            despesas_mes = db.session.query(func.coalesce(func.sum(Despesa.valor), 0))\
                .filter(Despesa.data.between(primeiro_dia, ultimo_dia))\
                .scalar()
            
            receitas_mensais.append(float(receitas_mes))
            despesas_mensais.append(float(despesas_mes))

        # Calcula totais gerais
        total_receitas = sum(receitas_mensais)
        total_despesas = sum(despesas_mensais)
        saldo = total_receitas - total_despesas
        
        # Calcula distribuição por categoria
        despesas_categoria = db.session.query(
            Despesa.categoria,
            func.sum(Despesa.valor)
        ).group_by(Despesa.categoria).all()
        
        return jsonify({
            'saldo': saldo,
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'despesas_categoria': dict(despesas_categoria),
            'fluxoCaixa': {
                'labels': meses,
                'receitas': receitas_mensais,
                'despesas': despesas_mensais
            }
        })
    except Exception as e:
        print(f"Erro no resumo: {str(e)}")  # Log do erro
        return jsonify({'error': str(e)}), 500

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
    
    
    
