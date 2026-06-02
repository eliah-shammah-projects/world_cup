# Simulador da Copa do Mundo 2026

## Visão Geral

Aplicação web para simular a Copa do Mundo FIFA 2026, permitindo ao usuário inserir resultados dos jogos, acompanhar a fase de grupos, gerar o chaveamento do mata-mata automaticamente e acessar informações completas sobre seleções e estádios.

---

## Formato da Copa 2026

- **48 seleções** divididas em **12 grupos de 4 times**
- Fase de grupos: cada time joga 3 partidas
- Avançam: os 2 primeiros de cada grupo (24 times) + os 8 melhores terceiros colocados (8 times)
- Total de 32 times no mata-mata
- Mata-mata:
  - 16 avos de final (Round of 32) — 16 jogos
  - Oitavas de final (Round of 16) — 8 jogos
  - Quartas de final — 4 jogos
  - Semifinais — 2 jogos
  - Disputa do 3º lugar — 1 jogo
  - Final — 1 jogo

---

## Funcionalidades

### 1. Fase de Grupos
- Exibir os 12 grupos com as seleções
- Usuário insere o placar de cada jogo
- Tabela de classificação atualizada automaticamente com:
  - Pontos, Jogos, Vitórias, Empates, Derrotas, Gols Pró, Gols Contra, Saldo de Gols
- Critérios de desempate seguindo as regras da FIFA:
  1. Pontos
  2. Saldo de gols (geral)
  3. Gols marcados (geral)
  4. Pontos nos confrontos diretos
  5. Saldo de gols nos confrontos diretos
  6. Gols marcados nos confrontos diretos
  7. Cartões (amarelo = 1pt, vermelho direto = 3pt, amarelo+vermelho = 3pt)
  8. Sorteio

### 2. Seleção dos 8 Melhores Terceiros
- Após encerrar a fase de grupos, o sistema identifica automaticamente os 8 melhores terceiros colocados
- Critérios de desempate entre terceiros: mesmos critérios da FIFA para terceiros
- Exibir tabela comparativa dos 12 terceiros colocados destacando os 8 classificados

### 3. Mata-Mata (Chaveamento)
- Geração automática do chaveamento a partir dos classificados, seguindo o mapa oficial da FIFA 2026
- O usuário insere o resultado de cada jogo do mata-mata
- Em caso de empate: vai para prorrogação e pênaltis (usuário informa o vencedor)
- Bracket visual mostrando toda a chave até a final
- Campeão destacado ao final

### 4. Informações das Seleções
Para cada uma das 48 seleções:
- **Nome** (em português e inglês), **bandeira**, **confederação** (UEFA, CONMEBOL, CONCACAF, AFC, CAF, OFC)
- **Técnico atual** (nome e nacionalidade)
- **Convocação** (quando disponível — alguns ainda não foram divulgados)
- **Histórico em Copas:**
  - Quantas Copas participou
  - Quantas Copas venceu e em quais anos
  - Melhor classificação alcançada

### 5. Estádios
Para cada estádio sede da Copa 2026:
- **Nome** e **cidade/estado/país** (EUA, Canadá, México)
- **Capacidade** total
- **Foto** (imagem de destaque)
- **Jogos que serão realizados** no estádio (incluindo fases)

---

## Tecnologias Utilizadas (Stack Definitiva)

| Camada | Escolha |
|--------|---------|
| Backend | Python + Flask |
| Frontend | Jinja2 (templates HTML) + CSS puro |
| Dados | Arquivos Python estáticos (`data.py`, `teams_data.py`) — sem banco de dados |
| Estado | Em memória (dicionários Python — reinicia com o servidor) |

> **Stack definida:** Flask + Jinja2 com dados estáticos em Python. Sem banco de dados por enquanto.

---

## Estrutura de Dados Principais

```
Seleção
├── id, nome, nome_en, bandeira
├── confederacao
├── tecnico { nome, nacionalidade }
├── convocacao [ { nome, posicao, clube } ]
└── historico { participacoes, titulos, anos_titulo[], melhor_classificacao }

Grupo
├── letra (A–L)
└── selecoes[] → ref Seleção

Jogo
├── grupo / fase
├── time1, time2
├── gols_time1, gols_time2
├── data, estadio
└── status (agendado | encerrado)

Estádio
├── nome, cidade, pais
├── capacidade
├── foto_url
└── jogos[] → ref Jogo
```

---

## Estádios da Copa 2026

### Estados Unidos (11 estádios)
- MetLife Stadium — East Rutherford, NJ (82.500)
- AT&T Stadium — Arlington, TX (80.000)
- SoFi Stadium — Inglewood, CA (70.240)
- Levi's Stadium — Santa Clara, CA (68.500)
- Arrowhead Stadium — Kansas City, MO (76.416)
- Rose Bowl — Pasadena, CA (88.565)
- Lincoln Financial Field — Philadelphia, PA (69.796)
- Gillette Stadium — Foxborough, MA (65.878)
- Hard Rock Stadium — Miami Gardens, FL (64.767)
- Mercedes-Benz Stadium — Atlanta, GA (71.000)
- Lumen Field — Seattle, WA (68.740)

### Canadá (2 estádios)
- BC Place — Vancouver, BC (54.500)
- BMO Field — Toronto, ON (45.000)

### México (3 estádios)
- Estadio Azteca — Cidade do México (87.523)
- Estadio BBVA — Monterrey (53.500)
- Estadio Akron — Guadalajara (49.850)

---

## Os 12 Grupos — Chave Oficial (sorteio realizado em 05/12/2025)

| Grupo | Time 1 (cabeça) | Time 2 | Time 3 | Time 4 |
|-------|-----------------|--------|--------|--------|
| **A** | México | África do Sul | Coreia do Sul | República Tcheca |
| **B** | Canadá | Suíça | Qatar | Bósnia e Herzegovina |
| **C** | Brasil | Marrocos | Haiti | Escócia |
| **D** | Estados Unidos | Paraguai | Austrália | Turquia |
| **E** | Alemanha | Curaçao | Costa do Marfim | Equador |
| **F** | Países Baixos | Japão | Tunísia | Suécia |
| **G** | Bélgica | Egito | Irã | Nova Zelândia |
| **H** | Espanha | Cabo Verde | Arábia Saudita | Uruguai |
| **I** | França | Senegal | Noruega | Iraque |
| **J** | Argentina | Argélia | Áustria | Jordânia |
| **K** | Portugal | Uzbequistão | Colômbia | Congo DR |
| **L** | Inglaterra | Croácia | Gana | Panamá |

---

## Chaveamento dos 16-avos de Final (Round of 32)

O chaveamento é **pré-determinado pela FIFA**. Os 16 confrontos fixos são:

| Jogo | Confronto | Observação |
|------|-----------|------------|
| R32-01 | **1º E** vs **3º (A/B/C/D/F)** | 3º variável |
| R32-02 | **1º I** vs **3º (C/D/F/G/H)** | 3º variável |
| R32-03 | **2º A** vs **2º B** | fixo |
| R32-04 | **1º F** vs **2º C** | fixo |
| R32-05 | **2º K** vs **2º L** | fixo |
| R32-06 | **1º H** vs **2º J** | fixo |
| R32-07 | **1º D** vs **3º (B/E/F/I/J)** | 3º variável |
| R32-08 | **1º G** vs **3º (A/E/H/I/J)** | 3º variável |
| R32-09 | **1º C** vs **2º F** | fixo |
| R32-10 | **2º E** vs **2º I** | fixo |
| R32-11 | **1º A** vs **3º (C/E/F/H/I)** | 3º variável |
| R32-12 | **1º L** vs **3º (E/H/I/J/K)** | 3º variável |
| R32-13 | **1º J** vs **2º H** | fixo |
| R32-14 | **2º D** vs **2º G** | fixo |
| R32-15 | **1º B** vs **3º (E/F/G/I/J)** | 3º variável |
| R32-16 | **1º K** vs **3º (D/E/I/J/L)** | 3º variável |

### Regra dos 8 Melhores Terceiros

Os 12 grupos geram 12 terceiros colocados. Apenas os **8 melhores** avançam.  
Ranking entre os 12 terceiros usa os **mesmos critérios de desempate da fase de grupos** (pontos → saldo → gols marcados → cartões → sorteio).

Os slots marcados como "3º variável" acima recebem os terceiros conforme tabela lookup da FIFA (Anexo C do regulamento — 495 combinações possíveis). A combinação exata depende de quais 8 grupos produziram os terceiros classificados.

**Implementação:** criar uma tabela de lookup com as 495 combinações que mapeia `{conjunto de 8 grupos com terceiros}` → `{qual grupo vai para qual slot R32}`.

---

## Critérios de Desempate (Fase de Grupos) — Regras FIFA 2026

1. Pontos obtidos
2. Saldo de gols geral
3. Gols marcados geral
4. Pontos nos confrontos diretos entre os empatados
5. Saldo de gols nos confrontos diretos
6. Gols marcados nos confrontos diretos
7. Pontuação disciplinar (amarelo = 1, vermelho direto = 3, amarelo+vermelho = 3)
8. Ranking FIFA (posição no ranking da FIFA)
9. Sorteio

---

## As 48 Seleções por Confederação

| Confederação | Vagas | Seleções |
|---|---|---|
| UEFA (Europa) | 16 | Alemanha, Inglaterra, Espanha, França, Portugal, Países Baixos, Bélgica, Croácia, Suíça, Noruega, Suécia, Áustria, Turquia, Escócia, República Tcheca, Uzbequistão |
| CAF (África) | 9 | Marrocos, Senegal, Egito, Costa do Marfim, Tunísia, Gana, África do Sul, Argélia, Congo DR, Cabo Verde |
| AFC (Ásia) | 8 | Coreia do Sul, Japão, Arábia Saudita, Qatar, Austrália, Iraque, Jordânia, Irã |
| CONCACAF | 6+3 sedes | EUA, Canadá, México (sedes), Panamá, Haiti, Curaçao, Bósnia e Herzegovina* |
| CONMEBOL | 6 | Brasil, Argentina, Uruguai, Equador, Colômbia, Paraguai |
| OFC (Oceania) | 1 | Nova Zelândia |

*Bósnia classificou via repescagem inter-confederações

---

## Roadmap de Desenvolvimento

### Fase 1 — Base (MVP) ✅ CONCLUÍDA
- [x] Setup do projeto Flask + Jinja2 (`app.py`, `requirements.txt`)
- [x] Dados das 48 seleções e 12 grupos (`data.py`, `teams_data.py`)
- [x] Inserção de resultados da fase de grupos (API `/api/resultado`)
- [x] Tabela de classificação automática (`logic.py → classificar_grupo()`)
- [x] Critérios de desempate por H2H (confrontos diretos)
- [x] Seleção dos 8 melhores terceiros (`logic.py → melhores_terceiros()`)
- [x] Reset geral (`/api/reset`)

### Fase 2 — Mata-Mata ⚠️ PARCIALMENTE CONCLUÍDA
- [x] Geração do chaveamento R32 com atribuição de terceiros (`gerar_bracket_r32_completo()`)
- [x] API para salvar resultados do mata-mata (`/api/mata-mata`) com suporte a pênaltis
- [x] Template base do mata-mata (`templates/mata_mata.html`)
- [ ] **PENDENTE: Progressão automática R32 → R16 → Quartas → Semis → Final**
- [ ] **PENDENTE: Bracket visual completo (todas as fases em cascata)**
- [ ] **PENDENTE: Revelação do campeão ao final**
- [ ] **PENDENTE: Jogo do 3º lugar**

### Fase 3 — Informações ⚠️ PARCIALMENTE CONCLUÍDA
- [x] Página individual de cada seleção (`/selecao/<code>`, `templates/selecao.html`)
- [x] Dados históricos e técnicos das seleções (`teams_data.py → TEAMS_INFO`)
- [x] Página de estádios (`/estadios`, `templates/estadios.html`)
- [ ] **PENDENTE: Verificar se convocações estão preenchidas em `teams_data.py`**
- [ ] **PENDENTE: Fotos reais dos estádios**

### Fase 4 — Polimento ❌ NÃO INICIADA
- [ ] Design responsivo (mobile)
- [ ] Animações e transições
- [ ] Modo escuro
- [ ] Compartilhar simulação

---

## Estado Atual — Resumo Executivo (atualizado em 26/05/2026)

```
FASE 1 (Base/MVP)       ████████████████ 100% ✅
FASE 2 (Mata-Mata)      ████████░░░░░░░░  50% ⚠️
FASE 3 (Informações)    ██████████░░░░░░  65% ⚠️
FASE 4 (Polimento)      ░░░░░░░░░░░░░░░░   0% ❌
```

### Design System
O site foi migrado para **tema Panini Retrô** (álbum de figurinhas Copa 78/82).
- `static/globals.css` — design system completo (tokens, componentes, overrides por página)
- `static/style.css` — estilos antigos (ainda carrega depois do globals.css; limpeza pendente)
- `preview.html` — página estática para validar componentes Panini (abrir direto no browser)
- Stack de fontes: **Playfair Display** (display/títulos) + **Libre Baskerville** (corpo)
- Paleta: papel bege `#f2e8cf`, laranja Panini `#c94a1a`, azul royal `#1a4a8a`, tinta `#2a1a08`
- Wrapper `.page-panini-bg` aplicado em grupos.html, selecao.html e mata_mata.html

### Próxima tarefa prioritária — Ajustes de Design Pendentes

Os itens abaixo foram identificados pelo usuário e devem ser feitos na próxima sessão:

#### HOME (index.html)
1. **Hero — slideshow de fotos** — o usuário vai fornecer as imagens. Implementar carrossel/slideshow automático no fundo do hero com transição suave entre fotos (overlay bege por cima para manter legibilidade do texto). Aguardar o usuário enviar as fotos antes de implementar.
2. **Badge do grupo** (`.group-badge` — a letra A, B, C…) — cor e tipografia ruins; redesenhar para combinar melhor com o card
3. **Bolinhas das confederações no hero** — os 6 pontos coloridos são estáticos mas parecem interativos; remover ou deixar mais discretos/decorativos
4. **Botão "Fase de Grupos"** — fundo branco sem cor e emoji inadequado; aplicar `.btn-retro` corretamente
5. **Estádios — modal ao clicar** — ao clicar num card de estádio, abrir overlay/modal com foto grande, nome, capacidade e jogos

#### SIMULADOR (grupos.html)
6. **Botões "Limpar resultados" e "Ver Mata-Mata"** — melhorar visual (tamanho, espaçamento, hierarquia)

#### MATA-MATA (mata_mata.html)
- **Jogo do 3º lugar** — está fora de lugar (jogado no rodapé ao lado do campeão). Reposicionar de forma lógica no layout do bracket
- **Labels do site** — toda a interface tem labels no estilo "vibe coding" (genérico, sem personalidade). Revisar tipografia, hierarquia e estilo dos labels em todas as páginas para elevar o nível de design

#### GERAL — Bandeiras
13. **Bandeiras** — substituir as bandeiras atuais (flagcdn.com) por símbolos/logos das confederações ou por imagens de bandeiras de melhor qualidade. Avaliar opções: flag-icons (SVG via CDN), twemoji flags, ou imagens locais de alta resolução.

#### PÁGINA DE SELEÇÃO (selecao.html) ⭐ PRIORIDADE ALTA
7. **UX/UI geral da página** — redesenho completo solicitado pelo usuário (02/06/2026)
8. **Cores do tema por seleção** — cores muito ruins; o card hero e os cards de info devem usar melhor a cor da confederação
9. **Labels (Técnico, Histórico, etc.)** — tipografia e estilo dos labels completamente a melhorar
10. **Botão "← Voltar às seleções"** no rodapé da página — melhorar
11. **Bloco Histórico** — tamanho/layout ruim; redesenhar mais moderno e com mais destaque visual
12. **Bloco "Sobre"** — fazer de jeito mais moderno e dinâmico (ex: expandir/colapsar, ícone, destaque visual)

### Arquivos principais
| Arquivo | Responsabilidade |
|---------|-----------------|
| `app.py` | Rotas Flask e lógica de API |
| `logic.py` | Classificação, desempate, geração do bracket |
| `data.py` | Grupos, jogos da fase de grupos, R32_BRACKET, SLOTS_TERCEIROS |
| `teams_data.py` | Info das 48 seleções + estádios |
| `templates/grupos.html` | Fase de grupos com tabelas e placares |
| `templates/mata_mata.html` | Bracket do mata-mata (incompleto) |
| `templates/selecao.html` | Página individual de cada seleção |
| `templates/estadios.html` | Lista de estádios |
| `static/style.css` | Estilos globais |

---

## Fase 5 — Infraestrutura & IA (PLANEJADA)

### DevOps & Deploy
- [ ] **Testes** — escrever testes unitários e de integração (pytest) para `logic.py`, APIs e rotas Flask
- [ ] **Docker** — criar `Dockerfile` e `docker-compose.yml` para containerizar a aplicação
- [ ] **GitHub** — repositório com boas práticas (`.gitignore`, `README.md`, branches)
- [ ] **GitHub Actions** — CI/CD: rodar testes automaticamente em cada push; build e push da imagem Docker
- [ ] **Docker Hub** — publicar imagem da aplicação no Docker Hub
- [ ] **AWS EC2** — fazer deploy da imagem Docker em uma instância EC2; configurar nginx como proxy reverso

### Feature de IA
- [ ] **Feature AI** — a definir com o usuário. Possibilidades: predição de resultados com ML, análise de desempenho das seleções, chatbot de Copa, geração de narrativas dos jogos com LLM (Claude API)

---

## Perguntas em Aberto

1. ~~**Linguagem/stack definitiva?**~~ → **Resolvido:** Flask + Jinja2
2. ~~**Dados fixos em JSON ou editáveis?**~~ → **Resolvido:** dados estáticos em Python
3. **Permitir múltiplas simulações salvas** (ex: simular cenários diferentes) ou apenas uma por vez? *(estado atual: apenas uma, em memória)*
4. **As fotos dos estádios serão hospedadas localmente ou links externos?** *(pendente)*
5. **Internacionalização?** Somente português ou também inglês? *(pendente)*
6. **Persistência dos dados?** Hoje o estado reinicia com o servidor — adicionar banco (SQLite) ou salvar em arquivo JSON?
