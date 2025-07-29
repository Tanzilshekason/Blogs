# liveblog/templatetags/rating_tags.py
from django import template

register = template.Library()

@register.filter
def user_rating(post, user):
    return post.ratings.filter(user=user).first()
