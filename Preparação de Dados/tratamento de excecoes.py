try:
    numero = 10/0
    print(numero)
except ZeroDivisionError:
    print("Não é possível dividir por zero.")
finally:
    print("Execução finalizada.")


#idade = -5
#
#if idade < 0:
#    raise ValueError("A idade não pode ser negativa.")



numero = input("Digite um número: ")
if numero.isdigit():
    numero = int(numero)
    print("O número digitado é:", numero)
else:
    print("Entrada inválida. Por favor, digite um número inteiro.")

    
divisor = 0

print('numero:', numero)
print('divisor:', divisor)
resultado = numero / divisor
print('resultado:', resultado)

import logging
logging.basicConfig(filename="sistema.log", level=logging.ERROR)
logging.info("Início do programa.")
logging.error("Ocorreu um erro ao dividir por zero.")
logging.warning("O divisor é zero, operação inválida.")
logging.debug("Valor do número: %d, Valor do divisor: %d", numero, divisor)
logging.critical("Erro crítico: divisão por zero.")

