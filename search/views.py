from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Q
from django.views.generic import ListView

from commentsapp.models import CommentsBranch
from mainapp.models import Article, Hub
from usersapp.models import GeekHubUser

TARGET_TYPES = {
    'posts': Article,
    'hubs': Hub,
    'users': GeekHubUser,
    'comments': CommentsBranch,
}


class Search(ListView):
    template_name = 'search/search_page.html'
    context_object_name = 'targets'
    paginate_by = 5

    def get_queryset(self):
        queryset = Article.objects.none()
        print(self.request.GET)
        query_string = self.request.GET.get('q')
        target_type = self.request.GET.get('target_type')
        if query_string and target_type in TARGET_TYPES.keys():
            if 'sqlite' in settings.DATABASES['default']['ENGINE']:
                queryset = Search.search_in_sqlite(query_string, target_type)
            if 'postgre' in settings.DATABASES['default']['ENGINE']:
                queryset = Search.search_in_postgres(query_string, target_type)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Search, self).get_context_data()
        context['title'] = 'Поиск'
        context['q'] = self.request.GET.get('q')
        context['target_type'] = self.request.GET.get('target_type')
        return context

    @staticmethod
    def search_in_sqlite(query_string, target_type):
        """ Partial search in development DB. """
        # TODO доделать посик по тестовой БД
        queryset = Article.objects.filter(is_deleted=False)
        for word in query_string.split():
            q_list = Q()
            q_list |= Q(title__icontains=word)
            q_list |= Q(contents_ck__icontains=word)
            q_list |= Q(contents_md__icontains=word)
            queryset = Article.objects.filter(is_published=True).filter(q_list)
        return queryset

    @staticmethod
    def search_in_postgres(query_string, target_type):
        """ Full-text search in postgres DB with vector and rank. Used for deploy settings. """
        search_query = SearchQuery('')
        for word in query_string.split():
            search_query |= SearchQuery(word)
        model = TARGET_TYPES[target_type]
        search_vector = Search.set_search_vector(model)
        # queryset = model.objects.annotate(search=search_vector).filter(search=search_query)
        # todo деделать поиск по частичным совпадениям в словах
        search_rank = SearchRank(search_vector, search_query)
        queryset = model.objects.annotate(rank=search_rank).order_by('-rank')

        return queryset

    @staticmethod
    def set_search_vector(model):
        """ Set search fields depend model. """
        if issubclass(model, Article):
            return SearchVector('title', 'contents_ck', 'contents_md')
        if issubclass(model, Hub):
            return SearchVector('name')
        if issubclass(model, GeekHubUser):
            return SearchVector('username')
        if issubclass(model, CommentsBranch):
            return SearchVector('description')
