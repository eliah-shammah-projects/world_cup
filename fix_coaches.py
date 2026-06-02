import re

coaches = {
    'MEX': ('Javier Aguirre', 'Mexicana'),
    'AFS': ('Hugo Broos', 'Belga'),
    'COR': ('Hong Myung-bo', 'Sul-coreana'),
    'TCH': ('Miroslav Koubek', 'Tcheca'),
    'CAN': ('Jesse Marsch', 'Americana'),
    'CAT': ('Julen Lopetegui', 'Espanhola'),
    'SUI': ('Murat Yakin', 'Suíça'),
    'BOS': ('Sergej Barbarez', 'Bósnia'),
    'BRA': ('Carlo Ancelotti', 'Italiana'),
    'MAR': ('Mohamed Ouahbi', 'Marroquina'),
    'HAI': ('Sébastien Migné', 'Francesa'),
    'ESC': ('Steve Clarke', 'Escocesa'),
    'EUA': ('Mauricio Pochettino', 'Argentina'),
    'PAR': ('Gustavo Alfaro', 'Argentina'),
    'AUS': ('Tony Popovic', 'Australiana'),
    'TUR': ('Vincenzo Montella', 'Italiana'),
    'ALE': ('Julian Nagelsmann', 'Alemã'),
    'CUR': ('Fred Rutten', 'Holandesa'),
    'CDM': ('Emerse Faé', 'Marfinense'),
    'EQU': ('Sebastián Beccacece', 'Argentina'),
    'HOL': ('Ronald Koeman', 'Holandesa'),
    'JAP': ('Hajime Moriyasu', 'Japonesa'),
    'TUN': ('Sabri Lamouchi', 'Tunisiana'),
    'SUE': ('Graham Potter', 'Inglesa'),
    'BEL': ('Rudi Garcia', 'Francesa'),
    'EGI': ('Hossam Hassan', 'Egípcia'),
    'IRA': ('Amir Ghalenoei', 'Iraniana'),
    'NZE': ('Darren Bazeley', 'Neozelandesa'),
    'ESP': ('Luis de la Fuente', 'Espanhola'),
    'CAB': ('Bubista', 'Portuguesa'),
    'ARS': ('Hervé Renard', 'Francesa'),
    'URU': ('Marcelo Bielsa', 'Argentina'),
    'FRA': ('Didier Deschamps', 'Francesa'),
    'SEN': ('Pape Thiaw', 'Senegalesa'),
    'NOR': ('Ståle Solbakken', 'Norueguesa'),
    'IRQ': ('Graham Arnold', 'Australiana'),
    'ARG': ('Lionel Scaloni', 'Argentina'),
    'AGL': ('Vladimir Petković', 'Bósnia'),
    'AUT': ('Ralf Rangnick', 'Alemã'),
    'JOR': ('Jamal Sellami', 'Tunisiana'),
    'POR': ('Roberto Martínez', 'Espanhola'),
    'UZB': ('Fabio Cannavaro', 'Italiana'),
    'COL': ('Néstor Lorenzo', 'Argentina'),
    'RDC': ('Sébastien Desabre', 'Francesa'),
    'ING': ('Thomas Tuchel', 'Alemã'),
    'CRO': ('Zlatko Dalić', 'Croata'),
    'GAN': ('Carlos Queiroz', 'Portuguesa'),
    'PAN': ('Thomas Christiansen', 'Dinamarquesa'),
}

with open('teams_data.py', encoding='utf-8') as f:
    lines = f.readlines()

current_team = None
result = []
updated = set()

for line in lines:
    # Detecta linha de código de seleção: '   'ABC': {'
    m = re.match(r"\s+'([A-Z]{2,3})':\s*\{", line)
    if m:
        current_team = m.group(1)

    # Se estamos numa seleção conhecida, procura linha do técnico
    if current_team in coaches:
        tm = re.match(r"(\s+'tecnico':\s*\{)'nome':\s*'[^']*',\s*'nac':\s*'[^']*'(\},?)", line)
        if tm:
            nome, nac = coaches[current_team]
            line = f"{tm.group(1)}'nome': '{nome}', 'nac': '{nac}'{tm.group(2)}\n"
            updated.add(current_team)

    result.append(line)

with open('teams_data.py', 'w', encoding='utf-8') as f:
    f.writelines(result)

for code, (nome, _) in coaches.items():
    if code in updated:
        print(f"✅ {code}: {nome}")
    else:
        print(f"⚠️  {code}: não encontrado")

print('\nPronto!')
