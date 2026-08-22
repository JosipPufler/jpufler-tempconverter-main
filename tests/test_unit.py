from unittest.mock import patch

from app import app


def test_home_page_loads():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        response = client.get("/")

        assert response.status_code == 200
        assert b"Celsius to Fahrenheit Converter" in response.data


def test_celsius_to_fahrenheit_conversion():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        with app.test_client() as client:
            with patch("app.db.session.add") as mock_add, \
                 patch("app.db.session.commit") as mock_commit, \
                 patch("app.Temperature.query") as mock_query:

                mock_query.order_by.return_value.limit.return_value.all.return_value = []

                response = client.post(
                    "/",
                    data={"celsius": "25"},
                    follow_redirects=True
                )

                assert response.status_code == 200

                temperature = mock_add.call_args[0][0]

                assert temperature.celsius == 25
                assert temperature.fahrenheit == 77

def test_negative_celsius_conversion():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        with patch("app.db.session.add") as mock_add, \
             patch("app.db.session.commit") as mock_commit, \
             patch("app.Temperature.query") as mock_query:

            mock_query.order_by.return_value.limit.return_value.all.return_value = []

            response = client.post(
                "/",
                data={"celsius": "-40"},
                follow_redirects=True
            )

            assert response.status_code == 200

            temperature = mock_add.call_args[0][0]

            assert temperature.celsius == -40
            assert temperature.fahrenheit == -40