from django.test import TestCase
from pdl.management.commands.scraper import Command


class ScrapperTest(TestCase):
    def setUp(self):
        self.congreso_url = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/' \
                       'CLProLey2011.nsf/PAporNumeroInverso?OpenView'
    def test_url1(self):
        """Test when user does not enter any argument for the scrapper."""
        options = dict(full_scrapping = False)
        scrapper_cmd = Command()
        scrapper_cmd.handle(**options)
        expected = self.congreso_url
        self.assertEqual(expected, scrapper_cmd.urls[0])

    def test_url2(self):
        """Test when user enter argument for full scrapping, since 20110727."""
        options = dict(full_scrapping = True)
        scrapper_cmd = Command()
        scrapper_cmd.handle(**options)
        expected_last = self.congreso_url + '&Start=3800'
        self.assertEqual(expected_last, scrapper_cmd.urls[-1])

    def test_get(self):
        scrapper_cmd = Command()
        soup = scrapper_cmd.get("http://www.bbc.com/news/")
        result = soup.title.get_text()
        expected = "BBC News - Home"
        self.assertEqual(result, expected)
