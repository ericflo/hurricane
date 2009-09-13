from django.contrib.auth.models import User

from socialgraph.models import UserLink
 
def get_people_user_follows(user):
    """
    Returns a ``QuerySet`` representing the users that the given user follows.
    """
    ul = UserLink.objects.filter(from_user=user).values_list('to_user', 
        flat=True)
    return User.objects.filter(id__in=ul, is_active=True)
 
def get_people_following_user(user):
    """
    Returns a ``QuerySet`` representing the users that follow the given user.
    """
    ul = UserLink.objects.filter(to_user=user).values_list('from_user', 
        flat=True)
    return User.objects.filter(id__in=ul, is_active=True)
 
def get_mutual_followers(user):
    """
    Returns a ``QuerySet`` representing the users that the given user follows,
    who also follow the given user back.
    """
    follows = UserLink.objects.filter(from_user=user).values_list('to_user',
        flat=True, is_active=True)
    following = UserLink.objects.filter(to_user=user).values_list('from_user',
        flat=True, is_active=True)
    return User.objects.filter(id__in=set(follows).intersection(set(following)))