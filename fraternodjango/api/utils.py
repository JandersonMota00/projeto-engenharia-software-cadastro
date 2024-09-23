

from django.contrib.auth.models import User, Group;


def get_user_type(user: User) -> str:

    # FIXME Isso só vai funcionar enquanto os user tiverem somente um grupo
    user_group = user.groups.first()
    
    role: str = '';
    
    if user_group:
        if user_group.name in ['Paciente', 'Atendente', 'Diretor']:
            role = user_group.name;
    else:
        role = 'none'

    return role
