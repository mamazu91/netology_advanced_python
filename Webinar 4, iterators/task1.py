import json


class CountriesIter:
    wiki_page_template = 'https://en.wikipedia.org/wiki/'

    def __init__(self, countries):
        self.countries = countries

    def __iter__(self):
        return self

    def __next__(self):
        if not self.countries:
            raise StopIteration

        country = self.countries.pop(0)
        country_name = country['name']['common']
        return f"{country_name} - {self.wiki_page_template + country_name.replace(' ', '_')}"


def get_countries(file):
    with open(file, 'r', encoding='UTF-8') as countries_file:
        countries = json.load(countries_file)

    return countries


def save_countries(country):
    with open('countries_urls.txt', 'a', encoding='UTF-8') as countries_file:
        countries_file.write(country + '\n')


def main():
    file = 'countries.json'
    countries = get_countries(file)
    countries_iter = CountriesIter(countries)

    for item in countries_iter:
        save_countries(item)


main()
