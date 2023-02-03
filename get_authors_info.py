import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

df = pd.read_csv('Output/books_info.csv')

df['born'] = ''
df['died'] = ''

for i in range(len(df)):

	print(f'Generating response #{i}... of {len(df)}', flush=True)

	query = eval(df['authors'][i])[0].replace(' ', '+')

	driver = webdriver.Firefox()

	driver.get(f"https://www.google.com/search?q={query}+author")

	try:
		accepteren = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div')
		sleep(0.5)
		accepteren.click()
	except:
		pass

	try:
		english = driver.find_element(By.XPATH, '/html/body/div[8]/div/div[7]/div[1]/div/div/div[2]/div/a[2]')
		sleep(0.5)
		english.click()
	except:
		pass

	try:
		born = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[11]/div[5]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div')
		df['born'][i] = born.text
	except:
		pass

	try:
		died = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[11]/div[5]/div[2]/div/div/div[2]/div/div/div/div[3]/div/div/div')
		df['died'][i] = died.text
	except:
		pass

	driver.quit()

df.to_csv('Output/books_info.csv', index=False)