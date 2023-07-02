
from bs4 import BeautifulSoup
import requests
import pandas as pd


# Website URL
URL = "https://www.audible.com/search?keywords=book&node=18573211011"

# Getting the HTML
response = requests.get(URL)
website_html = response.text

# Making the Soup
soup = BeautifulSoup(website_html, "html.parser")

# Getting Elements
title_elements = soup.select(".bc-heading .bc-link")
author_elements = soup.select(".authorLabel span")
narrator_elements = soup.select(".narratorLabel span")
length_elements = soup.select(".runtimeLabel span")
release_date_elements = soup.select(".releaseDateLabel span")
language_elements = soup.select(".languageLabel span")
rating_elements = soup.select(".ratingsLabel .bc-pub-offscreen")
price_elements = soup.select(".adblBuyBoxPrice .buybox-regular-price")


# Extracting Values
titles = [title.text for title in title_elements]
authors = [author.text.replace("By:", "").strip() for author in author_elements]
narrators = [narrator.text.replace("Narrated by:", "").strip() for narrator in narrator_elements]
lengths = [length.text.replace("Length:", "").strip() for length in length_elements]
release_dates = [release_date.text.replace("Release date:", "").strip() for release_date in release_date_elements]
languages = [language.text.replace("Language:", "").strip() for language in language_elements]
ratings = [rating.text.replace("out of 5 stars", "").strip() for rating in rating_elements]
prices = [price.text.replace("Regular price:", "").strip()[:6].strip() for price in price_elements]


# Inserting missing values in the webpage
ratings.insert(6, 'Not Rated yet')
ratings.insert(7, 'Not Rated yet')


# Create the dataframe
books = {
    'Title': titles,
    'Author': authors,
    'Narrator': narrators,
    'Length': lengths,
    'Release Date': release_dates,
    'Language': languages,
    "Rating": ratings,
    "Price": prices
}
books_df = pd.DataFrame(books)

# Save the dataframe to a CSV file
books_df.to_csv('books.csv', index=False)

