def test_add_favorite(authorized_client, test_recipe):
    response = authorized_client.post(f"/favorites/{test_recipe['id']}")
    assert response.status_code == 201

def test_add_nonexistent_recipe_to_favorites(authorized_client):
    response = authorized_client.post("/favorites/99999")
    assert response.status_code == 404

def test_add_duplicate_favorite(authorized_client, test_recipe):
    # Add first time
    response = authorized_client.post(f"/favorites/{test_recipe['id']}")
    assert response.status_code == 201
    
    # Try to add same recipe again
    response = authorized_client.post(f"/favorites/{test_recipe['id']}")
    assert response.status_code == 400

def test_get_favorites(authorized_client, test_recipe):
    # Add to favorites first
    authorized_client.post(f"/favorites/{test_recipe['id']}")
    
    response = authorized_client.get("/favorites/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == test_recipe["id"]

def test_remove_favorite(authorized_client, test_recipe):
    # Add to favorites first
    authorized_client.post(f"/favorites/{test_recipe['id']}")
    
    # Then remove
    response = authorized_client.delete(f"/favorites/{test_recipe['id']}")
    assert response.status_code == 204

def test_remove_nonexistent_favorite(authorized_client):
    response = authorized_client.delete("/favorites/99999")
    assert response.status_code == 404 