from .permissions import get_user_role, is_admin, is_guide, is_student


def auth_role(request):
    user = request.user
    return {
        "user_role": get_user_role(user),
        "is_student_user": is_student(user),
        "is_guide_user": is_guide(user),
        "is_admin_user": is_admin(user),
    }
