from scrape import scraper

class guardian:

    remove = []

    @staticmethod
    def get_links_2019() -> list[str]:
        url = "https://www.theguardian.com/news/2019/dec/24/the-best-of-the-long-read-in-2019"
        source = scraper.get(url)

        links = []
        for heading_2 in scraper.find_all('h2', source):
            for link in scraper.find_all('a', heading_2['element']):
                if 'href' in link:
                    links.append(link['href'])
        return links

    @staticmethod
    def get_links_2020() -> list[str]:
        url = "https://www.theguardian.com/news/2020/dec/22/the-best-of-the-long-read-in-2020"
        source = scraper.get(url)

        links = []
        for heading_2 in scraper.find_all('h2', source):
            for link in scraper.find_all('a', heading_2['element']):
                if 'href' in link:
                    links.append(link['href'])
        return links

    
    @staticmethod
    def get_article(link: str) -> str:
        source = scraper.get(link)

        article = []
        for div in scraper.find_all('div', source):
            if 'class' in div and 'article-body-commercial-selector' in div['class']:
                paragraphs = scraper.find_all('p', div['element'])
                marker = paragraphs[0]['class']

        for paragraph in scraper.find_all('p', source):
            if 'class' in paragraph and marker in paragraph['class']:
                article.append(paragraph['text'])

        return ' '.join(article)


if __name__ == '__main__':
    pass