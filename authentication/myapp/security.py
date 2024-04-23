from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS
from main import session
from models import User

ACL = {
    
    'admin': {'view','create','edit','delete'},
    'librarian':{'view','create','delete'},
    'student': {'view'},
    'guest_user': {'view'}
}

class RootACL:
    def __init__(self, request):
        self.request = request
        
    def get_roles_for_user(self, user_id):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            return [role.name for role in user.roles]
        else:
            return []

    @property
    def __acl__(self):
        
        user_id = self.request.authenticated_userid
        if user_id is None:
            return []
        user_roles = self.get_roles_for_user(user_id)
        
        acl = [(Allow, Authenticated, 'view')]  # Allow authenticated users to view by default
        
        for role in user_roles:
            if role in ACL:
                acl.extend([(Allow, Authenticated, perm) for perm in ACL[role]])
                return acl
            else:
                return []


