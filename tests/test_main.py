from fastapi.testclient import TestClient

from app.main import api as app

client = TestClient(app)


def test_dir_listing(tmp_path, monkeypatch):
    import app.main

    monkeypatch.setattr(app.main, "UPLOAD_DIRECTORY", f"{tmp_path}/df")

    d = tmp_path / "df"
    d.mkdir()
    file1 = d / "123456789.json"
    file2 = d / "987654321.json"
    file1.write_text("example")
    file2.write_text("example")

    response = client.get("/files")
    assert response.status_code == 200

    files_data = response.context["files"]
    assert files_data

    for file_data in files_data:
        assert file_data.endswith(".json")


def test_get_file_positive_case(tmp_path, monkeypatch):
    import app.main

    monkeypatch.setattr(app.main, "UPLOAD_DIRECTORY", f"{tmp_path}/df")

    d = tmp_path / "df"
    d.mkdir()
    file1 = d / "123456789.json"
    file2 = d / "987654321.json"
    file1.write_text("example")
    file2.write_text("example")

    response0 = client.get("/files")
    existing_file_name = response0.context["files"][0]

    response = client.get(f"/files/{existing_file_name}")
    assert response.status_code == 200
    assert response._content


def test_html5_predict(mock_predict_html_request_body):

    response = client.post(
        "/html5-predict", json=mock_predict_html_request_body
    )
    assert response.status_code == 200
    for element in response.json():
        assert element["predicted_label"]


def test_mui_predict(mock_predict_mui_request_body):

    response = client.post("/mui-predict", json=mock_predict_mui_request_body)
    assert response.status_code == 200
    for element in response.json():
        assert element["predicted_label"]


def test_get_cpu_count():
    response = client.get("/cpu-count")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["cpu_count"], int)


def test_get_system_info():
    response = client.get("/system_info")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["cpu_count"], int)
    assert isinstance(data["total_memory"], int)


def test_build_version():
    response = client.get("/build")
    assert response.json() == client.app.version


def test_ping_smtp():
    response = client.get("/ping_smtp")
    response_json = response.json()
    assert response_json == 1 or response_json.startswith(
        "Got Exception during pinging smtp.yandex.ru:"
    )
