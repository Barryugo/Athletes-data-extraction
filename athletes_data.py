import streamlit as st
import requests_html
import pandas as pd
import numpy as np
import asyncio



# Define your scrape function with the async keyword


async def scrape(athlete_name):
    # Construct the Wikipedia URL from the athlete name
    url = f'https://en.wikipedia.org/wiki/{athlete_name}'
    # Create an AsyncHTMLSession object and send a GET request to the URL
    session = requests_html.AsyncHTMLSession()
    response = await session.get(url)
    # Render the HTML content of the page using requests_html
    await response.html.arender()
    # Find the infobox table on the page using a CSS selector
    infobox_table = response.html.find('.infobox.vcard', first=True)
    # Find the rows in the infobox table
    rows = infobox_table.find('tr')
    # Initialize variables to store name, height and weight
    name = ''
    height = ''
    weight = ''
    # Loop through the rows to find the name, height and weight using CSS selectors
    for row in rows:
        # Find the row containing the name information
        if row.find('.fn'):
            # Get the first cell in the row, which contains the name value
            name_cell = row.find('.fn', first=True)
            name = name_cell.text.strip()
        # Find the row containing the height information
        elif row.find('.infobox-label', containing='Height'):
            # Get the second cell in the row, which contains the height value
            height_cell = row.find('.infobox-data', first=True)
            height = height_cell.text.strip()
        # Find the row containing the weight information
        elif row.find('.infobox-label', containing='Weight'):
            # Get the second cell in the row, which contains the weight value
            weight_cell = row.find('.infobox-data', first=True)
            weight = weight_cell.text.strip()
    # Return a dict with name, height and weight as keys and values
    return {'Name': name, 'Height': height, 'Weight': weight}

# Define an async function called main and put your Streamlit code inside it


def main(): 
    asyncio.run(async_main())

async def async_main(): 
    st.title('Athlete Data Scraper')

    name = st.text_input('Enter an athlete name')
    if st.button('Scrape'):
        try: 
            data = await scrape(name)
            st.json(data)
        except Exception as e:
            st.write('Athlete not found!')

main()
