TIMES = {
    'MEX': 'México',        'AFS': 'África do Sul',  'COR': 'Coreia do Sul', 'TCH': 'Rep. Tcheca',
    'CAN': 'Canadá',        'BOS': 'Bósnia',         'CAT': 'Catar',         'SUI': 'Suíça',
    'BRA': 'Brasil',        'MAR': 'Marrocos',        'HAI': 'Haiti',         'ESC': 'Escócia',
    'EUA': 'Estados Unidos','PAR': 'Paraguai',        'AUS': 'Austrália',     'TUR': 'Turquia',
    'ALE': 'Alemanha',      'CUR': 'Curaçao',         'CDM': 'Costa do Marfim','EQU': 'Equador',
    'HOL': 'Holanda',       'JAP': 'Japão',           'SUE': 'Suécia',        'TUN': 'Tunísia',
    'BEL': 'Bélgica',       'EGI': 'Egito',           'IRA': 'Irã',           'NZE': 'Nova Zelândia',
    'ESP': 'Espanha',       'CAB': 'Cabo Verde',       'ARS': 'Arábia Saudita','URU': 'Uruguai',
    'FRA': 'França',        'SEN': 'Senegal',          'IRQ': 'Iraque',        'NOR': 'Noruega',
    'ARG': 'Argentina',     'AGL': 'Argélia',          'AUT': 'Áustria',       'JOR': 'Jordânia',
    'POR': 'Portugal',      'RDC': 'Congo DR',         'UZB': 'Uzbequistão',   'COL': 'Colômbia',
    'ING': 'Inglaterra',    'CRO': 'Croácia',          'PAN': 'Panamá',        'GAN': 'Gana',
}

# Ordem dentro do grupo: T1, T2 (jogam na rodada 1 jogo 1),
#                        T3, T4 (jogam na rodada 1 jogo 2)
# Rodada 1: T1xT2, T3xT4 | Rodada 2: T1xT3, T2xT4 | Rodada 3: T1xT4, T2xT3
GRUPOS = {
    'A': ['MEX', 'AFS', 'COR', 'TCH'],
    'B': ['CAN', 'BOS', 'CAT', 'SUI'],
    'C': ['BRA', 'MAR', 'HAI', 'ESC'],
    'D': ['EUA', 'PAR', 'AUS', 'TUR'],
    'E': ['ALE', 'CUR', 'CDM', 'EQU'],
    'F': ['HOL', 'JAP', 'SUE', 'TUN'],
    'G': ['BEL', 'EGI', 'IRA', 'NZE'],
    'H': ['ESP', 'CAB', 'ARS', 'URU'],
    'I': ['FRA', 'SEN', 'IRQ', 'NOR'],
    'J': ['ARG', 'AGL', 'AUT', 'JOR'],
    'K': ['POR', 'RDC', 'UZB', 'COL'],
    'L': ['ING', 'CRO', 'PAN', 'GAN'],
}

# Dados da 1ª rodada (datas e estádios reais)
_R1 = {
    'A': [('11/06', '16:00', 'Azteca'),       ('11/06', '23:00', 'Akron')],
    'B': [('12/06', '16:00', 'Toronto'),      ('13/06', '16:00', 'Santa Clara')],
    'C': [('13/06', '19:00', 'Nova Jersey'),  ('13/06', '22:00', 'Boston')],
    'D': [('12/06', '22:00', 'Los Angeles'),  ('14/06', '01:00', 'Vancouver')],
    'E': [('14/06', '14:00', 'Houston'),      ('14/06', '20:00', 'Filadélfia')],
    'F': [('14/06', '17:00', 'Dallas'),       ('14/06', '23:00', 'Monterrey')],
    'G': [('15/06', '16:00', 'Seattle'),      ('15/06', '22:00', 'Los Angeles')],
    'H': [('15/06', '13:00', 'Atlanta'),      ('15/06', '19:00', 'Miami')],
    'I': [('16/06', '16:00', 'Nova Jersey'),  ('16/06', '19:00', 'Boston')],
    'J': [('16/06', '22:00', 'Kansas City'),  ('17/06', '01:00', 'Santa Clara')],
    'K': [('17/06', '14:00', 'Houston'),      ('17/06', '23:00', 'Azteca')],
    'L': [('17/06', '17:00', 'Dallas'),       ('17/06', '20:00', 'Toronto')],
}


def _gerar_jogos():
    jogos = []
    for g, times in GRUPOS.items():
        t1, t2, t3, t4 = times
        r1 = _R1[g]
        rodadas = [
            (1, t1, t2, r1[0][0], r1[0][1], r1[0][2]),
            (1, t3, t4, r1[1][0], r1[1][1], r1[1][2]),
            (2, t1, t3, '-', '-', '-'),
            (2, t2, t4, '-', '-', '-'),
            (3, t1, t4, '-', '-', '-'),
            (3, t2, t3, '-', '-', '-'),
        ]
        for i, (rod, ta, tb, data, hora, est) in enumerate(rodadas, 1):
            jogos.append({
                'id':      f'{g}{i}',
                'grupo':   g,
                'rodada':  rod,
                'time1':   ta,
                'time2':   tb,
                'data':    data,
                'horario': hora,
                'estadio': est,
            })
    return jogos


JOGOS = _gerar_jogos()

# Chaveamento fixo dos 16-avos (bracket pré-definido pela FIFA)
# Slots com "3X..." indicam que um terceiro colocado ocupa essa vaga
# A atribuição exata dos terceiros segue o Anexo C do regulamento FIFA
R32_BRACKET = [
    {'id': 'R32-01', 'time1': '1E',  'time2': '3ABCDF'},
    {'id': 'R32-02', 'time1': '1I',  'time2': '3CDFGH'},
    {'id': 'R32-03', 'time1': '2A',  'time2': '2B'},
    {'id': 'R32-04', 'time1': '1F',  'time2': '2C'},
    {'id': 'R32-05', 'time1': '2K',  'time2': '2L'},
    {'id': 'R32-06', 'time1': '1H',  'time2': '2J'},
    {'id': 'R32-07', 'time1': '1D',  'time2': '3BEFIJ'},
    {'id': 'R32-08', 'time1': '1G',  'time2': '3AEHIJ'},
    {'id': 'R32-09', 'time1': '1C',  'time2': '2F'},
    {'id': 'R32-10', 'time1': '2E',  'time2': '2I'},
    {'id': 'R32-11', 'time1': '1A',  'time2': '3CEFHI'},
    {'id': 'R32-12', 'time1': '1L',  'time2': '3EHIJK'},
    {'id': 'R32-13', 'time1': '1J',  'time2': '2H'},
    {'id': 'R32-14', 'time1': '2D',  'time2': '2G'},
    {'id': 'R32-15', 'time1': '1B',  'time2': '3EFGIJ'},
    {'id': 'R32-16', 'time1': '1K',  'time2': '3DEIJL'},
]

# Slots que recebem terceiros e quais grupos são válidos para cada slot
SLOTS_TERCEIROS = {
    'R32-01': set('ABCDF'),
    'R32-02': set('CDFGH'),
    'R32-07': set('BEFIJ'),
    'R32-08': set('AEHIJ'),
    'R32-11': set('CEFHI'),
    'R32-12': set('EHIJK'),
    'R32-15': set('EFGIJ'),
    'R32-16': set('DEIJL'),
}
