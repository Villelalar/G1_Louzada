# 🛡️ Cibersegurança no Brasil (2015–2024)

Projeto G1 — Linguagem de Programação: Análise e Visualização de Dados com Python.

**Aluna:** Larissa Villela dos Santos  
**Professor:** Alexandre Neves Louzada  
**Dashboard:** https://g1louzada-4jctawkdqhqnkfufwzq6ht.streamlit.app/ · **Página:** https://villelalar.github.io/G1_Louzada/

## Problema
Onde, como e com que custo ocorrem incidentes cibernéticos no Brasil, e quais vulnerabilidades mais pesam?

## Base de dados
`dados/simulacao_ciberseguranca_brasil.csv` — 4.440 registros mensais (2015–2024), 20 UFs, 5 setores, 5 tipos de ataque (base simulada).

## Tecnologias
Python · Pandas · NumPy · Matplotlib · Seaborn · Streamlit · SQLAlchemy + SQLite · GitHub

## Funcionalidades
- **Intermediárias:** filtros múltiplos (período, região, UF, setor), KPIs dinâmicos, análise temporal, dashboard organizado em seções, visualizações comparativas, tabela resumo por setor.
- **Avançadas:** persistência em SQLite via SQLAlchemy (notebook, seção 4.1), correlação estatística (Pearson), séries temporais (média móvel 12 meses e variação anual).

## Estrutura
```
projeto-g1/
├── app.py              # dashboard Streamlit
├── requirements.txt
├── README.md
├── index.html          # página do projeto (GitHub Pages)
├── dados/              # CSV original
├── database/           # SQLite gerado pelo notebook (ignorado no git)
├── notebooks/          # análise completa (.ipynb)
└── imagens/            # gráficos usados na página
```

## Como executar
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicação
1. **GitHub:** suba o repositório. 2. **GitHub Pages:** Settings → Pages → branch `main`, pasta `/ (root)`. 3. **Streamlit Cloud:** share.streamlit.io → New app → selecione o repositório e `app.py`.
