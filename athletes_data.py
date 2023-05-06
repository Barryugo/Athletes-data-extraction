import streamlit as st
import requests_html
import pandas as pd
import numpy as np
import asyncio
import signal

# Define a signal handler function to handle SIGINT signals
def sigint_handler():
    print("SIGINT received, stopping event loop")
    loop = asyncio.get_event_loop()
    loop.stop()

# Register the signal handler function to handle SIGINT signals
signal.signal(signal.SIGINT, sigint_handler)

# Define your scrape function with the async keyword
async def scrape(athlete_name):
    url = f'https://en.wikipedia.org/wiki/{athlete_name}'
    session = requests_html.AsyncHTMLSession()
    response = await session.get(url)

    if response.status_code == 200:
        await response.html.arender()
        infobox = response.html.find('.infobox.vcard', first=True)

        if infobox is not None:
            rows = infobox.find('tr')
            name = ''
            height = ''
            weight = ''

            for row in rows:
                if row.find('.fn'):
                    name_cell = row.find('.fn', first=True)
                    name = name_cell.text.strip()
                elif row.find('.infobox-label', containing='Height'):
                    height_cell = row.find('.infobox-data', first=True)
                    height = height_cell.text.strip()
                elif row.find('.infobox-label', containing='Weight'):
                    weight_cell = row.find('.infobox-data', first=True)
                    weight = weight_cell.text.strip()

            return {'Name': name, 'Height': height, 'Weight': weight}

        else:
            st.error('No infobox found')

    else:
        st.error(f'Wikipedia page not found for {athlete_name}')

    return None

# Define an async function called main and put your Streamlit code inside it
def main(): 
    st.title('Athlete Data Scraper')

    name = st.text_input('Enter an athlete name')
    if st.button('Scrape'):
        try:
            data = asyncio.run(scrape(name))
            st.json(data)
        except Exception as e:
            st.write(f'Error: {e}')
            st.write('Athlete not found!')
