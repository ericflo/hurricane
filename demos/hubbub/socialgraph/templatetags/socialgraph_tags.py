from django import template

from socialgraph.util import get_people_user_follows, get_people_following_user

def do_dict_entry_for_item(parser, token):
    """
    Given an object and a dictionary keyed with object ids - as returned by the
    ``friends_for_user`` template tag - retrieves the value for the given object
    and stores it in a context variable, storing ``None`` if no value exists 
    for the given object.
 
    Example usage::
 
        {% dict_entry_for_item user.username from friend_dict as friend %}
    """
    bits = token.contents.split()
    if len(bits) != 6:
        raise template.TemplateSyntaxError(
            "'%s' tag takes exactly five arguments" % bits[0])
    if bits[2] != 'from':
        raise template.TemplateSyntaxError(
            "Second argument to '%s' tag must be 'from'" % bits[0])
    if bits[4] != 'as':
        raise template.TemplateSyntaxError(
            "Fourth argument to '%s' tag must be 'as'" % bits[0])
    return DictEntryForItemNode(bits[1], bits[3], bits[5])
 
class DictEntryForItemNode(template.Node):
    def __init__(self, item, dictionary, context_var):
        self.item = item
        self.dictionary = dictionary
        self.context_var = context_var
 
    def render(self, context):
        try:
            dictionary = template.resolve_variable(self.dictionary, context)
            item = template.resolve_variable(self.item, context)
        except template.VariableDoesNotExist:
            return ''
        context[self.context_var] = dictionary.get(item, None)
        return ''
 
def do_friends_for_user(parser, token):
    """
    Gets the users that the given user follows, and saves that into a
    dictionary keyed by username.
    
    Usage:
    
        {% friends_for_user user as friend_dict %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError(
            "'%s' tag takes exactly four arguments" % (bits[0],))
    if bits[2] != 'as':
        raise template.TemplateSyntaxError(
            "Fourth argument to '%s' tag must be 'as'" % (bits[0],))
    return UserLinksForUserNode(bits[1], bits[3], get_people_user_follows)

def do_followers_for_user(parser, token):
    """
    Gets the users that follow the given user, and saves that into a
    dictionary keyed by username.

    Usage:

        {% followers_for_user user as friend_dict %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError(
            "'%s' tag takes exactly four arguments" % (bits[0],))
    if bits[2] != 'as':
        raise template.TemplateSyntaxError(
            "Fourth argument to '%s' tag must be 'as'" % (bits[0],))
    return UserLinksForUserNode(bits[1], bits[3], get_people_following_user)

class UserLinksForUserNode(template.Node):
    def __init__(self, user, context_var, func):
        self.user = user
        self.context_var = context_var
        self.func = func
 
    def render(self, context):
        try:
            user = template.resolve_variable(self.user, context)
        except template.VariableDoesNotExist:
            return ''
        context[self.context_var] = dict([(u.username, u) for u in
            self.func(user)])
        return ''
 
register = template.Library()
register.tag('dict_entry_for_item', do_dict_entry_for_item)
register.tag('friends_for_user', do_friends_for_user)
register.tag('followers_for_user', do_followers_for_user)