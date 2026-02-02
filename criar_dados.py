import pandas as pd
import random
from datetime import datetime, timedelta

# Gerando dados fictícios de pagamentos
random.seed(42)

fornecedores = ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor D', 'Fornecedor E']
departamentos = ['Compras', 'TI', 'Manutenção', 'Marketing', 'Operações']

dados = []
data_inicial = datetime(2024, 1, 1)

for i in range(200):
    registro = {
        'id_pagamento': f'PAG{i+1:04d}',
        'data': data_inicial + timedelta(days=random.randint(0, 365)),
        'fornecedor': random.choice(fornecedores),
        'departamento': random.choice(departamentos),
        'valor': round(random.uniform(500, 50000), 2),
        'tipo_pagamento': random.choice(['Boleto', 'TED', 'PIX']),
        'aprovador': random.choice(['Gestor 1', 'Gestor 2', 'Gestor 3'])
    }
    dados.append(registro)

# Adicionando alguns pagamentos duplicados intencionalmente (para testar detecção)
for i in range(10):
    dados.append(dados[i].copy())

df = pd.DataFrame(dados)
df.to_excel('pagamentos_fornecedores.xlsx', index=False)
print("✅ Arquivo 'pagamentos_fornecedores.xlsx' criado com sucesso!")
