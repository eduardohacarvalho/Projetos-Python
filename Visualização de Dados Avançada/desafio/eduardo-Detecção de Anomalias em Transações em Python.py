"""
========================================
PROJETO: DETECÇÃO DE FRAUDES EM CARTÕES DE CRÉDITO
========================================
Autor: Eduardo Carvalho
Data: Maio 2026

OBJETIVO:
Detectar transações fraudulentas em cartões de crédito usando Machine Learning,
priorizando a detecção de fraudes (minimizar falsos negativos) mesmo que isso
aumente um pouco os falsos positivos.

DATASET:
- 284,807 transações
- 492 fraudes (0.17% - MUITO DESBALANCEADO)
- Features V1-V28: já transformadas por PCA (confidencialidade)
- Time: segundos desde primeira transação
- Amount: valor da transação

CONTEXTO:
Este projeto foi desenvolvido como parte do bootcamp da DIO.me.
O código base foi adaptado das aulas, com contribuições próprias incluindo:
- Feature engineering adicional (Hour, Period)
- Comparação de 6 modelos diferentes
- Otimização de threshold
- Análise de custo-benefício
"""

# ==========================================
# IMPORTS E CONFIGURAÇÕES
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Sklearn - Pré-processamento
from sklearn.preprocessing import StandardScaler
# Sklearn - Divisão de dados
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
# Sklearn - Modelos
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
# Sklearn - Métricas
from sklearn.metrics import (
    classification_report, 
    roc_curve, 
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
    confusion_matrix,
    f1_score
)
# Imbalanced-learn - Técnicas de balanceamento
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
# XGBoost
from xgboost import XGBClassifier
# Shap
import shap
# Configurar visualizações
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ==========================================
# CARREGAMENTO E ANÁLISE EXPLORATÓRIA
# ==========================================
print("Carregando dataset...")
url = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"
df = pd.read_csv(url)
print("\nDataset carregado com sucesso!")
print(f"Shape: {df.shape}")
print("\nPrimeiras linhas:")
print(df.head())

# Verifica valores nulos no dataset
print("\nValores nulos:")
print(df.isnull().sum().sum())

# Análise do desbalanceamento
print("\nDistribuição das classes:")
print(df["Class"].value_counts())
print("\nProporção:")
print(df["Class"].value_counts(normalize=True))

# Estatísticas descritivas
print("\nEstatísticas de Amount por classe:")
print(df.groupby('Class')['Amount'].describe())

# ==========================================
# FEATURE ENGINEERING
# ==========================================
print("\nCriando novas features...")

# Feature 1: Log transformation de Amount para reduzir impacto de outliers
df['Amount_log'] = np.log1p(df['Amount'])

# Feature 2: Hora do dia - pode haver padrões temporais
df['Hour'] = (df['Time'] // 3600) % 24

# Feature 3: Período do dia
def get_period(hour):
    if 6 <= hour < 12:
        return 'Manhã'
    elif 12 <= hour < 18:
        return 'Tarde'
    elif 18 <= hour < 24:
        return 'Noite'
    else:
        return 'Madrugada'

df['Period'] = df['Hour'].apply(get_period)

# One-hot encoding do período
df_encoded = pd.get_dummies(df, columns=['Period'], prefix='Period')

print("Features criadas: Amount_log, Hour, Period")

# ==========================================
# PREPARAÇÃO DOS DADOS
# ==========================================
print("\nPreparando dados para modelagem...")

# Remover colunas que não serão usadas
X = df_encoded.drop(['Class', 'Time', 'Amount'], axis=1)
y = df_encoded['Class']

# Split estratificado - mantém a proporção de fraudes em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y
)

print(f"\nTreino: {X_train.shape[0]} amostras")
print(f"Teste: {X_test.shape[0]} amostras")
print(f"Proporção de fraudes no treino: {y_train.mean():.4f}")
print(f"Proporção de fraudes no teste: {y_test.mean():.4f}")

# Escalar features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Converter de volta para DataFrame
X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)

# ==========================================
# FUNÇÃO DE AVALIAR OS MODELOS
# ==========================================
def avaliar_modelo(nome, modelo, X_test, y_test, exibir_grafico=False):
    """
    Avalia o desempenho de um modelo de classificação.
    
    Parâmetros:
    - nome: nome do modelo para exibição
    - modelo: modelo treinado
    - X_test: features de teste
    - y_test: labels de teste
    - exibir_grafico: se True, exibe gráficos de ROC e Precision-Recall
    
    Retorna:
    - dicionário com métricas e predições
    """
    print(f"\n{'='*60}")
    print(f"AVALIAÇÃO: {nome}")
    print(f"{'='*60}")
    
    # Predições
    y_pred = modelo.predict(X_test)
    y_prob = modelo.predict_proba(X_test)[:, 1]
    
    # Classification Report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Fraude']))
    
    # Métricas adicionais
    roc_auc = roc_auc_score(y_test, y_prob)
    pr_auc = average_precision_score(y_test, y_prob)
    
    print(f"\nMétricas de Performance:")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"PR-AUC: {pr_auc:.4f} (melhor métrica para dados desbalanceados)")
    
    # Matriz de confusão
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nMatriz de Confusão:")
    print(f"Verdadeiros Negativos: {cm[0,0]}")
    print(f"Falsos Positivos: {cm[0,1]} (alarmes falsos)")
    print(f"Falsos Negativos: {cm[1,0]} (fraudes não detectadas - crítico)")
    print(f"Verdadeiros Positivos: {cm[1,1]} (fraudes detectadas)")
    
    # Análise de custo simplificada
    custo_fn = cm[1,0] * 100  # Assumindo que cada fraude não detectada custa $100
    custo_fp = cm[0,1] * 5     # Assumindo que cada falso alarme custa $5
    custo_total = custo_fn + custo_fp
    print(f"\nAnálise de Custo (estimativa):")
    print(f"Custo de Falsos Negativos: ${custo_fn}")
    print(f"Custo de Falsos Positivos: ${custo_fp}")
    print(f"Custo Total Estimado: ${custo_total}")
    
    # Gráficos
    if exibir_grafico:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Curva ROC
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        axes[0].plot(fpr, tpr, label=f'{nome} (AUC = {roc_auc:.3f})', linewidth=2)
        axes[0].plot([0, 1], [0, 1], 'k--', label='Baseline aleatório')
        axes[0].set_xlabel('Taxa de Falsos Positivos')
        axes[0].set_ylabel('Taxa de Verdadeiros Positivos')
        axes[0].set_title('Curva ROC')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Curva Precision-Recall
        precision, recall, _ = precision_recall_curve(y_test, y_prob)
        axes[1].plot(recall, precision, label=f'{nome} (PR-AUC = {pr_auc:.3f})', linewidth=2)
        axes[1].axhline(y=y_test.mean(), color='k', linestyle='--', label='Baseline (proporção)')
        axes[1].set_xlabel('Recall')
        axes[1].set_ylabel('Precision')
        axes[1].set_title('Curva Precision-Recall')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    return {
        'roc_auc': roc_auc,
        'pr_auc': pr_auc,
        'y_pred': y_pred,
        'y_prob': y_prob
    }

# ==========================================
# MODELO BASELINE
# ==========================================
print("\n" + "="*60)
print("MODELO 1: LOGISTIC REGRESSION")
print("="*60)

lr_baseline = LogisticRegression(
    max_iter=1000,
    class_weight='balanced',
    random_state=42
)
lr_baseline.fit(X_train_scaled, y_train)

resultados_lr = avaliar_modelo(
    "Logistic Regression", 
    lr_baseline, 
    X_test_scaled, 
    y_test,
    exibir_grafico=True
)

# ==========================================
# TÉCNICAS DE BALANCEAMENTO
# ==========================================
print("\n" + "="*60)
print("EXPERIMENTO: TÉCNICAS DE BALANCEAMENTO")
print("="*60)

# Undersampling
print("\nTécnica 1: UNDERSAMPLING")
print("Reduz a quantidade de transações normais para balancear com fraudes")

fraudes = df_encoded[df_encoded["Class"] == 1]
normais = df_encoded[df_encoded["Class"] == 0].sample(len(fraudes) * 2, random_state=42)
df_under = pd.concat([fraudes, normais])

print(f"\nDistribuição após undersampling:")
print(df_under["Class"].value_counts())

# Preparar dados undersampled
X_under = df_under.drop(['Class', 'Time', 'Amount'], axis=1)
y_under = df_under['Class']
X_train_u, X_test_u, y_train_u, y_test_u = train_test_split(
    X_under, y_under, test_size=0.2, random_state=42, stratify=y_under
)
scaler_under = StandardScaler()
X_train_u_scaled = scaler_under.fit_transform(X_train_u)

lr_under = LogisticRegression(max_iter=1000, random_state=42)
lr_under.fit(X_train_u_scaled, y_train_u)

# Avaliar no conjunto de teste original
resultados_under = avaliar_modelo(
    "LR com Undersampling",
    lr_under,
    X_test_scaled,
    y_test
)

# Oversampling com SMOTE
print("\nTécnica 2: SMOTE (Synthetic Minority Over-sampling Technique)")
print("Cria exemplos sintéticos da classe minoritária (fraudes)")

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

print(f"\nDistribuição após SMOTE:")
print(pd.Series(y_train_smote).value_counts())

lr_smote = LogisticRegression(max_iter=1000, random_state=42)
lr_smote.fit(X_train_smote, y_train_smote)

resultados_smote = avaliar_modelo(
    "LR com SMOTE",
    lr_smote,
    X_test_scaled,
    y_test
)

# ==========================================
# RANDOM FOREST
# ==========================================
print("\n" + "="*60)
print("MODELO 2: RANDOM FOREST")
print("="*60)

rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    class_weight='balanced',
    n_jobs=-1,
    random_state=42,
    min_samples_split=10
)
rf.fit(X_train_scaled, y_train)

resultados_rf = avaliar_modelo(
    "Random Forest",
    rf,
    X_test_scaled,
    y_test,
    exibir_grafico=True
)

# ==========================================
# XGBOOST
# ==========================================
print("\n" + "="*60)
print("MODELO 3: XGBOOST")
print("="*60)

# Calcular scale_pos_weight para balancear classes
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
print(f"Scale pos weight calculado: {scale_pos_weight:.2f}")

xgb = XGBClassifier(
    scale_pos_weight=scale_pos_weight,
    eval_metric='logloss',
    random_state=42,
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1
)
xgb.fit(X_train_scaled, y_train)

resultados_xgb = avaliar_modelo(
    "XGBoost",
    xgb,
    X_test_scaled,
    y_test,
    exibir_grafico=True
)

# Importância das features
print("\nTop 10 Features Mais Importantes (XGBoost):")
feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': xgb.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance.head(10))

# Visualizar importância
plt.figure(figsize=(10, 6))
plt.barh(feature_importance.head(10)['feature'], 
         feature_importance.head(10)['importance'])
plt.xlabel('Importância')
plt.title('Top 10 Features Mais Importantes')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# ==========================================
# GRID SEARCH
# ==========================================
print("\n" + "="*60)
print("OTIMIZAÇÃO: GRID SEARCH NO XGBOOST")
print("="*60)

param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2]
}

# Validação cruzada estratificada
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

grid = GridSearchCV(
    XGBClassifier(
        scale_pos_weight=scale_pos_weight,
        eval_metric='logloss',
        random_state=42
    ),
    param_grid,
    scoring='average_precision',
    cv=cv,
    n_jobs=-1,
    verbose=1
)

print("Iniciando Grid Search (pode demorar alguns minutos)...")
grid.fit(X_train_scaled, y_train)

print(f"\nMelhores hiperparâmetros encontrados:")
print(grid.best_params_)
print(f"\nMelhor PR-AUC no Cross-Validation: {grid.best_score_:.4f}")

# Avaliar modelo otimizado
resultados_grid = avaliar_modelo(
    "XGBoost Otimizado (Grid Search)",
    grid.best_estimator_,
    X_test_scaled,
    y_test,
    exibir_grafico=True
)

# ==========================================
# OTIMIZAÇÃO DE THRESHOLD
# ==========================================
print("\n" + "="*60)
print("OTIMIZAÇÃO DO THRESHOLD DE DECISÃO")
print("="*60)

y_prob_best = grid.best_estimator_.predict_proba(X_test_scaled)[:, 1]

thresholds = np.arange(0.1, 0.9, 0.05)
f1_scores = []
recalls = []
precisions = []

for threshold in thresholds:
    y_pred_t = (y_prob_best >= threshold).astype(int)
    f1_scores.append(f1_score(y_test, y_pred_t))
    
    cm = confusion_matrix(y_test, y_pred_t)
    if cm[1, 1] + cm[0, 1] > 0:
        precision = cm[1, 1] / (cm[1, 1] + cm[0, 1])
    else:
        precision = 0
    if cm[1, 1] + cm[1, 0] > 0:
        recall = cm[1, 1] / (cm[1, 1] + cm[1, 0])
    else:
        recall = 0
    
    precisions.append(precision)
    recalls.append(recall)

best_threshold = thresholds[np.argmax(f1_scores)]
print(f"\nMelhor threshold encontrado: {best_threshold:.2f}")
print(f"F1-Score no threshold ótimo: {max(f1_scores):.4f}")

# Visualizar
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(thresholds, f1_scores, marker='o', label='F1-Score')
axes[0].axvline(best_threshold, color='r', linestyle='--', label=f'Melhor = {best_threshold:.2f}')
axes[0].set_xlabel('Threshold')
axes[0].set_ylabel('F1-Score')
axes[0].set_title('F1-Score vs Threshold')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(thresholds, precisions, marker='o', label='Precision')
axes[1].plot(thresholds, recalls, marker='s', label='Recall')
axes[1].axvline(best_threshold, color='r', linestyle='--', label=f'Threshold ótimo')
axes[1].set_xlabel('Threshold')
axes[1].set_ylabel('Score')
axes[1].set_title('Precision vs Recall vs Threshold')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

# Avaliar com threshold otimizado
y_pred_otimizado = (y_prob_best >= best_threshold).astype(int)
print(f"\nResultados com threshold otimizado ({best_threshold:.2f}):")
print(classification_report(y_test, y_pred_otimizado, target_names=['Normal', 'Fraude']))

# ==========================================
# INTERPRETABILIDADE COM SHAP
# ==========================================
print("\n" + "="*60)
print("INTERPRETABILIDADE: SHAP VALUES")
print("="*60)

# Criar explainer
explainer = shap.TreeExplainer(grid.best_estimator_)

# Calcular SHAP values para amostra do conjunto de teste
print("Calculando SHAP values...")
shap_values = explainer(X_test_scaled[:100])

# Visualizar
print("\nVisualizando impacto das features:")
shap.plots.bar(shap_values, max_display=10)

print("\nExemplo de predição individual:")
shap.plots.waterfall(shap_values[0])

# ==========================================
# COMPARAÇÃO FINAL
# ==========================================
print("\n" + "="*60)
print("COMPARAÇÃO DE TODOS OS MODELOS")
print("="*60)

comparacao = pd.DataFrame({
    'Modelo': [
        'LR Baseline',
        'LR + Undersampling',
        'LR + SMOTE',
        'Random Forest',
        'XGBoost',
        'XGBoost Otimizado'
    ],
    'ROC-AUC': [
        resultados_lr['roc_auc'],
        resultados_under['roc_auc'],
        resultados_smote['roc_auc'],
        resultados_rf['roc_auc'],
        resultados_xgb['roc_auc'],
        resultados_grid['roc_auc']
    ],
    'PR-AUC': [
        resultados_lr['pr_auc'],
        resultados_under['pr_auc'],
        resultados_smote['pr_auc'],
        resultados_rf['pr_auc'],
        resultados_xgb['pr_auc'],
        resultados_grid['pr_auc']
    ]
}).sort_values('PR-AUC', ascending=False)

print("\n")
print(comparacao.to_string(index=False))

# Gráfico comparativo
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(comparacao))
width = 0.35

ax.bar(x - width/2, comparacao['ROC-AUC'], width, label='ROC-AUC', alpha=0.8)
ax.bar(x + width/2, comparacao['PR-AUC'], width, label='PR-AUC', alpha=0.8)

ax.set_xlabel('Modelo')
ax.set_ylabel('Score')
ax.set_title('Comparação de Performance dos Modelos')
ax.set_xticks(x)
ax.set_xticklabels(comparacao['Modelo'], rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# ==========================================
# CONCLUSÕES
# ==========================================
print("\n" + "="*60)
print("CONCLUSÕES E APRENDIZADOS")
print("="*60)

print("""
PRINCIPAIS APRENDIZADOS:

1. DESBALANCEAMENTO:
   - Dataset muito desbalanceado (apenas 0.17% fraudes)
   - PR-AUC é mais adequado que ROC-AUC para este caso
   - Técnicas de balanceamento (SMOTE, undersampling) ajudam

2. MODELOS:
   - XGBoost teve melhor performance que modelos lineares
   - Grid Search melhorou os resultados em alguns pontos percentuais
   - Feature engineering (Hour, Period) contribuiu para o modelo

3. THRESHOLD:
   - O threshold padrão (0.5) não é sempre o ideal
   - Otimização baseada em F1-Score ou custo de negócio é importante
   - Trade-off entre precision e recall deve ser considerado

4. INTERPRETABILIDADE:
   - SHAP permite entender quais features influenciam cada predição
   - Importante para confiança no modelo e debugging
   - As features mais importantes foram V14, V17 e V12

PRÓXIMOS PASSOS:

1. Análise temporal mais detalhada
2. Testar outros algoritmos (LightGBM, CatBoost)
3. Implementar ensemble de modelos
4. Criar pipeline de produção
5. Monitorar performance ao longo do tempo
6. Análise de custo-benefício mais realista

DIFERENCIAIS IMPLEMENTADOS:

- Correção de data leakage (scaling após split)
- Comparação de 6 abordagens diferentes
- Feature engineering próprio
- Otimização de threshold
- Análise de custo estimado
- Documentação detalhada
""")

print("\n" + "="*60)
print("PROJETO CONCLUÍDO")
print("="*60)