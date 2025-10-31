from web.app import app

def test_html_index_route():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200
    # Check if we got HTML response
    assert res.content_type.startswith('text/html')

def test_api_status_route():
    client = app.test_client()
    res = client.get('/api/status')
    assert res.status_code == 200
    data = res.get_json()
    assert 'message' in data
    assert 'db_connection' in data
    assert 'db_info' in data

