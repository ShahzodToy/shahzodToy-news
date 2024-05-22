from django import template
from ..models import Post,Category
from django.core.paginator import Paginator
from django.db.models import Count
register = template.Library()


@register.inclusion_tag('blog/footer.html')
def footr_stat():
    cat = Category.objects.all()
    cat_count = Category.objects.annotate(post_count=Count('cat_post')).values('name', 'post_count') 
    return {"cat":cat,'cat_count':cat_count}

