import pytest

@pytest.fixture
def test_recipe(authorized_client, test_user, session):
    recipe_data = {
        "title": "Test Recipe",
        "description": "Test Description",
        "cooking_time": 30,
        "servings": 4,
        "ingredients": [
            {
                "ingredient_id": 1,
                "quantity": 2,
                "notes": "test notes"
            }
        ],
        "instructions": [
            {
                "step_number": 1,
                "description": "Test instruction"
            }
        ]
    }
    response = authorized_client.post("/recipes/", json=recipe_data)
    assert response.status_code == 201
    return response.json()

def test_create_recipe(authorized_client):
    recipe_data = {
        "title": "New Recipe",
        "description": "Description",
        "cooking_time": 30,
        "servings": 4,
        "ingredients": [
            {
                "ingredient_id": 1,
                "quantity": 2,
                "notes": "test notes"
            }
        ],
        "instructions": [
            {
                "step_number": 1,
                "description": "Test instruction"
            }
        ]
    }
    response = authorized_client.post("/recipes/", json=recipe_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Recipe"
    assert data["cooking_time"] == 30

def test_get_recipe(authorized_client, test_recipe):
    response = authorized_client.get(f"/recipes/{test_recipe['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_recipe["title"]

def test_get_nonexistent_recipe(authorized_client):
    response = authorized_client.get("/recipes/99999")
    assert response.status_code == 404

def test_update_recipe(authorized_client, test_recipe):
    updated_data = {
        "title": "Updated Recipe",
        "description": "Updated Description",
        "cooking_time": 45,
        "servings": 6,
        "ingredients": [
            {
                "ingredient_id": 1,
                "quantity": 3,
                "notes": "updated notes"
            }
        ],
        "instructions": [
            {
                "step_number": 1,
                "description": "Updated instruction"
            }
        ]
    }
    response = authorized_client.put(
        f"/recipes/{test_recipe['id']}", 
        json=updated_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Recipe"
    assert data["cooking_time"] == 45

def test_delete_recipe(authorized_client, test_recipe):
    response = authorized_client.delete(f"/recipes/{test_recipe['id']}")
    assert response.status_code == 204

def test_delete_nonexistent_recipe(authorized_client):
    response = authorized_client.delete("/recipes/99999")
    assert response.status_code == 404 