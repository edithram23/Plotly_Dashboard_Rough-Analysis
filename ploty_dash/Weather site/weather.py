from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import os

def get_weatherinfo():
                    if os.path.exists('webpage.html'):
                        os.remove('webpage.html')
    
                    edge_driver_path = 'C:/Users/edith/Downloads/edgedriver/msedgedriver.exe'  
                    edge_options = Options()
                    edge_options.add_argument('--headless') 
                    service = Service(edge_driver_path)
                    driver = webdriver.Edge(service=service, options=edge_options)

                    url = 'https://openweathermap.org/city/1264527' 
                    driver.get(url)

            
                    import time
                    time.sleep(5)

                    html_content = driver.page_source

                    file_path = 'webpage.html'  
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(html_content)

                    driver.quit()


                    from bs4 import BeautifulSoup

                    file_path = 'webpage.html'  

                    with open(file_path, 'r', encoding='utf-8') as file:
                        html_content = file.read()

                    soup = BeautifulSoup(html_content, 'html.parser')

                   # cur_time = soup.find('span',class_='orange-text').text
                    try:
                        current_temp = soup.find('span', class_='heading').text
                    except AttributeError:
                        current_temp = None

                    try:
                        description = soup.find('div', class_='bold').text
                    except AttributeError:
                        description = None

                    try:
                        wind_speed = soup.find('div', class_='wind-line').text.strip()
                    except AttributeError:
                        wind_speed = None

                    try:
                        humidity = soup.find('span', string='Humidity:').next_sibling
                    except AttributeError:
                        humidity = None

                    try:
                        uv = soup.find('span', string='UV:').next_sibling
                    except AttributeError:
                        uv = None

                    try:
                        dew_point = soup.find('span', string='Dew point:').next_sibling
                    except AttributeError:
                        dew_point = None

                    try:
                        visibility = soup.find('span', string='Visibility:').next_sibling
                    except AttributeError:
                        visibility = None

                    try:
                        date_time = soup.find('span', class_='orange-text').text
                    except AttributeError:
                        date_time = None


                    os.remove('webpage.html')
                    return {'date_time':date_time, 
                            'current_temp': current_temp,
                            'description': description.lower(),
                            'wind_speed': wind_speed,
                            'humidity': humidity,
                            'uv': uv,
                            'dew_point': dew_point,
                            'visibility': visibility
                        }

print(get_weatherinfo())