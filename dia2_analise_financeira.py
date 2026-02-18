import pandas as pd
import numpy as np

# ============================================
# 1. CARREGAR DADOS
# ============================================
dados = pd.read_csv('dados_financeiro.csv')

print("=" * 60)
print("📊 ANÁLISE FINANCEIRA - PROJETADO VS REALIZADO")
print("=" * 60)

# ============================================
# 2. ANÁLISE: PROJETADO VS REALIZADO
# ============================================
print("\n🔍 ANÁLISE 1: VARIAÇÃO PROJETADO VS REALIZADO\n")

# Calcular variação (realizado - projetado)
dados['variacao'] = dados['realizado'] - dados['projetado']
dados['variacao_pct'] = (dados['variacao'] / dados['projetado']) * 100

# Por área
por_area = dados.groupby('area').agg({
    'projetado': 'sum',
    'realizado': 'sum',
    'variacao': 'sum'
}).round(0)

por_area['variacao_pct'] = ((por_area['realizado'] - por_area['projetado']) / por_area['projetado'] * 100).round(1)

print(por_area)
print("\n💡 INSIGHTS:")
for area, row in por_area.iterrows():
    if row['variacao'] > 0:
        print(f"   ⚠️  {area}: ESTOUROU orçamento em R$ {row['variacao']:,.0f} ({row['variacao_pct']:.1f}%)")
    else:
        print(f"   ✅ {area}: ECONOMIZOU R$ {abs(row['variacao']):,.0f} ({abs(row['variacao_pct']):.1f}%)")

# ============================================
# 3. VARIAÇÕES ENTRE MESES
# ============================================
print("\n" + "=" * 60)
print("📈 ANÁLISE 2: EVOLUÇÃO DE GASTOS POR ÁREA\n")

evolucao = dados.groupby(['mes', 'area'])['realizado'].sum().unstack()
crescimento = evolucao.pct_change() * 100

print("Crescimento % mês a mês:\n")
print(crescimento.round(1))

print("\n💡 INSIGHTS:")
# Última variação (mês mais recente)
ultima_var = crescimento.iloc[-1]
for area in ultima_var.index:
    var = ultima_var[area]
    if pd.notna(var):
        if var > 10:
            print(f"   ⚠️  {area}: AUMENTO de {var:.1f}% no último mês!")
        elif var < -10:
            print(f"   ✅ {area}: REDUÇÃO de {abs(var):.1f}% no último mês")

# ============================================
# 4. CORRELAÇÃO COM RECEITA
# ============================================
print("\n" + "=" * 60)
print("🔗 ANÁLISE 3: CORRELAÇÃO GASTOS x RECEITA x CHURN\n")

# Agregar por mês
por_mes = dados.groupby('mes').agg({
    'realizado': 'sum',
    'receita_mes': 'first',
    'churn_mes': 'first'
})

# Calcular correlações
corr_receita = por_mes['realizado'].corr(por_mes['receita_mes'])
corr_churn = por_mes['realizado'].corr(por_mes['churn_mes'])

print(f"Correlação Gastos x Receita: {corr_receita:.2f}")
print(f"Correlação Gastos x Churn:   {corr_churn:.2f}")

print("\n💡 INTERPRETAÇÃO:")
if corr_receita > 0.7:
    print(f"   ✅ Forte correlação POSITIVA com receita ({corr_receita:.2f})")
    print("      → Gastos crescem conforme receita cresce (esperado!)")
elif corr_receita < -0.7:
    print(f"   ⚠️  Correlação NEGATIVA com receita ({corr_receita:.2f})")
    print("      → Gastos crescem quando receita cai (PROBLEMA!)")
else:
    print(f"   📊 Correlação moderada com receita ({corr_receita:.2f})")

if corr_churn > 0.5:
    print(f"   ⚠️  Correlação com churn ({corr_churn:.2f})")
    print("      → Mais gastos = mais churn? Investigar!")
elif corr_churn < -0.5:
    print(f"   ✅ Correlação NEGATIVA com churn ({corr_churn:.2f})")
    print("      → Mais gastos = menos churn (investimento válido!)")

# ============================================
# 5. ÁREAS MAIS DESCONTROLADAS
# ============================================
print("\n" + "=" * 60)
print("🎯 ANÁLISE 4: ÁREAS COM MAIOR DESVIO\n")

desvio_por_area = dados.groupby('area')['variacao_pct'].agg(['mean', 'std']).round(1)
desvio_por_area.columns = ['Desvio_Médio_%', 'Volatilidade']
desvio_por_area = desvio_por_area.sort_values('Desvio_Médio_%', ascending=False)

print(desvio_por_area)

print("\n💡 INSIGHTS:")
for area, row in desvio_por_area.iterrows():
    if abs(row['Desvio_Médio_%']) > 5:
        print(f"   ⚠️  {area}: Desvio médio de {row['Desvio_Médio_%']:.1f}% - ATENÇÃO!")
    if row['Volatilidade'] > 5:
        print(f"   📊 {area}: Alta volatilidade ({row['Volatilidade']:.1f}%) - Instável")

# ============================================
# 6. RESUMO EXECUTIVO
# ============================================
print("\n" + "=" * 60)
print("📋 RESUMO EXECUTIVO\n")

total_projetado = dados['projetado'].sum()
total_realizado = dados['realizado'].sum()
variacao_total = total_realizado - total_projetado
variacao_total_pct = (variacao_total / total_projetado) * 100

print(f"Total Projetado:  R$ {total_projetado:,.0f}")
print(f"Total Realizado:  R$ {total_realizado:,.0f}")
print(f"Variação:         R$ {variacao_total:,.0f} ({variacao_total_pct:.1f}%)")

if variacao_total > 0:
    print(f"\n⚠️  ORÇAMENTO ESTOURADO em R$ {variacao_total:,.0f}!")
else:
    print(f"\n✅ ECONOMIA de R$ {abs(variacao_total):,.0f}!")

print("\n" + "=" * 60)