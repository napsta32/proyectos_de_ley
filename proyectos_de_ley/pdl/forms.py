from haystack.forms import HighlightedSearchForm


class SimpleSearchForm(HighlightedSearchForm):
    def search(self):
        sqs = super(SimpleSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q']).order_by('-date')
        print(">>>>>>cleaned data", sqs)

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
