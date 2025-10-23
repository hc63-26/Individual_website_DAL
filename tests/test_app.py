import importlib
import DAL
import app as app_module


def setup_temp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_app.db"
    # reload DAL first, then set DATABASE_FILE so any subsequent reloads use the temp DB
    importlib.reload(DAL)
    monkeypatch.setattr(DAL, 'DATABASE_FILE', str(db_file))
    # reload app so it uses the updated DAL (and the tmp DB)
    importlib.reload(app_module)


def test_projects_page_empty(tmp_path, monkeypatch):
    setup_temp_db(tmp_path, monkeypatch)
    client = app_module.app.test_client()

    resp = client.get('/projects')
    assert resp.status_code == 200
    # page should render even if there are no projects
    assert b'Projects' in resp.data or b'projects' in resp.data


def test_add_project_and_list(tmp_path, monkeypatch):
    setup_temp_db(tmp_path, monkeypatch)
    client = app_module.app.test_client()

    # POST to add project
    resp = client.post('/add', data={
        'title': 'Test Project',
        'description': 'A test',
        'image_file_name': 'img.png'
    }, follow_redirects=True)

    assert resp.status_code == 200
    # After adding, should redirect to projects and show the title
    assert b'Test Project' in resp.data
