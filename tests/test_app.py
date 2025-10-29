from web.app import app
def test_index_route():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200
    data = res.get_json()
    assert 'message' in data
