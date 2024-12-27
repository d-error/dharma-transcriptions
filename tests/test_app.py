import pytest

from dharma_transcriptions import create_app


@pytest.fixture
def app():
    """Fixture to create a test instance of the app."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'DEBUG': False,
    })
    return app


@pytest.fixture
def client(app):
    """Fixture to provide a test client for the app."""
    return app.test_client()


def test_app_creation(app):
    """Test if the app is created successfully."""
    assert app is not None
    assert app.testing is True


def test_home_endpoint(client):
    """Test the response of a basic endpoint (e.g., '/' if it exists)."""
    response = client.get('/')
    assert response.status_code in {
        200,
        404,
    }
