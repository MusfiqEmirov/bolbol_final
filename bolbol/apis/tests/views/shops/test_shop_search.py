import pytest
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_search_missing_query_param(api_client):
    response = api_client.get("/api/v1/shops/search/")
    assert response.status_code == 400
    assert "error" in response.data


@pytest.mark.django_db
@patch("apis.views.shops.ShopDocument.search")
def test_search_no_results(mock_search, api_client):
    mock_response = MagicMock()
    mock_response.execute.return_value = []
    mock_search.return_value = mock_response

    response = api_client.get("/api/v1/shops/search/", {"query": "noresults"})
    assert response.status_code == 200
    assert response.data == []

@pytest.mark.django_db
@patch("apis.views.shops.ShopDocument.search")
def test_search_elasticsearch_exception(mock_search, api_client):
    mock_search.side_effect = Exception("Elasticsearch down")

    response = api_client.get("/api/v1/shops/search/", {"query": "error"})
    assert response.status_code == 500
    assert "error" in response.data

@pytest.mark.django_db
def test_search_empty_query_param(api_client):
    response = api_client.get("/api/v1/shops/search/", {"query": ""})
    assert response.status_code == 400
    assert "error" in response.data
