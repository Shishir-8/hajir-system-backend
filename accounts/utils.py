from django.contrib.auth.models import Group


def assign_user_group(user):
    group = Group.objects.get(name=user.role)
    user.groups.add(group)