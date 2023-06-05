import pytest

from snap import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_pong(client):
    """Start with a blank database."""

    rv = client.get('/ping')
    assert b'pong' in rv.data
