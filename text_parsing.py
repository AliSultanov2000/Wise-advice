import pandas as pd
import requests
import pandas
from bs4 import BeautifulSoup
from time import sleep

MAIN_URL = 'https://www.imdb.com'

def get_links(main_url: str):
    """Получает ссылки на 2500 фильмов"""
    current_url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=2500,&sort=year,desc'
    movie_links = set()
    while True:
        r = requests.get(current_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        movies = soup.find('div', class_='lister list detail sub-list').findAll('div', class_='lister-item mode-advanced')
        for movie in movies:
            link = movie.find('div', class_="lister-top-right").find('div', class_='ribbonize').get('data-tconst')
            movie_links.add(main_url + '/title/' + link)
            print(main_url + '/title/' + link)

        sleep(0.8)
        next_page = soup.find('div', class_='desc').find('a', class_="lister-page-next next-page").get('href')
        print(len(movie_links))
        if next_page is not None:
            current_url = main_url + next_page
        else:
            return movie_links


def get_text_information(all_movies) -> pd.DataFrame:
    """Функция, которая по ссылкам на фильмы будет парсить отзыв"""
    max_movie_reviews = 20
    text_data = pd.DataFrame()
    all_reviews = [movie + '/reviews' for movie in all_movies]  # здесь храним 2500 страниц ссылок на reviews к фильму
    for review in all_reviews:
        r = requests.get(review)
        soup = BeautifulSoup(r.text, 'html.parser')
        all_blocks = soup.find('div', class_='lister-list')
        first_blocks = all_blocks.findAll('div', class_="lister-item mode-detail imdb-user-review collapsable")
        for block in first_blocks:
            print(block.find('div', class_='review-container').find('div', class_='lister-item-content').find('div', class_='content').find('div', class_='text show-more__control').text)
            print('*'*50)

        second_blocks = all_blocks.findAll('div', class_='lister-item mode-detail imdb-user-review with-spoiler')
        for block in second_blocks:
            pass


        sleep(0.7)

    return text_data



get_text_information(['https://www.imdb.com/title/tt8009428'])
# print(block.find('div', class_='review-container').find('div', class_='lister-item-content').find('div',class_='content').find('div', class_='text show-more__control clickable'))



# if __name__ == "__main__":
#     LINKS = get_links(MAIN_URL)
#     TEXT_DATA = get_text_information(LINKS)  # здесь храним pd.DataFrame
    # сохранить pd.dataframe в формате .csv на локальном компьютере




# CURRENT_URL = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=2500,&sort=year,desc'
# r = requests.get(CURRENT_URL)
# SOUP = BeautifulSoup(r.text, 'html.parser')
# print(MAIN_URL + SOUP.find('div', class_='desc').find('a').get('href'))
# print(len(SOUP.find('div', class_='lister list detail sub-list').findAll('div', class_="lister-item mode-advanced")))








