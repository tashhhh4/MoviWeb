import requests
import secret

API_URL = 'http://www.omdbapi.com/'

DESIRED_FIELDS = ['Title', 'Year', 'Director', 'Poster']

def clean_year(year_str):
    """ Returns a valid integer year.
    
    For formats mentioning multiple years or a range returns the first year. """
    try:
        year = int(year_str)
        return year
    except ValueError:
        # Return the first 4 digits found in the string
        digits = ''
        for char in year_str:
            if char.isdigit():
                digits += char
                if len(digits) == 4:
                    break
        return int(digits)


def extract_details(result):
    """ A helper function which extracts the desired fields from
    a title search result.
    """
    # Note: Any additional data cleaning (i.e. year:str -> year:int)
    #       should be done here.
    details = []
    for key in DESIRED_FIELDS:
        value = result.get(key, None)
        if value == '':
            value = None
        details.append(value)
    return details


def get_full_details(title, year=None):
    """ Retrieves the exact movie by title match. """
    url = f'{API_URL}?apikey={secret.API_KEY}&t={title}'
    if year is not None:
        url += f'&y={year}'
    response = requests.get(url)
    data = response.json()
    found_movie = data['Response'] == 'True'

    if not found_movie:
        return None

    full_details = extract_details(data)
    return full_details


def get_movie_details(title_search, year=None):
    """ Searches OMDB API for the best matching movie.
    
    Movies are searched by `title` first, and then filtered for the closest matching `year`, if provided.
    If no movie is found, returns None.
    """
    url = f'{API_URL}?apikey={secret.API_KEY}&s={title_search}'
    response = requests.get(url)
    data = response.json()

    found_movies = data['Response'] == 'True'

    if not found_movies:
        return None

    results = data['Search']

    if year is None:
        return get_full_details(results[0]['Title'])

    search_year = clean_year(year)

    best_result = results[0]    
    for result in results:
        result_year = clean_year(result['Year'])
        best_result_year = clean_year(best_result['Year'])
        if abs(result_year - search_year) < abs(best_result_year - search_year):
            best_result = result
    return get_full_details(best_result['Title'], year=best_result['Year'])