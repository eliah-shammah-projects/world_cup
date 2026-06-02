from data import GRUPOS, JOGOS, SLOTS_TERCEIROS, R32_BRACKET


def classificar_grupo(grupo, resultados):
    times = GRUPOS[grupo]
    jogos = [j for j in JOGOS if j['grupo'] == grupo]

    stats = {t: {
        'time': t, 'pts': 0, 'j': 0, 'v': 0, 'e': 0, 'd': 0,
        'gp': 0, 'gc': 0, 'sg': 0
    } for t in times}

    for j in jogos:
        if j['id'] not in resultados:
            continue
        r = resultados[j['id']]
        g1, g2 = int(r['gols1']), int(r['gols2'])
        t1, t2 = j['time1'], j['time2']

        for t, gf, ga in [(t1, g1, g2), (t2, g2, g1)]:
            stats[t]['j'] += 1
            stats[t]['gp'] += gf
            stats[t]['gc'] += ga

        if g1 > g2:
            stats[t1]['pts'] += 3; stats[t1]['v'] += 1; stats[t2]['d'] += 1
        elif g1 < g2:
            stats[t2]['pts'] += 3; stats[t2]['v'] += 1; stats[t1]['d'] += 1
        else:
            stats[t1]['pts'] += 1; stats[t1]['e'] += 1
            stats[t2]['pts'] += 1; stats[t2]['e'] += 1

    for s in stats.values():
        s['sg'] = s['gp'] - s['gc']

    lista = list(stats.values())
    return _resolver_desempate(lista, jogos, resultados)


def _h2h(times_set, jogos, resultados):
    h = {t: {'pts': 0, 'sg': 0, 'gp': 0} for t in times_set}
    for j in jogos:
        t1, t2 = j['time1'], j['time2']
        if t1 not in times_set or t2 not in times_set:
            continue
        if j['id'] not in resultados:
            continue
        r = resultados[j['id']]
        g1, g2 = int(r['gols1']), int(r['gols2'])
        h[t1]['gp'] += g1; h[t2]['gp'] += g2
        h[t1]['sg'] += g1 - g2; h[t2]['sg'] += g2 - g1
        if g1 > g2:
            h[t1]['pts'] += 3
        elif g1 < g2:
            h[t2]['pts'] += 3
        else:
            h[t1]['pts'] += 1; h[t2]['pts'] += 1
    return h


def _resolver_desempate(lista, jogos, resultados):
    lista.sort(key=lambda x: (-x['pts'], -x['sg'], -x['gp']))
    result = []
    i = 0
    while i < len(lista):
        j = i + 1
        while j < len(lista) and (
            lista[j]['pts'] == lista[i]['pts'] and
            lista[j]['sg'] == lista[i]['sg'] and
            lista[j]['gp'] == lista[i]['gp']
        ):
            j += 1
        grupo = lista[i:j]
        if len(grupo) > 1:
            ts = {t['time'] for t in grupo}
            h = _h2h(ts, jogos, resultados)
            grupo.sort(key=lambda x: (
                -h[x['time']]['pts'],
                -h[x['time']]['sg'],
                -h[x['time']]['gp'],
            ))
        result.extend(grupo)
        i = j
    return result


def melhores_terceiros(resultados):
    terceiros = []
    for g in GRUPOS:
        tab = classificar_grupo(g, resultados)
        if len(tab) >= 3:
            t = dict(tab[2])
            t['grupo'] = g
            terceiros.append(t)
    terceiros.sort(key=lambda x: (-x['pts'], -x['sg'], -x['gp']))
    return terceiros


def gerar_bracket_r32(resultados):
    standings = {g: classificar_grupo(g, resultados) for g in GRUPOS}

    top8 = melhores_terceiros(resultados)[:8]
    grupos_classificados = {t['grupo'] for t in top8}
    terceiro_por_grupo = {t['grupo']: t['time'] for t in top8}

    assignment = _atribuir_terceiros(grupos_classificados)

    bracket = []
    for slot in R32_BRACKET:
        jogo = dict(slot)
        jogo['time1_nome'] = _resolver_slot(slot['time1'], standings)
        jogo['time2_nome'] = _resolver_slot(slot['time2'], standings, assignment, terceiro_por_grupo)
        bracket.append(jogo)
    return bracket


def _resolver_slot(slot_str, standings, assignment=None, terceiro_por_grupo=None):
    if slot_str[0].isdigit():
        pos = int(slot_str[0]) - 1
        grupo = slot_str[1:]
        tab = standings.get(grupo, [])
        return tab[pos]['time'] if len(tab) > pos else '?'
    if slot_str.startswith('3') and assignment:
        slot_id_map = {v: k for k, v in {}}  # unused
        return '?'
    return slot_str


def _atribuir_terceiros(grupos_qualificados):
    slots = list(SLOTS_TERCEIROS.items())
    assignment = {}
    used = set()

    def bt(idx):
        if idx == len(slots):
            return True
        sid, valid = slots[idx]
        for g in sorted(grupos_qualificados):
            if g in valid and g not in used:
                assignment[sid] = g
                used.add(g)
                if bt(idx + 1):
                    return True
                del assignment[sid]
                used.remove(g)
        return False

    bt(0)
    return assignment


def get_vencedor_mk(jid, time1, time2, resultados_mk):
    """Retorna o time vencedor de um jogo do mata-mata, ou None se não jogado."""
    if jid not in resultados_mk or not time1 or not time2:
        return None
    r = resultados_mk[jid]
    g1, g2 = r['gols1'], r['gols2']
    if g1 > g2:
        return time1
    elif g2 > g1:
        return time2
    else:
        return r.get('pen_vencedor')


def get_perdedor_mk(jid, time1, time2, resultados_mk):
    v = get_vencedor_mk(jid, time1, time2, resultados_mk)
    if v is None:
        return None
    return time2 if v == time1 else time1


def gerar_fases_mata_mata(bracket_r32, resultados_mk):
    """Gera R16, QF, SF, 3º lugar e Final a partir do R32."""
    def win(jid, t1, t2):
        return get_vencedor_mk(jid, t1, t2, resultados_mk)

    def lose(jid, t1, t2):
        return get_perdedor_mk(jid, t1, t2, resultados_mk)

    def make(jid, t1, t2):
        v = win(jid, t1, t2) if t1 and t2 else None
        return {'id': jid, 'time1_code': t1, 'time2_code': t2, 'winner': v}

    r32m = {j['id']: j for j in bracket_r32}

    def wr(jid):
        j = r32m[jid]
        return win(jid, j['time1_code'], j['time2_code'])

    # R16 (oitavas)
    r16_def = [
        ('R16-01', 'R32-01', 'R32-02'),
        ('R16-02', 'R32-03', 'R32-04'),
        ('R16-03', 'R32-05', 'R32-06'),
        ('R16-04', 'R32-07', 'R32-08'),
        ('R16-05', 'R32-09', 'R32-10'),
        ('R16-06', 'R32-11', 'R32-12'),
        ('R16-07', 'R32-13', 'R32-14'),
        ('R16-08', 'R32-15', 'R32-16'),
    ]
    r16 = [make(rid, wr(a), wr(b)) for rid, a, b in r16_def]
    r16m = {j['id']: j for j in r16}

    def w16(jid):
        j = r16m[jid]
        return win(jid, j['time1_code'], j['time2_code'])

    # Quartas de final
    qf_def = [
        ('QF-01', 'R16-01', 'R16-02'),
        ('QF-02', 'R16-03', 'R16-04'),
        ('QF-03', 'R16-05', 'R16-06'),
        ('QF-04', 'R16-07', 'R16-08'),
    ]
    qf = [make(rid, w16(a), w16(b)) for rid, a, b in qf_def]
    qfm = {j['id']: j for j in qf}

    def wqf(jid):
        j = qfm[jid]
        return win(jid, j['time1_code'], j['time2_code'])

    def lqf(jid):
        j = qfm[jid]
        return lose(jid, j['time1_code'], j['time2_code'])

    # Semifinais
    sf_def = [
        ('SF-01', 'QF-01', 'QF-02'),
        ('SF-02', 'QF-03', 'QF-04'),
    ]
    sf = [make(rid, wqf(a), wqf(b)) for rid, a, b in sf_def]
    sfm = {j['id']: j for j in sf}

    def wsf(jid):
        j = sfm[jid]
        return win(jid, j['time1_code'], j['time2_code'])

    def lsf(jid):
        j = sfm[jid]
        return lose(jid, j['time1_code'], j['time2_code'])

    terceiro = make('3RD', lsf('SF-01'), lsf('SF-02'))
    final = make('FINAL', wsf('SF-01'), wsf('SF-02'))
    campeao = win('FINAL', final['time1_code'], final['time2_code'])

    return {'r16': r16, 'qf': qf, 'sf': sf,
            'terceiro': terceiro, 'final': final, 'campeao': campeao}


def gerar_bracket_r32_completo(resultados):
    standings = {g: classificar_grupo(g, resultados) for g in GRUPOS}

    top8 = melhores_terceiros(resultados)[:8]
    grupos_classificados = {t['grupo'] for t in top8}
    terceiro_por_grupo = {t['grupo']: t['time'] for t in top8}

    assignment = _atribuir_terceiros(grupos_classificados)

    bracket = []
    for slot in R32_BRACKET:
        jogo = dict(slot)

        t1_str = slot['time1']
        if t1_str[0].isdigit():
            pos = int(t1_str[0]) - 1
            g = t1_str[1:]
            tab = standings.get(g, [])
            jogo['time1_code'] = tab[pos]['time'] if len(tab) > pos else '?'
        else:
            jogo['time1_code'] = t1_str

        t2_str = slot['time2']
        if t2_str.startswith('3'):
            g_atrib = assignment.get(slot['id'])
            jogo['time2_code'] = terceiro_por_grupo.get(g_atrib, '?') if g_atrib else '?'
        elif t2_str[0].isdigit():
            pos = int(t2_str[0]) - 1
            g = t2_str[1:]
            tab = standings.get(g, [])
            jogo['time2_code'] = tab[pos]['time'] if len(tab) > pos else '?'
        else:
            jogo['time2_code'] = t2_str

        bracket.append(jogo)
    return bracket
