from my_bookshelf.common.forms import SearchForm


class SearchBarMixin:
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            queryset = self.queryset.filter(title__icontains=query)
        else:
            queryset = self.queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        context['query'] = self.request.GET.get('query')
        return context
