-- Insert data into `cliente`
INSERT INTO `cliente` (`nomeCliente`, `cpfCliente`, `senhaCliente`, `emailCliente`, `telefoneCliente`, `enderecoCliente`, `nascimentoCliente`, `sexoCliente`)
VALUES
('Ana Silva', '12345678901', 'senha123', 'ana.silva@email.com', '11987654321', 'Rua A, 123, São Paulo', '1990-05-15', 'F'),
('João Pereira', '23456789012', 'senha456', 'joao.pereira@email.com', '21987654321', 'Rua B, 456, Rio de Janeiro', '1985-08-22', 'M'),
('Maria Santos', '34567890123', 'senha789', 'maria.santos@email.com', '31987654321', 'Rua C, 789, Belo Horizonte', '1992-12-01', 'F'),
('Carlos Oliveira', '45678901234', 'senha012', 'carlos.oliveira@email.com', '41987654321', 'Rua D, 101, Curitiba', '1988-11-30', 'M');

-- Insert data into `administrador`
INSERT INTO `administrador` (`nomeAdministrador`, `cpfAdministrador`, `senhaAdministrador`, `emailAdministrador`, `telefoneAdministrador`, `enderecoAdministrador`, `nascimentoAdministrador`, `sexoAdministrador`, `idFuncionario`)
VALUES
('Roberta Lima', '56789012345', 'senha1234', 'roberta.lima@email.com', '51987654321', 'Rua E, 202, Porto Alegre', '1980-07-10', 'F', 'FUNC001'),
('Pedro Almeida', '67890123456', 'senha5678', 'pedro.almeida@email.com', '61987654321', 'Rua F, 303, Salvador', '1975-03-20', 'M', 'FUNC002'),
('Laura Costa', '78901234567', 'senha9101', 'laura.costa@email.com', '71987654321', 'Rua G, 404, Recife', '1995-09-15', 'F', 'FUNC003'),
('Fernando Silva', '89012345678', 'senha1121', 'fernando.silva@email.com', '81987654321', 'Rua H, 505, Fortaleza', '1983-04-05', 'M', 'FUNC004');

-- Insert data into `Produto`
INSERT INTO `Produto` (`nomeProduto`, `categoriaProduto`, `validadeProduto`, `pesoProduto`, `valorProduto`, `estoqueProduto`)
VALUES
('Arroz Tipo 1', 'Alimentos', '2025-01-01', 1.0, 20.50, 100),
('Feijão Preto', 'Alimentos', '2024-12-01', 0.5, 15.75, 50),
('Sabonete Líquido', 'Higiene', '2026-06-30', 0.25, 8.90, 75),
('Detergente', 'Higiene', '2025-11-15', 0.5, 12.30, 60);

-- Insert data into `Pedido`
INSERT INTO `Pedido` (`dataPedido`, `statusPedido`, `valorTotalPedido`, `idCliente`)
VALUES
('2024-08-15 14:30:00', 'Concluído', 40.90, 1),
('2024-08-16 09:00:00', 'Concluído', 27.80, 2),
('2024-08-17 11:45:00', 'Concluído', 21.20, 3),
('2024-08-18 16:20:00', 'Concluído', 12.30, 4);

-- Insert data into `ItemPedido`
INSERT INTO `ItemPedido` (`quantidadeItem`, `valorUnitarioItem`, `idPedido`, `idProduto`)
VALUES
(2, 20.50, 1, 1),
(1, 15.75, 2, 2),
(3, 8.90, 3, 3),
(1, 12.30, 4, 4);

-- Insert data into `Pagamento`
INSERT INTO `Pagamento` (`formaPagamento`, `parcelasPagamento`, `descontoPagamento`, `idPedido`)
VALUES
('Pix', NULL, 5.00, 1),
('Cartão de Crédito', 2, NULL, 2),
('Pix', NULL, 5.00, 3),
('Boleto', NULL, NULL, 4);

-- Insert data into `Avaliacao`
INSERT INTO `Avaliacao` (`notaAvaliacao`, `comentarioAvaliacao`, `dataAvaliacao`, `idCliente`, `idProduto`)
VALUES
(5, 'Excelente produto!', '2024-08-16 10:00:00', 1, 1),
(4, 'Bom, mas poderia ser melhor.', '2024-08-17 12:00:00', 2, 2),
(3, 'Cumpre o que promete.', '2024-08-18 15:00:00', 3, 3),
(2, 'Não gostei muito.', '2024-08-19 09:00:00', 4, 4);

-- Insert data into `TrocaDevolucao`
INSERT INTO `TrocaDevolucao` (`tipoTrocaDevolucao`, `dataSolicitacaoTrocaDevolucao`, `statusTrocaDevolucao`, `idPedido`, `idProduto`)
VALUES
('Troca', '2024-08-20', 'Aprovado', 1, 1),
('Devolução', '2024-08-21', 'Pendente', 2, 2),
('Troca', '2024-08-22', 'Aprovado', 3, 3),
('Devolução', '2024-08-23', 'Aprovado', 4, 4);
