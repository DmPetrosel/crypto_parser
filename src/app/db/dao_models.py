from app.db.models import *
from app.db.dao import *

class UserDAO(BaseDAO):
    _model = User
