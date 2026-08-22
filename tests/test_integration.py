import pytest

from app import app, Temperature, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    db.drop_all()
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Celsius to Fahrenheit Converter" in response.data


def test_conversion_is_saved_to_database(client):
    response = client.post(
        "/",
        data={"celsius": "25"},
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        temperature = Temperature.query.order_by(
            Temperature.id.desc()
        ).first()

        assert temperature is not None
        assert temperature.celsius == 25
        assert temperature.fahrenheit == 77


def test_zero_celsius_is_saved_correctly(client):
    response = client.post(
        "/",
        data={"celsius": "0"},
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        temperature = Temperature.query.order_by(
            Temperature.id.desc()
        ).first()

        assert temperature is not None
        assert temperature.celsius == 0
        assert temperature.fahrenheit == 32


def test_conversion_appears_in_recent_conversions(client):
    client.post(
        "/",
        data={"celsius": "100"},
        follow_redirects=True
    )

    response = client.get("/")

    assert response.status_code == 200
    assert b"100.0" in response.data
    assert b"212.0" in response.data