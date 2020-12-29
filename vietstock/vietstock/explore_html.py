from bs4 import BeautifulSoup

with open('index.html', 'rb') as f:
    soup = BeautifulSoup(f, 'html.parser')

h = soup.find_all('span', class_='txt-green price')
print(h[0].text.strip())

