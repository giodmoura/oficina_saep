from flask import flash, redirect, render_template, request, url_for
from banco import obter_conexao


def listar_agendamentos():
    """Lista serviços ordenados por data, com informações do cliente e veículo."""
    conexao = obter_conexao()
    agendamentos = []
    clientes = []
    veiculos = []
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            query = """SELECT a.id AS agendamento_id, a.data_agendamento, a.descricao_servico, a.status,
                              a.valor_estimado, a.observacoes,
                              c.id AS cliente_id, c.nome AS cliente_nome, c.cpf AS cliente_cpf,
                              c.telefone AS cliente_telefone, c.email AS cliente_email, c.endereco AS cliente_endereco,
                              v.id AS veiculo_id, v.placa AS veiculo_placa, v.marca AS veiculo_marca,
                              v.modelo AS veiculo_modelo, v.ano AS veiculo_ano, v.cor AS veiculo_cor,
                              v.quilometragem AS veiculo_quilometragem
                       FROM agendamentos a
                       JOIN clientes c ON a.cliente_id = c.id
                       JOIN veiculos v ON a.veiculo_id = v.id
                       ORDER BY a.data_agendamento ASC"""
            cursor.execute(query)
            agendamentos = cursor.fetchall()
            cursor.execute("SELECT id, nome, telefone FROM clientes ORDER BY nome ASC")
            clientes = cursor.fetchall()
            cursor.execute("""SELECT v.id, v.placa, v.marca, v.modelo, c.nome AS cliente_nome
                              FROM veiculos v JOIN clientes c ON v.cliente_id = c.id ORDER BY c.nome ASC""")
            veiculos = cursor.fetchall()
        finally:
            conexao.close()
    return render_template('agendamentos.html', agendamentos=agendamentos, clientes=clientes, veiculos=veiculos)


def cadastrar_agendamento():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        veiculo_id = request.form.get('veiculo_id')
        data_agendamento = request.form.get('data_agendamento')
        descricao = request.form.get('descricao_servico', '').strip()
        valor = request.form.get('valor_estimado', '0.00').replace(',', '.')
        obs = request.form.get('observacoes', '').strip()
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = """INSERT INTO agendamentos
                         (cliente_id, veiculo_id, data_agendamento, descricao_servico, status, valor_estimado, observacoes)
                         VALUES (%s, %s, %s, %s, 'Agendado', %s, %s)"""
                cursor.execute(sql, (cliente_id, veiculo_id, data_agendamento.replace('T', ' '), descricao, float(valor or 0), obs))
                conexao.commit()
                flash('Agendamento cadastrado com sucesso!', 'sucesso')
            except Exception as e:
                flash(f'Erro ao cadastrar agendamento: {str(e)}', 'erro')
            finally:
                conexao.close()
        else:
            flash('Erro de conexão com o banco de dados.', 'erro')
    return redirect(url_for('agendamentos_view'))


def atualizar_data_agendamento(agendamento_id: int):
    if request.method == 'POST':
        nova_data = request.form.get('nova_data_agendamento')
        if not nova_data:
            flash('Informe a nova data e horário.', 'erro')
            return redirect(url_for('agendamentos_view'))
        conexao = obter_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = "UPDATE agendamentos SET data_agendamento = %s WHERE id = %s"
                cursor.execute(sql, (nova_data.replace('T', ' '), agendamento_id))
                conexao.commit()
                flash(f'Data do agendamento #{agendamento_id} atualizada com sucesso no banco!', 'sucesso')
            except Exception as e:
                flash(f'Erro ao atualizar data: {str(e)}', 'erro')
            finally:
                conexao.close()
    return redirect(url_for('agendamentos_view'))


def excluir_agendamento(agendamento_id: int):
    conexao = obter_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM agendamentos WHERE id = %s", (agendamento_id,))
            conexao.commit()
            flash('Agendamento excluído.', 'sucesso')
        finally:
            conexao.close()
    return redirect(url_for('agendamentos_view'))
