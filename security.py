from werkzeug.security import safe_str_cmp
from models.userModel import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


# Whenever they request an endpoint, where they need to be authenticated,
# we use the identity method, so we get a pay load coming from the request,
# and in that pay load, we get the identity, which is the user id,
# and there we retrieve the user object using the id mapping,
# and if that does match, then we assume that the jwt token was correct,
# and the user therefore knows that he is logged in.

def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
