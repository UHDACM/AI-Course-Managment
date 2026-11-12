from conftest import register_and_login

RANGE = {"start": "2030-03-01", "end": "2030-03-31"}


def test_calendar_todos(client):
    teacher = register_and_login(client, "ct@example.com", "teacher")
    student = register_and_login(client, "cs@example.com", "student")
    other = register_and_login(client, "co@example.com", "student")

    cls = client.post("/classes", json={"name": "Cal101"}, headers=teacher).json()
    client.post("/classes/join", json={"join_code": cls["join_code"]}, headers=student)
    url = f"/classes/{cls['id']}/assignments"
    r = client.post(url, data={"title": "HW", "due_date": "2030-03-10T12:00:00"}, headers=teacher)
    assert r.status_code == 201, r.text
    client.post(url, data={"title": "Later", "due_date": "2030-06-10T12:00:00"}, headers=teacher)

    # add todos to days
    r = client.post("/calendar/todos", json={"title": "Study", "date": "2030-03-10"}, headers=student)
    assert r.status_code == 201, r.text
    tid = r.json()["id"]
    client.post("/calendar/todos", json={"title": "Laundry", "date": "2030-03-05"}, headers=student)
    assert client.post("/calendar/todos", json={"title": "x", "date": "2030-03-05"}).status_code == 401

    feed = client.get("/calendar", params=RANGE, headers=student).json()
    assert [d["date"] for d in feed] == ["2030-03-05", "2030-03-10"]
    assert feed[1]["todos"][0]["title"] == "Study"
    assert feed[1]["assignments"][0]["title"] == "HW"  # due date shows on its day
    assert feed[0]["assignments"] == []
    assert feed[1]["assignments"][0]["completed"] is False  # not submitted yet

    # submitting marks it completed (for that student only)
    aid = feed[1]["assignments"][0]["id"]
    sub = client.post(
        f"/assignments/{aid}/submissions",
        files={"file": ("hw.pdf", b"%PDF-1.4 hw", "application/pdf")},
        headers=student,
    )
    assert sub.status_code == 201, sub.text
    feed = client.get("/calendar", params=RANGE, headers=student).json()
    assert feed[1]["assignments"][0]["completed"] is True
    t_feed = client.get("/calendar", params=RANGE, headers=teacher).json()
    assert t_feed[0]["assignments"][0]["completed"] is False

    # todos are private; assignments only for class members
    assert client.get("/calendar", params=RANGE, headers=other).json() == []
    assert len(t_feed) == 1 and t_feed[0]["todos"] == []

    # check off, move, remove
    r = client.patch(f"/calendar/todos/{tid}", json={"completed": True, "date": "2030-03-12"}, headers=student)
    assert r.status_code == 200 and r.json()["completed"] and r.json()["date"] == "2030-03-12"
    assert client.patch(f"/calendar/todos/{tid}", json={"completed": True}, headers=other).status_code == 403
    assert client.delete(f"/calendar/todos/{tid}", headers=other).status_code == 403
    assert client.delete(f"/calendar/todos/{tid}", headers=student).status_code == 204
    assert client.delete(f"/calendar/todos/{tid}", headers=student).status_code == 404

    big = {"start": "2030-01-01", "end": "2032-01-01"}
    assert client.get("/calendar", params=big, headers=student).status_code == 422
