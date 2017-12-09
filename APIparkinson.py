import requests
import json



polo_link = requests.get('https://poloniex.com/public?command=returnTicker')
polo_data = json.loads(polo_link.text)



trex_link = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
trex_data = json.loads(trex_link.text)
trex_data = trex_data['result']
#print (trex_data)

crypto_link = requests.get('https://www.cryptopia.co.nz/api/GetMarkets')
crypto_data = json.loads(crypto_link.text)
crypto_data = crypto_data['Data']
#print (crypto_data)


def spread(exch1Last, exch2Last, name1, name2, key):
	diff = abs(float(exch1Last) - float(exch2Last))
	smallest = min(float(exch2Last), float(exch1Last))
	spread = (diff/smallest)*100
	if spread > 2:
		data = (key, spread, "%", name2, float(exch2Last), name1, float(exch1Last))
		print("%-10s: Spread= %6.2f%s, %s= %-12.8f, %s= %-12.8f" % data)


def trex_polo():
	for trex_ticker in trex_data:
		key = trex_ticker['MarketName'].replace('-', '_')
		if key in polo_data:
			trex_last = trex_ticker['Last']
			polo_last = polo_data[key]['last']
			spread(trex_last, polo_last, 'Trex', 'Polo', key)
				
def crypto_polo():
	for crypto_ticker in crypto_data:
		keyArr = crypto_ticker['Label'].split('/')
		key = keyArr[1] + '_' + keyArr[0]
		if key in polo_data:
			crypto_last = crypto_ticker['LastPrice']
			polo_last = polo_data[key]['last']
			spread(crypto_last, polo_last, 'Crypto', 'Polo', key)
			
			
def main():
	while True:
		usr_input = input('''
		Hello. 
		Choose '1' for the spread of Bittrex and Poloniex.
		Choose '2' for the spread of Cryptopia and Poloniex.
		''')
		if usr_input == '1':
			trex_polo()
		
		
#main()
crypto_polo()



