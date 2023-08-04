from flask import Blueprint


api_bp = Blueprint('api', __name__)

# here will be imports from src.pii__api__general.routes
from src.pii__api__auth.routes import generate_xor_token, \
    create_session_tokens, delete_jwt_tokens, update_session_tokens     # noqa: E402
# here list of files from imports

__all__ = (
    'api_bp',
    'generate_xor_token',
    'create_session_tokens',
    'delete_jwt_tokens',
    'update_session_tokens',
)
