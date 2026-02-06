import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import date, datetime
import uuid

from src.ventio_api.services.auth_service import AuthService
from src.ventio_api.api.schema.user import UserSignup
from src.ventio_api.models.user import User
# ADDED: NotFoundException
from src.ventio_api.exceptions import InvalidCredentials, UsernameAlreadyExists, NotFoundException
from src.ventio_api.infrastructure.auth.security import get_password_hash

# --- FIXTURES ---
@pytest.fixture
def mock_user_db():
    db = MagicMock()
    db.get_by_username = AsyncMock()
    db.insert = AsyncMock()
    db.collection = MagicMock()
    return db

@pytest.fixture
def auth_service(mock_user_db):
    return AuthService(user_db=mock_user_db)

# --- THE TESTS ---

@pytest.mark.asyncio
async def test_signup_success(auth_service, mock_user_db):
    """Test that valid input creates a user and returns a token."""
    
    # 1. GIVEN: Valid signup data
    signup_data = UserSignup(
        name="Test User",
        username="newuser",
        password="securepass",
        birthday=date(2000, 1, 1),
        gender="M"
    )
    
    # --- FIX START ---
    # MOCK: When code calls get_by_username, FORCE it to say "Not Found"
    mock_user_db.get_by_username.side_effect = NotFoundException()
    # --- FIX END ---
    
    # Mock: Insert returns a valid User object
    mock_user_db.insert.return_value = None 
    
    # 2. WHEN: We call signup
    result = await auth_service.signup(signup_data)

    # 3. THEN: We expect tokens back
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    
    # Verify the code tried to save to the DB
    mock_user_db.insert.assert_called_once()

@pytest.mark.asyncio
async def test_signup_duplicate_username(auth_service, mock_user_db):
    """Test that duplicate usernames block the signup."""
    
    signup_data = UserSignup(
        name="Test", username="taken_user", password="123", birthday=date(2000,1,1), gender="M"
    )

    # MOCK: DB finds a user (returns a Success/Mock object)
    mock_user_db.get_by_username.return_value = {"username": "taken_user"}

    # WHEN/THEN: Expect an error
    with pytest.raises(UsernameAlreadyExists):
        await auth_service.signup(signup_data)

@pytest.mark.asyncio
async def test_signin_success(auth_service, mock_user_db):
    """Test login with correct password."""
    
    real_password = "mypassword"
    hashed_pw = get_password_hash(real_password)
    
    existing_user = User(
        user_id=uuid.uuid4(),
        name="Login User",
        username="login_test",
        pass_hash=hashed_pw,
        birthday=datetime(1990, 1, 1),
        age=30,
        gender="F",
        bio="",
        created_at=datetime.utcnow()
    )
    
    # Mock: db.get_by_username returns this user
    mock_user_db.get_by_username.return_value = existing_user

    # WHEN: Login with CORRECT password
    result = await auth_service.signin("login_test", real_password)

    # THEN: Success
    assert "access_token" in result

@pytest.mark.asyncio
async def test_signin_wrong_password(auth_service, mock_user_db):
    """Test login with wrong password."""
    
    hashed_pw = get_password_hash("correct_password")
    existing_user = User(
        user_id=uuid.uuid4(),
        name="User",
        username="user",
        pass_hash=hashed_pw,
        birthday=datetime(1990,1,1),
        age=20,
        gender="M",
        bio="",
        created_at=datetime.utcnow()
    )
    mock_user_db.get_by_username.return_value = existing_user

    with pytest.raises(InvalidCredentials):
        await auth_service.signin("user", "wrong_password")