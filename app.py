from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector


app = Flask(__name__)
app.secret_key = 'superSecreta'  # Mantenha esta chave segura e única

def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='e-commerce'
    )

@app.route('/')
def home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Corrigido para usar "Produto" com inicial maiúscula
    cursor.execute("SELECT nomeProduto, categoriaProduto, valorProduto FROM produto")
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', resultados=resultados)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT idCliente FROM cliente WHERE emailCliente = %s AND senhaCliente = %s
            """,
            (email, senha)
        )
        usuario = cursor.fetchone()
        cursor.close()
        connection.close()

        if usuario:
            # Armazenar o ID do cliente na sessão
            session['cliente_id'] = usuario['idCliente']
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('cliente'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':
        nome = request.form['nomeCliente']
        cpf = request.form['cpfCliente']
        senha = request.form['senhaCliente']
        email = request.form['emailCliente']
        telefone = request.form['telefoneCliente']
        endereco = request.form['enderecoCliente']
        nascimento = request.form['nascimentoCliente']
        sexo = request.form['sexoCliente']

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO cliente (nomeCliente, cpfCliente, senhaCliente, emailCliente, telefoneCliente, enderecoCliente, nascimentoCliente, sexoCliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (nome, cpf, senha, email, telefone, endereco, nascimento, sexo)
            )
            connection.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return "Erro ao registrar usuário. Tente novamente."
        finally:
            cursor.close()
            connection.close()

@app.route('/adm_prod', methods=['GET', 'POST'])
def adm_prod():
    
    # Verificar se o ADM está logado
    if 'adm_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('adm'))

    adm_id = session['adm_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Buscar todos os produtos disponíveis
    cursor.execute(
        """
        SELECT idProduto, nomeProduto, categoriaProduto, validadeProduto, pesoProduto, valorProduto, estoqueProduto
        FROM Produto
        """
    )
    produtos = cursor.fetchall()

    # Buscar o nome do ADM
    cursor.execute(
        """
        SELECT nomeAdministrador
        FROM administrador
        WHERE idAdministrador = """ + str(adm_id)
    )
    adminNome = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    connection.close()

    # Renderizar a página cliente.html, passando produtos e nome do ADM
    return render_template('adm_prod.html', adminNome=adminNome, produtos=produtos)

@app.route('/ver_pedidos', methods=['GET', 'POST'])
def ver_pedidos():
    
    # Verificar se o ADM está logado
    if 'adm_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('adm'))

    adm_id = session['adm_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Buscar todos os produtos disponíveis
    query = """
    SELECT 
        Pedido.idPedido,
        Pedido.dataPedido,
        Pedido.statusPedido,
        Pedido.valorTotalPedido,
        ItemPedido.idItem,
        ItemPedido.quantidadeItem,
        ItemPedido.valorUnitarioItem,
        Produto.nomeProduto
    FROM 
        ItemPedido
    JOIN 
        Pedido ON ItemPedido.idPedido = Pedido.idPedido
    JOIN 
        Produto ON ItemPedido.idProduto = Produto.idProduto;
    """
    
    cursor.execute(query)
    pedidos = cursor.fetchall()

    # Buscar o nome do ADM
    cursor.execute(
        """
        SELECT nomeAdministrador
        FROM administrador
        WHERE idAdministrador = """ + str(adm_id)
    )
    adminNome = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    connection.close()

    # Renderizar a página cliente.html, passando produtos e nome do ADM
    return render_template('ver_pedidos.html', adminNome=adminNome, pedidos=pedidos)

@app.route('/adm', methods=['GET', 'POST'])
def adm():
    if request.method == 'POST':
        id = request.form['id']
        senha = request.form['senha']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM administrador WHERE idAdministrador = %s AND senhaAdministrador = %s
            """,
            (id, senha)
        )
        usuario = cursor.fetchone()
        cursor.close()
        connection.close()

        if usuario:
            # Armazenar o ID do ADM na sessão
            session['adm_id'] = usuario['idAdministrador']
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('adm_prod'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
            return redirect(url_for('adm'))

    return render_template('adm.html')

@app.route('/cliente')
def cliente():

    # Verificar se o cliente está logado
    if 'cliente_id' not in session:
        flash('Você precisa estar logado para ver seus pedidos.', 'error')
        return redirect(url_for('login'))

    cliente_id = session['cliente_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Buscar todos os produtos disponíveis
    cursor.execute(
        """
        SELECT idProduto, nomeProduto, categoriaProduto, valorProduto
        FROM Produto
        """
    )
    produtos = cursor.fetchall()

    # Buscar o nome do cliente
    cursor.execute(
        """
        SELECT nomeCliente
        FROM Cliente
        WHERE idCliente = %s
        """,
        (cliente_id,)
    )
    clienteNome = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    cursor.close()
    connection.close()

    # Renderizar a página cliente.html, passando produtos e nome do cliente
    return render_template('cliente.html', clienteNome=clienteNome, produtos=produtos)


@app.route('/logout')
def logout():
    session.pop('cliente_id', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

@app.route('/logout_adm')
def logout_adm():
    session.pop('adm_id', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('adm'))

@app.route('/pedido')
def pedido():
    # Verificar se o cliente está logado
    if 'cliente_id' not in session:
        flash('Você precisa estar logado para ver seus pedidos.', 'error')
        return redirect(url_for('login'))

    cliente_id = session['cliente_id']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Buscar os pedidos do cliente
    cursor.execute(
        """
        SELECT P.nomeProduto, P.categoriaProduto, P.valorProduto 
        FROM Pedido PE
        JOIN ItemPedido IP ON PE.idPedido = IP.idPedido
        JOIN Produto P ON IP.idProduto = P.idProduto
        WHERE PE.idCliente = %s
        """,
        (cliente_id,)
    )
    pedido = cursor.fetchall()

    return render_template('pedido.html', pedido=pedido)

from flask import session, redirect, url_for, flash

@app.route('/adicionar_ao_carrinho/<int:id_produto>', methods=['POST'])
def adicionar_ao_carrinho(id_produto):
    # Verificar se o carrinho já existe na sessão
    if 'carrinho' not in session:
        session['carrinho'] = []

    # Buscar detalhes do produto a partir do ID
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Produto WHERE idProduto = %s", (id_produto,))
    produto = cursor.fetchone()
    cursor.close()
    connection.close()

    # Adicionar produto ao carrinho
    if produto:
        session['carrinho'].append({
            'idProduto': produto['idProduto'],  # Certifique-se de incluir idProduto
            'nomeProduto': produto['nomeProduto'],
            'categoriaProduto': produto['categoriaProduto'],
            'valorProduto': produto['valorProduto']
        })

    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('carrinho'))

@app.route('/deleta_produto')
def deleta_produto():
    if 'adm_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('adm'))

    adm_id = session['adm_id']
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Buscar o nome do ADM
    cursor.execute(
        """
        SELECT nomeAdministrador
        FROM administrador
        WHERE idAdministrador = """ + str(adm_id)
    )
    adminNome = cursor.fetchone()
    
    cursor.execute(
        """
        SELECT idProduto, nomeProduto, categoriaProduto, validadeProduto, pesoProduto, valorProduto, estoqueProduto
        FROM Produto
        """
    )
    items = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('deleta_produtos.html', adminNome=adminNome, items=items)

@app.route('/deleta_cliente')
def deleta_cliente():
    if 'adm_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('adm'))

    adm_id = session['adm_id']
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Buscar o nome do ADM
    cursor.execute(
        """
        SELECT nomeAdministrador
        FROM administrador
        WHERE idAdministrador = """ + str(adm_id)
    )
    adminNome = cursor.fetchone()
    
    cursor.execute(
        """
        SELECT idCliente, nomeCliente, cpfCliente, senhaCliente, emailCliente, telefoneCliente, enderecoCliente, nascimentoCliente, sexoCliente
        FROM cliente
        """
    )
    items = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('deleta_cliente.html', adminNome=adminNome, items=items)
    
    
@app.route('/remocao_produto', methods=['POST'])
def remocao_produto():
    if request.method == 'POST':
        # Captura os IDs dos produtos selecionados nas checkboxes
        selected_items = request.form.getlist('items')

        # Verifica se algum item foi selecionado
        if selected_items:
            connection = get_db_connection()
            cursor = connection.cursor()

            try:
                # Deleta os produtos selecionados com base nos IDs
                format_strings = ','.join(['%s'] * len(selected_items))
                cursor.execute(
                    f"DELETE FROM Produto WHERE idProduto IN ({format_strings})", tuple(selected_items)
                )
                connection.commit()
                flash(f'Produtos removidos com sucesso!', 'success')
            except mysql.connector.Error as e:
                flash(f'Erro ao deletar produtos: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
        else:
            flash('Nenhum produto foi selecionado.', 'error')

        return redirect(url_for('deleta_produto'))
    
@app.route('/remocao_cliente', methods=['POST'])
def remocao_cliente():
    if request.method == 'POST':
        # Captura os IDs dos clientes selecionados nas checkboxes
        selected_items = request.form.getlist('items')

        # Verifica se algum cliente foi selecionado
        if selected_items:
            connection = get_db_connection()
            cursor = connection.cursor()

            try:
                # Deleta os clientes selecionados com base nos IDs
                format_strings = ','.join(['%s'] * len(selected_items))
                cursor.execute(
                    f"DELETE FROM cliente WHERE idCliente IN ({format_strings})", tuple(selected_items)
                )
                connection.commit()
                flash(f'Clientes removidos com sucesso!', 'success')
            except mysql.connector.Error as e:
                flash(f'Erro ao deletar clientes: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
        else:
            flash('Nenhum cliente foi selecionado.', 'error')

        return redirect(url_for('deleta_cliente'))


@app.route('/cadastro_prod', methods=['GET', 'POST'])
def cadastro_prod():
    if 'adm_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('adm'))

    adm_id = session['adm_id']
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Buscar o nome do ADM
    cursor.execute(
        """
        SELECT nomeAdministrador
        FROM administrador
        WHERE idAdministrador = """ + str(adm_id)
    )
    adminNome = cursor.fetchone()

    if request.method == 'GET':
        return render_template('registro_produtos.html', adminNome=adminNome)
    elif request.method == 'POST':
        nomeProd = request.form['NomeProd']
        catProd = request.form['CatProd']
        validade = request.form['Validade']
        peso = request.form['Peso']
        valor = request.form['Valor']
        estoque = request.form['Estoque']

        try:
            cursor.execute(
                """
                INSERT INTO produto (nomeProduto, categoriaProduto, validadeProduto, pesoProduto, valorProduto, estoqueProduto)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (nomeProd, catProd, validade, peso, valor, estoque)
            )
            connection.commit()
            flash('Produto Cadastrado!', 'info')
            return redirect(url_for('cadastro_prod'))
        except mysql.connector.Error:
            flash('Erro, retornado ao Login.', 'error')
            return redirect(url_for('logout_adm'))
        finally:
            cursor.close()
            connection.close()
            
@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if 'adm_id' not in session:
        flash('Você precisa estar logado.', 'error')
        return redirect(url_for('adm'))

    adm_id = session['adm_id']
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Buscar o nome do ADM
    cursor.execute(
        """
        SELECT nomeAdministrador
        FROM administrador
        WHERE idAdministrador = """ + str(adm_id)
    )
    adminNome = cursor.fetchone()

    if request.method == 'GET':
        return render_template('registro_cliente.html', adminNome=adminNome)
    elif request.method == 'POST':
        NomeCliente = request.form['NomeCliente']
        CpfCliente = request.form['CpfCliente']
        SenhaCliente = request.form['SenhaCliente']
        EmailCliente = request.form['EmailCliente']
        TelefoneCliente = request.form['TelefoneCliente']
        EnderecoCliente = request.form['EnderecoCliente']
        NascimentoCliente = request.form['NascimentoCliente']
        SexoCliente = request.form['sexoCliente']

        try:
            cursor.execute(
                """
                INSERT INTO cliente (nomeCliente, cpfCliente, senhaCliente, emailCliente, telefoneCliente, enderecoCliente, nascimentoCliente, sexoCliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (NomeCliente, CpfCliente, SenhaCliente, EmailCliente, TelefoneCliente, EnderecoCliente, NascimentoCliente, SexoCliente)
            )
            connection.commit()
            flash('Cliente Cadastrado!', 'info')
            return redirect(url_for('cadastro_cliente'))
        except mysql.connector.Error:
            flash('Erro, retornado ao Login.', 'error')
            return redirect(url_for('logout_adm'))
        finally:
            cursor.close()
            connection.close()

@app.route('/carrinho')
def carrinho():
    # Verificar se o cliente está logado
    if 'cliente_id' not in session:
        flash('Você precisa estar logado para ver seu carrinho.', 'error')
        return redirect(url_for('login'))

    # Verificar se o carrinho existe na sessão
    carrinho = session.get('carrinho', [])

    return render_template('carrinho.html', carrinho=carrinho)

@app.route('/fechar_compra', methods=['POST'])
def fechar_compra():
    # Verificar se o cliente está logado
    if 'cliente_id' not in session:
        flash('Você precisa estar logado para finalizar a compra.', 'error')
        return redirect(url_for('login'))

    cliente_id = session['cliente_id']

    # Verificar se o carrinho não está vazio
    if 'carrinho' not in session or not session['carrinho']:
        flash('Seu carrinho está vazio.', 'error')
        return redirect(url_for('carrinho'))

    # Conectar ao banco de dados
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Calcular o valor total do pedido
        valor_total_pedido = sum(float(item['valorProduto']) for item in session['carrinho'])

        # Criar o pedido
        cursor.execute(
            """
            INSERT INTO Pedido (dataPedido, statusPedido, valorTotalPedido, idCliente)
            VALUES (NOW(), %s ,%s, %s)
            """,
            ("Concluído",valor_total_pedido, cliente_id)
        )
        pedido_id = cursor.lastrowid

        # Adicionar itens ao pedido
        for item in session['carrinho']:
            cursor.execute(
                """
                INSERT INTO ItemPedido (quantidadeItem, valorUnitarioItem, idPedido, idProduto)
                VALUES (1, %s, %s, %s)  -- Assumindo quantidade 1 para simplicidade
                """,
                (float(item['valorProduto']), pedido_id, int(item['idProduto']))
            )

        # Confirmar transação
        connection.commit()
    
    except mysql.connector.Error as err:
        flash(f'Ocorreu um erro ao processar o pedido: {err}', 'error')
        connection.rollback()
    
    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        connection.close()

    # Limpar o carrinho
    session.pop('carrinho', None)

    flash('Compra finalizada com sucesso!', 'success')
    return redirect(url_for('cliente'))




if __name__ == '__main__':
    app.run(debug=True)
