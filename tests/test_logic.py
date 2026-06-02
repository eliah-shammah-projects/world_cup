"""Testes unitários para logic.py"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import logic
from data import GRUPOS, JOGOS


# ── Helpers ──────────────────────────────────────────────────────────────────

def _res(jid, g1, g2):
    return {jid: {'gols1': g1, 'gols2': g2}}


def _jogos_grupo(g):
    return [j for j in JOGOS if j['grupo'] == g]


def _id(g, idx):
    """Retorna o ID do idx-ésimo jogo do grupo g (1-based)."""
    jogos = _jogos_grupo(g)
    return jogos[idx - 1]['id']


# ── classificar_grupo ─────────────────────────────────────────────────────────

class TestClassificarGrupo:

    def test_sem_resultados_todos_zerados(self):
        tabela = logic.classificar_grupo('A', {})
        for t in tabela:
            assert t['pts'] == 0
            assert t['j'] == 0

    def test_quatro_times_retornados(self):
        tabela = logic.classificar_grupo('A', {})
        assert len(tabela) == 4

    def test_vitoria_vale_3_pontos(self):
        jid = _id('A', 1)  # MEX x AFS
        resultados = _res(jid, 2, 0)
        tabela = logic.classificar_grupo('A', resultados)
        mex = next(t for t in tabela if t['time'] == 'MEX')
        afs = next(t for t in tabela if t['time'] == 'AFS')
        assert mex['pts'] == 3
        assert afs['pts'] == 0

    def test_empate_vale_1_ponto_cada(self):
        jid = _id('A', 1)  # MEX x AFS
        resultados = _res(jid, 1, 1)
        tabela = logic.classificar_grupo('A', resultados)
        mex = next(t for t in tabela if t['time'] == 'MEX')
        afs = next(t for t in tabela if t['time'] == 'AFS')
        assert mex['pts'] == 1
        assert afs['pts'] == 1

    def test_derrota_vale_0_pontos(self):
        jid = _id('A', 1)  # MEX x AFS
        resultados = _res(jid, 0, 3)
        tabela = logic.classificar_grupo('A', resultados)
        mex = next(t for t in tabela if t['time'] == 'MEX')
        assert mex['pts'] == 0
        assert mex['d'] == 1

    def test_saldo_de_gols_calculado(self):
        jid = _id('A', 1)  # MEX x AFS
        resultados = _res(jid, 3, 1)
        tabela = logic.classificar_grupo('A', resultados)
        mex = next(t for t in tabela if t['time'] == 'MEX')
        afs = next(t for t in tabela if t['time'] == 'AFS')
        assert mex['sg'] == 2
        assert afs['sg'] == -2

    def test_ordenacao_por_pontos(self):
        j1 = _id('A', 1)  # MEX x AFS — MEX ganha
        j2 = _id('A', 2)  # COR x TCH — COR ganha
        resultados = {**_res(j1, 1, 0), **_res(j2, 1, 0)}
        tabela = logic.classificar_grupo('A', resultados)
        assert tabela[0]['time'] in ('MEX', 'COR')
        assert tabela[0]['pts'] == 3

    def test_gols_pro_e_contra_corretos(self):
        jid = _id('A', 1)  # MEX x AFS
        resultados = _res(jid, 4, 2)
        tabela = logic.classificar_grupo('A', resultados)
        mex = next(t for t in tabela if t['time'] == 'MEX')
        afs = next(t for t in tabela if t['time'] == 'AFS')
        assert mex['gp'] == 4
        assert mex['gc'] == 2
        assert afs['gp'] == 2
        assert afs['gc'] == 4

    def test_jogos_contabilizados(self):
        j1 = _id('A', 1)
        j2 = _id('A', 3)  # MEX joga nos jogos 1 e 3
        resultados = {**_res(j1, 1, 0), **_res(j2, 2, 1)}
        tabela = logic.classificar_grupo('A', resultados)
        mex = next(t for t in tabela if t['time'] == 'MEX')
        assert mex['j'] == 2

    def test_desempate_por_saldo_gols(self):
        # MEX e COR com mesmos pontos mas MEX com melhor saldo
        j1 = _id('A', 1)  # MEX x AFS
        j2 = _id('A', 2)  # COR x TCH
        j3 = _id('A', 3)  # MEX x COR
        resultados = {
            **_res(j1, 3, 0),  # MEX 3pts, sg+3
            **_res(j2, 1, 0),  # COR 3pts, sg+1
            **_res(j3, 0, 0),  # MEX x COR empate — ambos 4pts agora
        }
        tabela = logic.classificar_grupo('A', resultados)
        # MEX tem sg maior (3+0=3 vs 1+0=1 após os jogos disponíveis)
        posicoes = [t['time'] for t in tabela]
        assert posicoes.index('MEX') < posicoes.index('COR')


# ── get_vencedor_mk ───────────────────────────────────────────────────────────

class TestGetVencedorMk:

    def test_nao_jogado_retorna_none(self):
        assert logic.get_vencedor_mk('R32-01', 'BRA', 'ARG', {}) is None

    def test_time1_vence(self):
        r = {'R32-01': {'gols1': 2, 'gols2': 0}}
        assert logic.get_vencedor_mk('R32-01', 'BRA', 'ARG', r) == 'BRA'

    def test_time2_vence(self):
        r = {'R32-01': {'gols1': 0, 'gols2': 1}}
        assert logic.get_vencedor_mk('R32-01', 'BRA', 'ARG', r) == 'ARG'

    def test_empate_retorna_pen_vencedor(self):
        r = {'R32-01': {'gols1': 1, 'gols2': 1, 'pen_vencedor': 'BRA'}}
        assert logic.get_vencedor_mk('R32-01', 'BRA', 'ARG', r) == 'BRA'

    def test_empate_sem_pen_retorna_none(self):
        r = {'R32-01': {'gols1': 1, 'gols2': 1}}
        assert logic.get_vencedor_mk('R32-01', 'BRA', 'ARG', r) is None

    def test_time_none_retorna_none(self):
        r = {'R32-01': {'gols1': 2, 'gols2': 0}}
        assert logic.get_vencedor_mk('R32-01', None, 'ARG', r) is None


# ── get_perdedor_mk ───────────────────────────────────────────────────────────

class TestGetPerdedorMk:

    def test_perdedor_correto(self):
        r = {'R32-01': {'gols1': 2, 'gols2': 0}}
        assert logic.get_perdedor_mk('R32-01', 'BRA', 'ARG', r) == 'ARG'

    def test_nao_jogado_retorna_none(self):
        assert logic.get_perdedor_mk('R32-01', 'BRA', 'ARG', {}) is None

    def test_perdedor_com_penaltis(self):
        r = {'R32-01': {'gols1': 1, 'gols2': 1, 'pen_vencedor': 'ARG'}}
        assert logic.get_perdedor_mk('R32-01', 'BRA', 'ARG', r) == 'BRA'


# ── gerar_fases_mata_mata ─────────────────────────────────────────────────────

class TestGerarFasesMataMAta:

    def _bracket_fake(self):
        """Gera um bracket R32 com times fictícios para teste."""
        bracket = []
        for i in range(1, 17):
            jid = f'R32-{i:02d}'
            bracket.append({
                'id': jid,
                'time1_code': f'T{i*2-1}',
                'time2_code': f'T{i*2}',
            })
        return bracket

    def _resultados_r32(self, bracket):
        """Time1 sempre vence em todos os jogos R32."""
        return {j['id']: {'gols1': 2, 'gols2': 0} for j in bracket}

    def test_retorna_todas_as_fases(self):
        bracket = self._bracket_fake()
        res_mk = self._resultados_r32(bracket)
        fases = logic.gerar_fases_mata_mata(bracket, res_mk)
        assert 'r16' in fases
        assert 'qf' in fases
        assert 'sf' in fases
        assert 'final' in fases
        assert 'terceiro' in fases
        assert 'campeao' in fases

    def test_r16_tem_8_jogos(self):
        bracket = self._bracket_fake()
        res_mk = self._resultados_r32(bracket)
        fases = logic.gerar_fases_mata_mata(bracket, res_mk)
        assert len(fases['r16']) == 8

    def test_qf_tem_4_jogos(self):
        bracket = self._bracket_fake()
        res_mk = self._resultados_r32(bracket)
        fases = logic.gerar_fases_mata_mata(bracket, res_mk)
        assert len(fases['qf']) == 4

    def test_sf_tem_2_jogos(self):
        bracket = self._bracket_fake()
        res_mk = self._resultados_r32(bracket)
        fases = logic.gerar_fases_mata_mata(bracket, res_mk)
        assert len(fases['sf']) == 2

    def test_sem_resultados_campeao_none(self):
        bracket = self._bracket_fake()
        fases = logic.gerar_fases_mata_mata(bracket, {})
        assert fases['campeao'] is None

    def test_progressao_vencedores(self):
        """Vencedor do R32-01 deve aparecer no R16-01."""
        bracket = self._bracket_fake()
        res_mk = self._resultados_r32(bracket)
        fases = logic.gerar_fases_mata_mata(bracket, res_mk)
        # T1 venceu R32-01, deve estar no R16-01
        assert fases['r16'][0]['time1_code'] == 'T1'


# ── melhores_terceiros ────────────────────────────────────────────────────────

class TestMelhoresTerceiros:

    def test_sem_resultados_retorna_12(self):
        terceiros = logic.melhores_terceiros({})
        assert len(terceiros) == 12

    def test_cada_terceiro_tem_grupo(self):
        terceiros = logic.melhores_terceiros({})
        for t in terceiros:
            assert 'grupo' in t
            assert t['grupo'] in list('ABCDEFGHIJKL')

    def test_ordenados_por_pontos(self):
        # Dá 3 pontos ao 3º do grupo A fazendo ele ganhar um jogo
        j1 = _id('A', 2)  # COR x TCH — COR ganha, TCH perde (3º lugar com 0pts)
        j2 = _id('A', 1)  # MEX x AFS — MEX ganha
        j3 = _id('A', 3)  # MEX x COR — MEX ganha
        j4 = _id('A', 4)  # AFS x TCH — AFS ganha (dá pts ao 3º AFS)
        resultados = {
            **_res(j1, 2, 0),
            **_res(j2, 1, 0),
            **_res(j3, 1, 0),
            **_res(j4, 3, 0),
        }
        terceiros = logic.melhores_terceiros(resultados)
        pts_list = [t['pts'] for t in terceiros]
        assert pts_list == sorted(pts_list, reverse=True)
