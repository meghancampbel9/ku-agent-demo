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


def test_welcome_page(client):
    r = client.get("/welcome")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert "Hey Meg!" in r.text
