import pandas as pd
import json
import requests

API_KEY = 'AIzaSyDn54_wZ1c7iYjD1wxK9OsRnmo81xuuW6k'

with open('Input/goodreads/track_book_origins.json') as f:
	line_content = [json.loads(line) for line in f.readlines()]

df = pd.DataFrame(line_content)
df = df[df.book_name != 'NULL']
df.reset_index(inplace=True, drop=True)

df['authors'] = ''
df['publishedDate'] = ''
df['pageCount'] = ''
df['industryIdentifiers'] = ''
df['price'] = ''
df['currency'] = ''
df['isEbook'] = ''

for i in range(len(df)):

	print(f'Generating response #{i}...', flush=True)

	title = df.book_name[i]
	response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={title}&key={API_KEY}")

	dict = eval(response.text.replace('true', 'True').replace('false', 'False'))

	try:
		df['authors'][i] = dict['items'][0]['volumeInfo']['authors']
	except:
		pass

	try:
		df['publishedDate'][i] = dict['items'][0]['volumeInfo']['publishedDate']
	except:
		pass

	try:
		df['pageCount'][i] = dict['items'][0]['volumeInfo']['pageCount']
	except:
		pass

	try:
		df['industryIdentifiers'][i] = dict['items'][0]['volumeInfo']['industryIdentifiers']
	except:
		pass

	try:
		df['price'][i] = dict['items'][0]['saleInfo']['listPrice']['amount']
		df['currency'][i] = dict['items'][0]['saleInfo']['listPrice']['currencyCode']
	except:
		pass

	try:
		df['isEbook'][i] = dict['items'][0]['saleInfo']['isEbook']
	except:
		pass

	print('DONE')

df.to_csv('Output/books_info.csv', index=False)
