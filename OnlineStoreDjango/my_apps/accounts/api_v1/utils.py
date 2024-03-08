from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound
from ..models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_user_by_email(email: str) -> User | None:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise NotFound(detail="User not found")
    return user


def create_user(email: str, password: str, first_name=None, last_name=None) -> User:
    """Create a new auth user """

    user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
    return user
