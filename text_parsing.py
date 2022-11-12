import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
from model_pipeline import json_load

MAIN_URL = 'https://www.imdb.com'
DATA_SAVE_PATH = json_load('paths.json')['DATA_SAVE_PATH']  # here we will save the .csv file with text and label

def get_html_data(url: str) -> BeautifulSoup:
    """The function returns the result of sending a request by url"""
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html.parser')


def get_links(main_url: str) -> list:
    """The function of getting links to movies"""
    current_url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=2000,&sort=year,desc'
    movie_links = []  # here we will save all links to the movie
    movie_count = 0
    while True:  # processing movies by current_url, after processing, we change current_url
        soup = get_html_data(current_url)
        movies = soup.find('div', class_='lister list detail sub-list').findAll('div', class_='lister-item mode-advanced')
        for movie in movies:  # for the current url, we get all the movies on the page
            link = movie.find('div', class_="lister-top-right").find('div', class_='ribbonize').get('data-tconst')
            movie_links.append(main_url + '/title/' + link)
            movie_count += 1

        sleep(1.5)  # in order not to load the server
        next_page = soup.find('div', class_='desc').find('a', class_="lister-page-next next-page").get('href')
        if movie_count > 2000:
            return movie_links
        else:
            current_url = main_url + next_page


def get_main_data(all_movies: list) -> pd.DataFrame:
    """Function for getting basic information: review and label for all movies"""
    def data_pulling(blocks: list) -> None:
        """Function for getting reviews and labels for a movie"""
        nonlocal texts_and_labels
        for block in blocks:
            try:
                current_block = block.find('div', class_='review-container').find('div', class_='lister-item-content')
                text_review = current_block.find('div', class_='content').find('div', class_='text show-more__control').text
                label_review = int(current_block.find('div', class_='ipl-ratings-bar').find('span', class_='rating-other-user-rating').find('span').text)
                df_review = pd.DataFrame(data=[[text_review, label_review]], columns=['text', 'label'])
                texts_and_labels = pd.concat([texts_and_labels, df_review], ignore_index=True)
            except AttributeError:
                continue

    texts_and_labels = pd.DataFrame(data=[], columns=['text', 'label'])
    all_reviews_url = [movie + '/reviews' for movie in all_movies]
    for reviews_url in all_reviews_url:
        soup = get_html_data(reviews_url)
        all_blocks = soup.find('div', class_='lister-list')
        first_blocks = all_blocks.findAll('div', class_="lister-item mode-detail imdb-user-review collapsable")
        second_blocks = all_blocks.findAll('div', class_='lister-item mode-detail imdb-user-review with-spoiler')
        data_pulling(first_blocks)
        data_pulling(second_blocks)
        sleep(1)  # in order not to load the server
    return texts_and_labels


if __name__ == "__main__":
    LINKS = get_links(MAIN_URL)
    TEXTS_AND_LABELS = get_main_data(LINKS)
    TEXTS_AND_LABELS.to_csv(DATA_SAVE_PATH, encoding='utf8')