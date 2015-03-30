import unicodedata

from haystack.forms import HighlightedSearchForm


class SimpleSearchForm(HighlightedSearchForm):
    def search(self):
        sqs = super(SimpleSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        query = unicodedata.normalize('NFD', self.cleaned_data['q']).encode('ascii', 'ignore').decode(encoding='utf-8')
        sqs = self.searchqueryset.auto_query(query).order_by('-codigo')

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
