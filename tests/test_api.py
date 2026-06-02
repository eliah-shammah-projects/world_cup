"""Testes de integração para as rotas Flask (app.py)"""
import pytest
import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data import JOGOS


def _primeiro_jogo():
    return JOGOS[0]['id']


def _post_json(client, url, data):
    return client.post(url,
                       data=json.dumps(data),
                       content_type='application/json')


# ── Páginas ───────────────────────────────────────────────────────────────────

class TestPaginas:

    def test_index_retorna_200(self, client):
        r = client.get('/')
        assert r.status_code == 200

    def test_grupos_retorna_200(self, client):
        r = client.get('/grupos')
        assert r.status_code == 200

    def test_mata_mata_retorna_200(self, client):
        r = client.get('/mata-mata')
        assert r.status_code == 200

    def test_selecao_brasil_retorna_200(self, client):
        r = client.get('/selecao/BRA')
        assert r.status_code == 200

    def test_selecao_invalida_redireciona(self, client):
        r = client.get('/selecao/XXXX')
        assert r.status_code == 302

    def test_vitoria_brasil_retorna_200(self, client):
        r = client.get('/vitoria/BRA')
        assert r.status_code == 200

    def test_vitoria_invalida_redireciona(self, client):
        r = client.get('/vitoria/XXXX')
        assert r.status_code == 302

    def test_index_contem_estadios(self, client):
        r = client.get('/')
        assert r.status_code == 200
        assert 'Est' in r.data.decode('utf-8')


# ── API resultado (fase de grupos) ────────────────────────────────────────────

class TestApiResultado:

    def test_salvar_resultado_ok(self, client):
        jid = _primeiro_jogo()
        r = _post_json(client, '/api/resultado', {'jogo_id': jid, 'gols1': 2, 'gols2': 1})
        data = json.loads(r.data)
        assert r.status_code == 200
        assert data['ok'] is True

    def test_salvar_resultado_retorna_tabela(self, client):
        jid = _primeiro_jogo()
        r = _post_json(client, '/api/resultado', {'jogo_id': jid, 'gols1': 1, 'gols2': 0})
        data = json.loads(r.data)
        assert 'tabela' in data
        assert isinstance(data['tabela'], list)

    def test_salvar_resultado_retorna_done(self, client):
        jid = _primeiro_jogo()
        r = _post_json(client, '/api/resultado', {'jogo_id': jid, 'gols1': 0, 'gols2': 0})
        data = json.loads(r.data)
        assert 'done' in data
        assert data['done'] >= 1

    def test_jogo_inexistente_retorna_404(self, client):
        r = _post_json(client, '/api/resultado', {'jogo_id': 'XXXX', 'gols1': 1, 'gols2': 0})
        assert r.status_code == 404

    def test_placar_invalido_retorna_400(self, client):
        jid = _primeiro_jogo()
        r = _post_json(client, '/api/resultado', {'jogo_id': jid, 'gols1': 'abc', 'gols2': 0})
        assert r.status_code == 400

    def test_gols_negativos_retorna_400(self, client):
        jid = _primeiro_jogo()
        r = _post_json(client, '/api/resultado', {'jogo_id': jid, 'gols1': -1, 'gols2': 0})
        assert r.status_code == 400

    def test_limpar_resultado_ok(self, client):
        jid = _primeiro_jogo()
        _post_json(client, '/api/resultado', {'jogo_id': jid, 'gols1': 1, 'gols2': 0})
        r = client.delete(f'/api/resultado/{jid}')
        data = json.loads(r.data)
        assert r.status_code == 200
        assert data['ok'] is True


# ── API reset ─────────────────────────────────────────────────────────────────

class TestApiReset:

    def test_reset_ok(self, client):
        jid = _primeiro_jogo()
        _post_json(client, '/api/resultado', {'jogo_id': jid, 'gols1': 1, 'gols2': 0})
        r = _post_json(client, '/api/reset', {})
        data = json.loads(r.data)
        assert r.status_code == 200
        assert data['ok'] is True

    def test_reset_limpa_resultados(self, client):
        jid = _primeiro_jogo()
        _post_json(client, '/api/resultado', {'jogo_id': jid, 'gols1': 2, 'gols2': 1})
        _post_json(client, '/api/reset', {})
        r = _post_json(client, '/api/resultado', {'jogo_id': jid, 'gols1': 0, 'gols2': 0})
        data = json.loads(r.data)
        assert data['done'] == 1  # só 1 resultado após reset


# ── API terceiros ─────────────────────────────────────────────────────────────

class TestApiTerceiros:

    def test_retorna_lista(self, client):
        r = client.get('/api/terceiros')
        data = json.loads(r.data)
        assert r.status_code == 200
        assert isinstance(data, list)

    def test_retorna_12_terceiros(self, client):
        r = client.get('/api/terceiros')
        data = json.loads(r.data)
        assert len(data) == 12

    def test_cada_item_tem_campos_necessarios(self, client):
        r = client.get('/api/terceiros')
        data = json.loads(r.data)
        for t in data:
            assert 'time' in t
            assert 'pts' in t
            assert 'grupo' in t


# ── API mata-mata ─────────────────────────────────────────────────────────────

class TestApiMataMata:

    def test_salvar_resultado_mata_ok(self, client):
        r = _post_json(client, '/api/mata-mata', {
            'jogo_id': 'R32-01', 'gols1': 2, 'gols2': 0
        })
        data = json.loads(r.data)
        assert r.status_code == 200
        assert data['ok'] is True

    def test_empate_sem_penaltis_retorna_400(self, client):
        r = _post_json(client, '/api/mata-mata', {
            'jogo_id': 'R32-01', 'gols1': 1, 'gols2': 1
        })
        assert r.status_code == 400

    def test_empate_com_penaltis_ok(self, client):
        r = _post_json(client, '/api/mata-mata', {
            'jogo_id': 'R32-01', 'gols1': 1, 'gols2': 1, 'pen_vencedor': 'BRA'
        })
        data = json.loads(r.data)
        assert r.status_code == 200
        assert data['ok'] is True

    def test_placar_invalido_retorna_400(self, client):
        r = _post_json(client, '/api/mata-mata', {
            'jogo_id': 'R32-01', 'gols1': 'x', 'gols2': 0
        })
        assert r.status_code == 400
