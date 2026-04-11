
# Leitura dos três valores inteiros em uma única linha
entrada = input()
valor_transacao, taxa_servico, pagamento_minimo = map(int, entrada.split())

# Cálculo do valor líquido após a taxa
valor_final = valor_transacao - taxa_servico

# Verificação lógica: o valor final atende ao requisito mínimo?
if valor_final >= pagamento_minimo:
    print("Aprovada")
else:
    print("Recusada")



# Leitura dos três valores inteiros em uma única linha
entrada = input()
valor_transacao, taxa_servico, pagamento_minimo = map(int, entrada.split())

# TODO: Calcule o valor final da transação subtraindo a taxa do valor
# valor_final = ...

# Verifique se o valor final é suficiente para aprovar a transação
if valor_final >= pagamento_minimo:
    print("Aprovada")
else:
    print("Recusada")