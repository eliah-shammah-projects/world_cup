# Copa do Mundo 2026 — Simulador

Simulador completo da Copa do Mundo FIFA 2026. Insira os resultados dos jogos, acompanhe a classificação em tempo real e gere o chaveamento do mata-mata automaticamente.

## Stack

- **Backend:** Python + Flask
- **Frontend:** Jinja2 + CSS puro (tema Panini Retrô)
- **Dados:** arquivos Python estáticos — sem banco de dados

## Funcionalidades

- 12 grupos com 48 seleções
- Tabela de classificação automática com critérios de desempate FIFA
- Seleção dos 8 melhores terceiros colocados
- Bracket em cascata do mata-mata (R32 → R16 → Quartas → Semis → Final)
- Tela de vitória animada para o campeão
- Páginas individuais das 48 seleções com convocações e histórico
- Informações dos 16 estádios sede

## Como rodar

### Local

```bash
pip install -r requirements.txt
python app.py
```

Acesse: http://127.0.0.1:5010

### Docker

```bash
docker compose up --build
```

Acesse: http://localhost:5010

## Testes

```bash
python -m pytest tests/ -v
```

## Estrutura

```
world_cup/
├── app.py              # Rotas Flask
├── logic.py            # Classificação, desempate, bracket
├── data.py             # Grupos, jogos, R32
├── teams_data.py       # Info das 48 seleções e estádios
├── templates/          # HTML Jinja2
├── static/             # CSS e imagens
├── tests/              # Testes pytest
├── Dockerfile
└── docker-compose.yml
```
