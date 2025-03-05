import pytest
from unittest.mock import MagicMock
from src.application.auth_module.api.services.user_service import UserService

pytestmark = pytest.mark.django_db

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def mock_person_repository():
    return MagicMock()

@pytest.fixture
def mock_serializer():
    return MagicMock()

@pytest.fixture
def user_service(mock_user_repository, mock_serializer, mock_person_repository):
    return UserService(mock_user_repository, mock_serializer, mock_person_repository)

@pytest.mark.django_db(transaction=True)
def test_get_all_users(user_service, mock_user_repository, mock_serializer):
    mock_users = [MagicMock(), MagicMock()]
    mock_user_repository.get_all.return_value.select_related.return_value = mock_users
    mock_serializer.return_value.data = [{"id": 1}, {"id": 2}]
    
    result = user_service.get_all()
    
    assert result == [{"id": 1}, {"id": 2}]
    mock_user_repository.get_all.assert_called_once()
    mock_serializer.assert_called_once_with(mock_users, many=True)

@pytest.mark.django_db(transaction=True)
def test_get_user_by_id_found(user_service, mock_user_repository, mock_serializer):
    mock_user = MagicMock()
    mock_user_repository.get_by_id.return_value = mock_user
    mock_serializer.return_value.data = {"id": 1}
    
    result = user_service.get_by_id(1)
    
    assert result == {"id": 1}
    mock_user_repository.get_by_id.assert_called_once_with(1)

@pytest.mark.django_db(transaction=True)
def test_get_user_by_id_not_found(user_service, mock_user_repository):
    mock_user_repository.get_by_id.return_value = None
    testid = 10000
    result = user_service.get_by_id(testid)
    assert result == {'status': 404, 'data': f'Usuario con ID {testid} no encontrado.'}

@pytest.mark.django_db(transaction=True)
def test_create_user(user_service, mock_user_repository, mock_person_repository, mock_serializer):
    mock_person = MagicMock(id=1, email="test@example.com")
    mock_person_repository.create.return_value = mock_person
    mock_user = MagicMock()
    mock_user_repository.create.return_value = mock_user
    mock_serializer.return_value.data = {"id": 1}
    
    data = {"person": {"name": "Test"}}
    result = user_service.create(data)
    
    assert result == {"id": 1}
    mock_person_repository.create.assert_called_once_with({"name": "Test"})
    mock_user_repository.create.assert_called_once_with({"person_id": 1, "email": "test@example.com"})

@pytest.mark.django_db(transaction=True)
def test_update_user(user_service, mock_user_repository, mock_person_repository, mock_serializer):
    mock_user = MagicMock(person=MagicMock(id=1))
    mock_user_repository.get_by_id.return_value = mock_user
    mock_updated_user = MagicMock()
    mock_user_repository.update.return_value = mock_updated_user
    mock_serializer.return_value.data = {"id": 1}
    
    result = user_service.update(1, {"person": {"name": "Updated"}})
    
    assert result == {"id": 1}
    mock_person_repository.update.assert_called_once_with(1, {"name": "Updated"})
    mock_user_repository.update.assert_called_once_with(1, {})

@pytest.mark.django_db(transaction=True)
def test_delete_user(user_service, mock_user_repository, mock_person_repository):
    mock_user = MagicMock(person=MagicMock(id=1))
    mock_user_repository.get_by_id.return_value = mock_user
    
    result = user_service.delete(1)
    
    assert result == {"message": "Usuario con ID 1 eliminado correctamente."}
    mock_user_repository.delete.assert_called_once_with(1)
    mock_person_repository.delete.assert_called_once_with(1)

@pytest.mark.django_db(transaction=True)
def test_get_user_by_email(user_service, mock_user_repository):
    mock_user = MagicMock()
    mock_user_repository.filter_custom.return_value.first.return_value = mock_user
    
    result = user_service.get_by_email("test@example.com")
    
    assert result == mock_user
    mock_user_repository.filter_custom.assert_called_once_with(email="test@example.com")

@pytest.mark.django_db(transaction=True)
def test_get_user_by_token(user_service, mock_user_repository):
    mock_user = MagicMock()
    mock_user_repository.filter_custom.return_value.first.return_value = mock_user
    
    result = user_service.get_by_token("abc123")
    
    assert result == mock_user
    mock_user_repository.filter_custom.assert_called_once_with(token="abc123")

@pytest.mark.django_db(transaction=True)
def test_update_user_not_found(user_service, mock_user_repository):
    mock_user_repository.get_by_id.return_value = None
    
    result = user_service.update(1, {"person": {"name": "Updated"}})
    
    assert result == {'status': 404, 'data': 'Usuario con ID 1 no encontrado.'}

@pytest.mark.django_db(transaction=True)
def test_update_user_without_person_data(user_service, mock_user_repository, mock_person_repository, mock_serializer):
    mock_user = MagicMock(person=MagicMock(id=1))
    mock_user_repository.get_by_id.return_value = mock_user
    mock_serializer.return_value.data = {"id": 1}
    data = {"username": "new_user"}
    
    result = user_service.update(1, data)
    
    assert result == {"id": 1}
    mock_person_repository.update.assert_not_called()
    mock_user_repository.update.assert_called_once_with(1, data)

@pytest.mark.django_db(transaction=True)
def test_delete_user_not_found(user_service, mock_user_repository):
    mock_user_repository.get_by_id.return_value = None
    
    result = user_service.delete(1)
    
    assert result == {'status': 404, 'data': 'Usuario con ID 1 no encontrado.'}

@pytest.mark.django_db(transaction=True)
def test_get_all_users_empty(user_service, mock_user_repository, mock_serializer):
    mock_user_repository.get_all.return_value.select_related.return_value = []
    mock_serializer.return_value.data = []
    
    result = user_service.get_all()
    
    assert result == []
    mock_serializer.assert_called_once_with([], many=True)

@pytest.mark.django_db(transaction=True)
def test_get_user_by_email_not_found(user_service, mock_user_repository):
    mock_user_repository.filter_custom.return_value.first.return_value = None
    
    result = user_service.get_by_email("nonexistent@example.com")
    
    assert result is None

@pytest.mark.django_db(transaction=True)
def test_get_user_by_token_not_found(user_service, mock_user_repository):
    mock_user_repository.filter_custom.return_value.first.return_value = None
    
    result = user_service.get_by_token("invalid_token")
    
    assert result is None