from flask import Flask, render_template, request, jsonify, redirect, url_for
from data import GRUPOS, JOGOS, TIMES
from teams_data import TEAMS_INFO, ESTADIOS
import logic

app = Flask(__name__)

# Estado em memória — reiniciado quando o servidor reinicia
resultados = {}   # fase de grupos: {jogo_id: {gols1, gols2}}
resultados_mk = {}  # mata-mata: {jogo_id: {gols1, gols2, pen_vencedor?}}


@app.route('/')
def index():
    total = len(JOGOS)
    done  = sum(1 for j in JOGOS if j['id'] in resultados)
    return render_template('index.html',
                           grupos=GRUPOS, times=TIMES,
                           teams_info=TEAMS_INFO, estadios=ESTADIOS,
                           done=done, total=total)


@app.route('/selecao/<code>')
def selecao(code):
    if code not in TIMES:
        return redirect(url_for('index'))
    info = TEAMS_INFO.get(code, {})
    grupo = next((g for g, ts in GRUPOS.items() if code in ts), None)
    jogos_time = [j for j in JOGOS if j['time1'] == code or j['time2'] == code]
    tabela = logic.classificar_grupo(grupo, resultados) if grupo else []
    return render_template('selecao.html',
                           code=code, nome=TIMES[code], info=info,
                           grupo=grupo, jogos=jogos_time,
                           times=TIMES, resultados=resultados, tabela=tabela,
                           teams_info=TEAMS_INFO)


@app.route('/grupos')
def grupos():
    tabelas = {g: logic.classificar_grupo(g, resultados) for g in GRUPOS}
    jogos_por_grupo = {g: [j for j in JOGOS if j['grupo'] == g] for g in GRUPOS}
    return render_template('grupos.html',
                           grupos=GRUPOS, tabelas=tabelas,
                           jogos_por_grupo=jogos_por_grupo,
                           times=TIMES, resultados=resultados,
                           teams_info=TEAMS_INFO)


@app.route('/mata-mata')
def mata_mata():
    total = len(JOGOS)
    done = sum(1 for j in JOGOS if j['id'] in resultados)
    completo = done == total
    bracket = logic.gerar_bracket_r32_completo(resultados) if completo else None
    if bracket:
        for j in bracket:
            j['winner'] = logic.get_vencedor_mk(j['id'], j['time1_code'], j['time2_code'], resultados_mk)
    fases = logic.gerar_fases_mata_mata(bracket, resultados_mk) if bracket else None
    return render_template('mata_mata.html',
                           completo=completo, done=done, total=total,
                           bracket=bracket, fases=fases,
                           resultados_mk=resultados_mk,
                           times=TIMES, teams_info=TEAMS_INFO)



# ── API ──────────────────────────────────────────────────────────────────────

@app.route('/api/resultado', methods=['POST'])
def salvar_resultado():
    data = request.get_json(force=True)
    jid = data.get('jogo_id', '')
    try:
        g1 = int(data['gols1'])
        g2 = int(data['gols2'])
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'Placar inválido'}), 400
    if g1 < 0 or g2 < 0:
        return jsonify({'error': 'Gols não podem ser negativos'}), 400

    jogo = next((j for j in JOGOS if j['id'] == jid), None)
    if not jogo:
        return jsonify({'error': 'Jogo não encontrado'}), 404

    resultados[jid] = {'gols1': g1, 'gols2': g2}
    grupo = jogo['grupo']
    tabela = logic.classificar_grupo(grupo, resultados)
    done = sum(1 for j in JOGOS if j['id'] in resultados)
    return jsonify({'ok': True, 'grupo': grupo, 'tabela': tabela,
                    'done': done, 'total': len(JOGOS)})


@app.route('/api/resultado/<jid>', methods=['DELETE'])
def limpar_resultado(jid):
    resultados.pop(jid, None)
    jogo = next((j for j in JOGOS if j['id'] == jid), None)
    grupo = jogo['grupo'] if jogo else None
    tabela = logic.classificar_grupo(grupo, resultados) if grupo else []
    return jsonify({'ok': True, 'tabela': tabela})


@app.route('/api/reset', methods=['POST'])
def reset():
    resultados.clear()
    resultados_mk.clear()
    return jsonify({'ok': True})


@app.route('/api/terceiros')
def api_terceiros():
    return jsonify(logic.melhores_terceiros(resultados))


@app.route('/api/mata-mata', methods=['POST'])
def salvar_mata():
    data = request.get_json(force=True)
    jid = data.get('jogo_id', '')
    try:
        g1 = int(data['gols1'])
        g2 = int(data['gols2'])
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'Placar inválido'}), 400
    res = {'gols1': g1, 'gols2': g2}
    if g1 == g2:
        pen = data.get('pen_vencedor', '')
        if not pen:
            return jsonify({'error': 'Informe o vencedor nos pênaltis'}), 400
        res['pen_vencedor'] = pen
    resultados_mk[jid] = res
    return jsonify({'ok': True})


@app.route('/vitoria/<code>')
def vitoria(code):
    if code not in TIMES:
        return redirect(url_for('index'))
    info = TEAMS_INFO.get(code, {})
    return render_template('vitoria.html',
                           code=code, nome=TIMES[code], info=info)


if __name__ == '__main__':
    app.run(debug=True, port=5010)
