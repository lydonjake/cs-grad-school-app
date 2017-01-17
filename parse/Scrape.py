"""Scrapes computer science data from grad-cafe.com

Credit to Debarghya Das for the idea. https://github.com/deedy/gradcafe_data"""

import requests

__author__ = "Jacob Lydon"
__copyright__ = "Copyright 2017"
__credits__ = ["Debarghya Das"]

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Jacob Lydon"
__email__ = "jlydon001@regis.edu"
__status__ = "Development"

num_pages = 2

for page in range(1, 2):
    retrieved_data = requests.get("""http://thegradcafe.com/survey/index.php?q="computer+science"&t=a&pp=250&o=d&p="""
                                  + str(page), headers={'User-Agent': 'Mozilla/5.0'})

    with open("./scraped/" + str(page) + ".html", 'wb') as file_open:
        file_open.write(retrieved_data.text.encode('UTF-8'))
