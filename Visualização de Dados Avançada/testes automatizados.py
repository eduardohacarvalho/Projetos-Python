def soma(a,b):
    return a + b

# Teste simples usando assert
assert soma(2, 3) == 5

# Teste usando pytest
def test_soma():
    assert soma(2, 3) == 5