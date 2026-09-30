def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"service": "ku-agent-demo"}


def test_create_and_list(client):
    r = client.post("/todos", json={"title": "write tests"})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "write tests", "done": False}
    assert client.get("/todos").json() == [{"id": 1, "title": "write tests", "done": False}]


def test_get_missing_returns_404(client):
    assert client.get("/todos/42").status_code == 404


def test_delete(client):
    tid = client.post("/todos", json={"title": "x"}).json()["id"]
    assert client.delete(f"/todos/{tid}").status_code == 204
    assert client.get("/todos").json() == []


def test_validation(client):
    assert client.post("/todos", json={"title": ""}).status_code == 422


def test_patch_done(client):
    tid = client.post("/todos", json={"title": "x"}).json()["id"]
    r = client.patch(f"/todos/{tid}", json={"done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True
    assert client.get(f"/todos/{tid}").json()["done"] is True


def test_patch_missing_returns_404(client):
    assert client.patch("/todos/42", json={"done": True}).status_code == 404


def test_ui_served(client):
    r = client.get("/ui")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
