from conftest import register_and_login

PDF = ("a.pdf", b"%PDF-1.4 teacher file", "application/pdf")


def test_full_flow_and_permissions(client):
    teacher = register_and_login(client, "t1@example.com", "teacher")
    teacher2 = register_and_login(client, "t2@example.com", "teacher")
    student = register_and_login(client, "s1@example.com", "student")
    outsider = register_and_login(client, "s2@example.com", "student")

    # duplicate registration rejected
    r = client.post(
        "/auth/register",
        json={"email": "t1@example.com", "name": "x", "password": "password123", "role": "teacher"},
    )
    assert r.status_code == 409

    # students cannot create classes; unauthenticated is 401
    assert client.post("/classes", json={"name": "X"}, headers=student).status_code == 403
    assert client.post("/classes", json={"name": "X"}).status_code == 401

    # teacher creates class, student joins
    cls = client.post("/classes", json={"name": "CS101"}, headers=teacher).json()
    code = cls["join_code"]
    assert code
    r = client.post("/classes/join", json={"join_code": code}, headers=student)
    assert r.status_code == 200 and r.json()["join_code"] is None  # code hidden from students
    assert client.post("/classes/join", json={"join_code": "nope"}, headers=outsider).status_code == 404

    # teacher creates assignment with attachment
    r = client.post(
        f"/classes/{cls['id']}/assignments",
        data={"title": "HW1", "description": "Read ch1"},
        files={"file": PDF},
        headers=teacher,
    )
    assert r.status_code == 201, r.text
    a = r.json()
    assert a["class_id"] == cls["id"] and a["attachment_filename"] == "a.pdf"

    # permissions on assignment creation
    url = f"/classes/{cls['id']}/assignments"
    assert client.post(url, data={"title": "t"}, headers=student).status_code == 403
    assert client.post(url, data={"title": "t"}, headers=teacher2).status_code == 403

    # members can list/download; outsiders cannot
    assert len(client.get(url, headers=student).json()) == 1
    assert client.get(url, headers=outsider).status_code == 403
    r = client.get(f"/assignments/{a['id']}/attachment", headers=student)
    assert r.status_code == 200 and r.content == PDF[1]
    assert client.get(f"/assignments/{a['id']}/attachment", headers=outsider).status_code == 403

    # student submits; outsider and teacher cannot
    sub_url = f"/assignments/{a['id']}/submissions"
    r = client.post(sub_url, files={"file": ("hw.pdf", b"v1", "application/pdf")}, headers=student)
    assert r.status_code == 201, r.text
    assert client.post(sub_url, files={"file": ("hw.pdf", b"x", "application/pdf")}, headers=outsider).status_code == 403
    assert client.post(sub_url, files={"file": ("hw.pdf", b"x", "application/pdf")}, headers=teacher).status_code == 403

    # bad file type rejected
    r = client.post(sub_url, files={"file": ("x.exe", b"MZ", "application/x-msdownload")}, headers=student)
    assert r.status_code == 415

    # resubmission replaces the file (still a single submission)
    r = client.post(sub_url, files={"file": ("hw2.pdf", b"v2", "application/pdf")}, headers=student)
    assert r.status_code == 201
    subs = client.get(sub_url, headers=teacher).json()
    assert len(subs) == 1 and subs[0]["filename"] == "hw2.pdf"

    # teacher owner downloads; other teacher and outsider cannot
    sid = subs[0]["id"]
    assert client.get(f"/submissions/{sid}/file", headers=teacher).content == b"v2"
    assert client.get(f"/submissions/{sid}/file", headers=student).content == b"v2"
    assert client.get(f"/submissions/{sid}/file", headers=teacher2).status_code == 403
    assert client.get(f"/submissions/{sid}/file", headers=outsider).status_code == 403

    # bad ids -> 404
    assert client.get("/assignments/not-an-id", headers=teacher).status_code == 404
