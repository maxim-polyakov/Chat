from misa.dao.base import BaseDAO
from misa.users.models import User


class UsersDAO(BaseDAO):
    model = User