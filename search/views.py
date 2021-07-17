from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Q
from django.views.generic import ListView

from mainapp.models import Article


class Search(ListView):
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = Article.objects.none()
        if self.request.GET.get('q'):
            if 'sqlite' in settings.DATABASES['default']['ENGINE']:
                queryset = self.search_in_sqlite()
            if 'postgre' in settings.DATABASES['default']['ENGINE']:
                queryset = self.search_in_postgres()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Search, self).get_context_data()
        context['title'] = 'Поиск'
        context['search'] = True
        context['q'] = self.request.GET.get('q')
        return context

    def search_in_sqlite(self):
        queryset = not Article.objects.filter(is_deleted=False)
        for word in self.request.GET.get('q').split():
            q_list = Q()
            q_list |= Q(title__icontains=word)
            q_list |= Q(contents_ck__icontains=word)
            q_list |= Q(contents_md__icontains=word)
            queryset = Article.objects.filter(q_list)
        return queryset

    def search_in_postgres(self):
        search_query = SearchQuery('')
        for word in self.request.GET.get('q').split():
            search_query |= SearchQuery(word)
        search_vector = SearchVector('title', 'contents_ck', 'contents_md')
        search_rank = SearchRank(search_vector, search_query)
        queryset = Article.objects.annotate(rank=search_rank).order_by('-rank')
        return queryset
