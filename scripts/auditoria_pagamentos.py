import pandas as pd

print("="*60)
print("AUDITORIA DE PAGAMENTOS - BRF JUNDIAÍ")
print("="*60)

# 1. CARREGAR OS DADOS
print("\n📂 Carregando dados...")
df = pd.read_excel('pagamentos_fornecedores.xlsx')
print(f"✅ {len(df)} registros carregados")

# 2. EXPLORAÇÃO INICIAL
print("\n📊 VISÃO GERAL DOS DADOS")
print("-"*60)
print(df.head())
print("\n📈 Estatísticas Descritivas:")
print(df.describe())

# 3. VERIFICAR QUALIDADE DOS DADOS
print("\n🔍 VERIFICAÇÃO DE QUALIDADE")
print("-"*60)
valores_nulos = df.isnull().sum()
print(f"Valores nulos por coluna:\n{valores_nulos}")

# 4. IDENTIFICAR PAGAMENTOS DUPLICADOS
print("\n⚠️ DETECÇÃO DE DUPLICATAS")
print("-"*60)
# Consideramos duplicata se tiver mesmo fornecedor, valor e data
duplicatas = df[df.duplicated(subset=['fornecedor', 'valor', 'data'], keep=False)]
num_duplicatas = len(duplicatas)
print(f"🚨 {num_duplicatas} pagamentos duplicados encontrados!")

if num_duplicatas > 0:
    print("\nPrimeiras duplicatas identificadas:")
    print(duplicatas[['id_pagamento', 'fornecedor', 'valor', 'data']].head(10))
    
    # Exportar duplicatas para análise
    duplicatas.to_excel('pagamentos_duplicados.xlsx', index=False)
    print("📄 Arquivo 'pagamentos_duplicados.xlsx' gerado")

# 5. ANÁLISE DE VALORES ATÍPICOS
print("\n💰 ANÁLISE DE VALORES")
print("-"*60)
media_pagamentos = df['valor'].mean()
desvio_padrao = df['valor'].std()
limite_alto = media_pagamentos + (2 * desvio_padrao)

pagamentos_altos = df[df['valor'] > limite_alto]
print(f"Média de pagamentos: R$ {media_pagamentos:,.2f}")
print(f"Limite de alerta (média + 2 desvios): R$ {limite_alto:,.2f}")
print(f"🔴 {len(pagamentos_altos)} pagamentos acima do limite de alerta")

if len(pagamentos_altos) > 0:
    print("\nPagamentos que requerem atenção:")
    print(pagamentos_altos[['id_pagamento', 'fornecedor', 'valor', 'aprovador']].head(10))
    pagamentos_altos.to_excel('pagamentos_alto_valor.xlsx', index=False)

# 6. ANÁLISE POR FORNECEDOR
print("\n🏢 ANÁLISE POR FORNECEDOR")
print("-"*60)
analise_fornecedor = df.groupby('fornecedor').agg({
    'valor': ['count', 'sum', 'mean', 'max'],
    'id_pagamento': 'count'
}).round(2)

analise_fornecedor.columns = ['Qtd_Pagamentos', 'Total_Pago', 'Ticket_Medio', 'Maior_Pagamento', 'Registros']
analise_fornecedor = analise_fornecedor.sort_values('Total_Pago', ascending=False)
print(analise_fornecedor)

# 7. ANÁLISE POR DEPARTAMENTO
print("\n🏛️ ANÁLISE POR DEPARTAMENTO")
print("-"*60)
analise_depto = df.groupby('departamento').agg({
    'valor': ['count', 'sum', 'mean']
}).round(2)
analise_depto.columns = ['Qtd_Pagamentos', 'Total_Gasto', 'Ticket_Medio']
analise_depto = analise_depto.sort_values('Total_Gasto', ascending=False)
print(analise_depto)

# 8. ANÁLISE POR TIPO DE PAGAMENTO
print("\n💳 ANÁLISE POR TIPO DE PAGAMENTO")
print("-"*60)
tipo_pagamento = df['tipo_pagamento'].value_counts()
print(tipo_pagamento)

# 9. GERAR RESUMO EXECUTIVO
print("\n📋 RESUMO EXECUTIVO")
print("="*60)
total_pago = df['valor'].sum()
num_fornecedores = df['fornecedor'].nunique()
num_departamentos = df['departamento'].nunique()

print(f"""
📊 INDICADORES PRINCIPAIS
   • Total de pagamentos: {len(df)}
   • Total pago: R$ {total_pago:,.2f}
   • Ticket médio: R$ {media_pagamentos:,.2f}
   • Fornecedores ativos: {num_fornecedores}
   • Departamentos envolvidos: {num_departamentos}

⚠️ ACHADOS DE AUDITORIA
   • Pagamentos duplicados: {num_duplicatas}
   • Pagamentos acima do limite: {len(pagamentos_altos)}
   
🎯 RECOMENDAÇÕES
   1. Investigar pagamentos duplicados identificados
   2. Revisar aprovações de pagamentos acima de R$ {limite_alto:,.2f}
   3. Validar fornecedores com maior volume de transações
""")

# 10. EXPORTAR RELATÓRIO CONSOLIDADO
print("\n💾 Gerando relatórios...")
with pd.ExcelWriter('relatorio_auditoria_completo.xlsx') as writer:
    df.to_excel(writer, sheet_name='Dados_Completos', index=False)
    duplicatas.to_excel(writer, sheet_name='Duplicatas', index=False)
    pagamentos_altos.to_excel(writer, sheet_name='Alto_Valor', index=False)
    analise_fornecedor.to_excel(writer, sheet_name='Analise_Fornecedores')
    analise_depto.to_excel(writer, sheet_name='Analise_Departamentos')

print("✅ Relatório 'relatorio_auditoria_completo.xlsx' gerado com sucesso!")
print("\n🎉 Análise concluída!")

