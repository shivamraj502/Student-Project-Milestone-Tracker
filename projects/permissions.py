from functools import wraps

from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect

ROLE_STUDENT = "Student"
ROLE_GUIDE = "Guide"
ROLE_ADMIN = "Admin"
ROLE_NAMES = (ROLE_STUDENT, ROLE_GUIDE)


def ensure_role_groups():
    groups = {}
    for role_name in ROLE_NAMES:
        group, _ = Group.objects.get_or_create(name=role_name)
        groups[role_name] = group
    return groups


def assign_role(user, role_name):
    groups = ensure_role_groups()
    user.groups.remove(*Group.objects.filter(name__in=ROLE_NAMES))
    user.groups.add(groups[role_name])


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_student(user):
    return user.is_authenticated and user.groups.filter(name=ROLE_STUDENT).exists()


def is_guide(user):
    return user.is_authenticated and user.groups.filter(name=ROLE_GUIDE).exists()


def get_user_role(user):
    if not user.is_authenticated:
        return None
    if is_admin(user):
        return ROLE_ADMIN
    if is_student(user):
        return ROLE_STUDENT
    if is_guide(user):
        return ROLE_GUIDE
    return None


def role_required(*roles, allow_admin=True):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("auth_selection")
            if allow_admin and is_admin(request.user):
                return view_func(request, *args, **kwargs)
            if any(
                (role == ROLE_STUDENT and is_student(request.user))
                or (role == ROLE_GUIDE and is_guide(request.user))
                or (role == ROLE_ADMIN and is_admin(request.user))
                for role in roles
            ):
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to access that page.")
            if get_user_role(request.user) is None:
                return redirect("auth_selection")
            return redirect("home")

        return wrapped_view

    return decorator


def admin_required(view_func):
    return role_required(ROLE_ADMIN, allow_admin=True)(view_func)
