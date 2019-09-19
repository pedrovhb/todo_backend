from starlette.testclient import TestClient

from main import app

client = TestClient(app)

created_todo_ids = {}


def test_empty_todos():
    response = client.get('/all_todos')
    assert response.status_code == 200
    assert response.json() == []


def test_get_invalid_id():
    response = client.get('/todo', params={'id_': 'invalid-id'})
    assert response.status_code == 400


def test_get_non_existent_id():
    response = client.get('/todo', params={'id_': "5d7c00f66108587a6e504c2a"})
    assert response.status_code == 404


def test_create_todo_boolean_invalid():
    invalid_inputs = [
        {},  # Invalid because text is a required field
        {'text': ''},  # Invalid because length has to be >= 1
        {'text': 'long text' * 100}  # Invalid because the string is too long
    ]
    for ii in invalid_inputs:
        response = client.post('/todo/boolean', json=ii)
        assert response.status_code == 422


def test_create_todo_boolean():
    response = client.post('/todo/boolean', json={
        'text': 'Test the create todo boolean function.',
        'completed': False
    })
    assert response.status_code == 200
    assert 'id_' in response.json()

    created_todo_ids['boolean'] = response.json()['id_']


def test_get_created_todo_boolean():
    response = client.get('/todo', params={'id_': created_todo_ids['boolean']})
    assert response.status_code == 200
    assert response.json()['text'] == 'Test the create todo boolean function.'
    assert response.json()['completed'] is False


def test_update_todo_boolean():
    # Get to-do and mark it as completed. Then, get it again and assert it's still marked as completed
    todo = client.get('/todo', params={'id_': created_todo_ids['boolean']}).json()
    assert todo['completed'] is False
    todo['completed'] = True
    response = client.patch('/todo', json=todo)
    assert response.status_code == 200
    updated_todo = client.get('/todo', params={'id_': created_todo_ids['boolean']}).json()
    assert updated_todo['completed'] is True


def test_create_todo_count():
    response = client.post('/todo/count', json={
        'text': 'Test the create todo count function.',
        'target_count': 10
    })
    assert response.status_code == 200
    assert 'id_' in response.json()

    created_todo_ids['count'] = response.json()['id_']


def test_get_created_todo_count():
    response = client.get('/todo', params={'id_': created_todo_ids['count']})
    assert response.status_code == 200
    assert response.json()['text'] == 'Test the create todo count function.'
    assert response.json()['current_count'] == 0


def test_update_todo_count():
    todo = client.get('/todo', params={'id_': created_todo_ids['count']}).json()
    assert todo['current_count'] == 0
    todo['current_count'] = 7
    response = client.patch('/todo', json=todo)
    assert response.status_code == 200
    updated_todo = client.get('/todo', params={'id_': created_todo_ids['count']}).json()
    assert updated_todo['current_count'] == 7


def test_create_todo_timer():
    response = client.post('/todo/timer', json={
        'text': 'Test the create todo timer function.',
        'target_time': 200  # seconds
    })
    assert response.status_code == 200
    assert 'id_' in response.json()

    created_todo_ids['timer'] = response.json()['id_']


def test_get_created_todo_timer():
    response = client.get('/todo', params={'id_': created_todo_ids['timer']})
    assert response.status_code == 200
    assert response.json()['text'] == 'Test the create todo timer function.'
    assert response.json()['current_time'] == 0


def test_update_todo_timer():
    todo = client.get('/todo', params={'id_': created_todo_ids['timer']}).json()
    assert todo['current_time'] == 0
    todo['current_time'] = 120
    response = client.patch('/todo', json=todo)
    assert response.status_code == 200
    updated_todo = client.get('/todo', params={'id_': created_todo_ids['timer']}).json()
    assert updated_todo['current_time'] == 120


def test_update_invalid_id():
    todo = client.get('/todo', params={'id_': created_todo_ids['timer']}).json()
    todo['id_'] = 'invalid-id'
    response = client.patch('/todo', json=todo)
    assert response.status_code == 400


def test_update_non_existent_id():
    todo = client.get('/todo', params={'id_': created_todo_ids['timer']}).json()
    todo['id_'] = "5d7c00f66108587a6e504c2a"  # Random non-existing ID
    response = client.patch('/todo', json=todo)
    assert response.status_code == 404


def test_all_todos():
    response = client.get('/all_todos')
    assert response.status_code == 200
    for created_todo_id in created_todo_ids.values():
        assert any(created_todo_id == todo['id_'] for todo in response.json())


def test_delete_todo():
    response = client.delete('/todo', params={'id_': created_todo_ids['boolean']})
    assert response.status_code == 200
    response = client.get('/all_todos')
    assert response.status_code == 200
    assert not any(todo['id_'] == created_todo_ids['boolean'] for todo in response.json())
    assert len(response.json()) == 2


def test_delete_todo_invalid_id():
    response = client.delete('/todo', params={'id_': 'invalid-id'})
    assert response.status_code == 400


def test_delete_todo_non_existent_id():
    response = client.delete('/todo', params={'id_': '5d7c00f66108587a6e504c2a'})
    assert response.status_code == 404
