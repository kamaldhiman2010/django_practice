import datetime
from  d_query.models import Post
def get_current_year_to_context(request):
    current_datetime = datetime.datetime.now()
    return {
        'current_year': current_datetime.year
    }


def post_count(request):
    count=Post.objects.count()
    return {'post_count':count}