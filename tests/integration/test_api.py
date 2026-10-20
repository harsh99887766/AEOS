def test_plugins_endpoint_lists_github_plugin(client):
    response = client.get("/api/v1/plugins")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "github"
