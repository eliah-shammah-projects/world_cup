"""Testes de integridade dos dados (data.py e teams_data.py)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data import TIMES, GRUPOS, JOGOS, R32_BRACKET
from teams_data import TEAMS_INFO, ESTADIOS


# ── TIMES ─────────────────────────────────────────────────────────────────────

class TestTimes:

    def test_exatamente_48_selecoes(self):
        assert len(TIMES) == 48

    def test_todos_codigos_sao_strings(self):
        for code in TIMES:
            assert isinstance(code, str)
            assert len(code) >= 2

    def test_todos_nomes_nao_vazios(self):
        for code, nome in TIMES.items():
            assert nome and isinstance(nome, str)


# ── GRUPOS ────────────────────────────────────────────────────────────────────

class TestGrupos:

    def test_exatamente_12_grupos(self):
        assert len(GRUPOS) == 12

    def test_letras_a_ate_l(self):
        assert set(GRUPOS.keys()) == set('ABCDEFGHIJKL')

    def test_cada_grupo_tem_4_times(self):
        for g, times in GRUPOS.items():
            assert len(times) == 4, f'Grupo {g} tem {len(times)} times'

    def test_total_de_times_nos_grupos(self):
        todos = [t for times in GRUPOS.values() for t in times]
        assert len(todos) == 48

    def test_sem_times_duplicados(self):
        todos = [t for times in GRUPOS.values() for t in times]
        assert len(todos) == len(set(todos))

    def test_todos_times_existem_em_times(self):
        for g, times in GRUPOS.items():
            for t in times:
                assert t in TIMES, f'{t} do grupo {g} não está em TIMES'


# ── JOGOS ─────────────────────────────────────────────────────────────────────

class TestJogos:

    def test_total_72_jogos(self):
        assert len(JOGOS) == 72

    def test_6_jogos_por_grupo(self):
        for g in GRUPOS:
            jogos_g = [j for j in JOGOS if j['grupo'] == g]
            assert len(jogos_g) == 6, f'Grupo {g} tem {len(jogos_g)} jogos'

    def test_ids_unicos(self):
        ids = [j['id'] for j in JOGOS]
        assert len(ids) == len(set(ids))

    def test_campos_obrigatorios(self):
        campos = {'id', 'grupo', 'rodada', 'time1', 'time2'}
        for j in JOGOS:
            for c in campos:
                assert c in j, f'Campo {c} falta no jogo {j.get("id")}'

    def test_times_existem_em_times(self):
        for j in JOGOS:
            assert j['time1'] in TIMES, f'{j["time1"]} não está em TIMES'
            assert j['time2'] in TIMES, f'{j["time2"]} não está em TIMES'

    def test_rodadas_validas(self):
        for j in JOGOS:
            assert j['rodada'] in (1, 2, 3)

    def test_time1_diferente_de_time2(self):
        for j in JOGOS:
            assert j['time1'] != j['time2']


# ── R32_BRACKET ───────────────────────────────────────────────────────────────

class TestR32Bracket:

    def test_exatamente_16_jogos(self):
        assert len(R32_BRACKET) == 16

    def test_ids_r32_01_a_16(self):
        ids = {j['id'] for j in R32_BRACKET}
        esperados = {f'R32-{i:02d}' for i in range(1, 17)}
        assert ids == esperados

    def test_campos_obrigatorios(self):
        for slot in R32_BRACKET:
            assert 'id' in slot
            assert 'time1' in slot
            assert 'time2' in slot


# ── TEAMS_INFO ────────────────────────────────────────────────────────────────

class TestTeamsInfo:

    def test_48_entradas(self):
        assert len(TEAMS_INFO) == 48

    def test_todos_codigos_existem_em_times(self):
        for code in TEAMS_INFO:
            assert code in TIMES, f'{code} em TEAMS_INFO mas não em TIMES'

    def test_campos_obrigatorios(self):
        campos = {'nome', 'confederacao', 'tecnico', 'historia'}
        for code, info in TEAMS_INFO.items():
            for c in campos:
                assert c in info, f'Campo {c} falta em {code}'

    def test_confederacoes_validas(self):
        validas = {'UEFA', 'CONMEBOL', 'CONCACAF', 'AFC', 'CAF', 'OFC'}
        for code, info in TEAMS_INFO.items():
            conf = info.get('confederacao', '')
            assert conf in validas, f'{code} tem confederação inválida: {conf}'

    def test_historia_tem_campos(self):
        for code, info in TEAMS_INFO.items():
            h = info.get('historia', {})
            assert 'p' in h, f'Falta "p" no histórico de {code}'
            assert 'titulos' in h, f'Falta "titulos" no histórico de {code}'

    def test_tecnico_tem_nome(self):
        for code, info in TEAMS_INFO.items():
            tec = info.get('tecnico', {})
            assert 'nome' in tec and tec['nome'], f'Falta nome do técnico em {code}'

    def test_bandeira_url_existe(self):
        for code, info in TEAMS_INFO.items():
            assert 'bandeira' in info and info['bandeira'], f'Falta bandeira em {code}'


# ── ESTADIOS ──────────────────────────────────────────────────────────────────

class TestEstadios:

    def test_exatamente_16_estadios(self):
        assert len(ESTADIOS) == 16

    def test_campos_obrigatorios(self):
        campos = {'nome', 'cidade', 'pais', 'capacidade'}
        for eid, est in ESTADIOS.items():
            for c in campos:
                assert c in est, f'Campo {c} falta no estádio {eid}'

    def test_paises_validos(self):
        paises_validos = {'Estados Unidos', 'Canadá', 'México'}
        for eid, est in ESTADIOS.items():
            assert est['pais'] in paises_validos, \
                f'País inválido no estádio {eid}: {est["pais"]}'

    def test_capacidade_positiva(self):
        for eid, est in ESTADIOS.items():
            assert est['capacidade'] > 0, f'Capacidade inválida no estádio {eid}'
