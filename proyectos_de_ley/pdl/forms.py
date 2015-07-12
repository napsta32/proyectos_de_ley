import unicodedata

from haystack.forms import SearchForm


class SimpleSearchForm(SearchForm):
    def search(self):
        sqs = super(SimpleSearchForm, self).search()
        print(">>>sqws", sqs)

        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        """
        original = self.cleaned_data['q']
        modified = unicodedata.normalize('NFKD', original).encode('ascii', 'ignore')
        query = modified.decode(encoding='utf-8')
        print(">>>>>query form", query)
        sqs = self.searchqueryset.auto_query(query).order_by('-codigo')
        """

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
