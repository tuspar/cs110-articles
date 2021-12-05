from scrape import scraper

class newyorker:

    remove = [8, 3]

    @staticmethod
    def get_links_2019() -> list[str]:
        '''
        Returns a list of the top 100 TNY articles from 2019
        '''
        url = f"https://www.newyorker.com/culture/2019-in-review/the-top-twenty-five-new-yorker-stories-of-2019"
        source = scraper.get(url)

        links = []
        for div in scraper.find_all('div', source):
            if 'class' in div and 'heading-h4' in div['class']:
                for link in scraper.find_all('a', div['element']):
                    links.append(link['href'])
        return links


    @staticmethod
    def get_links_2020() -> list[str]:
        '''
        Returns a list of the top 100 TNY articles from 2019
        '''
        url = f"https://www.newyorker.com/culture/2020-in-review/the-top-twenty-five-new-yorker-stories-of-2020"
        source = scraper.get(url)

        links = []
        for div in scraper.find_all('div', source):
            if 'class' in div and 'heading-h4' in div['class']:
                for link in scraper.find_all('a', div['element']):
                    links.append(link['href'])
        return links

    @staticmethod
    def get_article(link: str) -> str:
        '''
        Returns the text in a TNY Live/Regular Story written between 2020-2019
        '''
        source = scraper.get(link)
        article = []

        for paragraph in scraper.find_all('p', source):
            if 'class' in paragraph and 'paywall' in paragraph['class']:
                    article.append(paragraph['text'])
        
        return ' '.join(article)

if __name__ == '__main__':
    pass