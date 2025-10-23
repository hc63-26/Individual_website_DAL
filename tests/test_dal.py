import importlib
import DAL


def test_dal_crud(tmp_path, monkeypatch):
    # Use a temporary database file so tests don't touch the real DB
    db_file = tmp_path / "test_dal.db"
    monkeypatch.setattr(DAL, 'DATABASE_FILE', str(db_file))
    importlib.reload(DAL)

    # initialize and assert empty
    DAL.init_db()
    projects = list(DAL.get_all_projects())
    assert projects == []

    # add a project and verify
    DAL.add_project('Title A', 'Description A', 'a.png')
    projects = list(DAL.get_all_projects())
    assert len(projects) == 1
    pid = projects[0]['id']

    # get by id
    proj = DAL.get_project_by_id(pid)
    assert proj['title'] == 'Title A'

    # delete and verify empty again
    DAL.delete_project(pid)
    projects = list(DAL.get_all_projects())
    assert projects == []
