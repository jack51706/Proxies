import requests
import time
import os
import threading
import sys
import logging
import random 

urls = ["http://pubproxy.com/api/proxy?format=txt&type=http&limit=20&level=elite&user_agent=true"]
site = "http://httpbin.org/get"

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
				
def banner():
	os.system("cls" if os.name == "nt" else "clear")
	
	print '\033[36m' + '''
    ___o .--.
   /___| |OO|
  /'   |_|  |_    - Downloads proxies from URL and tests each proxie
       (_    _)     
       | |  | 
       | |__|
	''' + '\033[37m'

def proxie_list_load():
	'''
	Load proxie list from file
	'''
	proxylist = open("result.txt").readlines()
	proxylist = [x.strip() for x in proxylist]
	
	return proxylist

def random_useragent():
	'''
	Random User-Agent for our HTTP requests
	'''
	user_agents = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 
				'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
				'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
				'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
				'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',
				'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
				'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02',
				'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (J2ME/23.377; U; en) Presto/2.5.25 Version/10.54',
				'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+',
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246']

	user_agent = random.choice(user_agents)
	user_agent_set = {'User-Agent' : '{}'.format(user_agent)}
	
	return user_agent_set

def proxie_pull():
	'''
	Download proxie list from url and save results
	'''
	for _ in range(1):
		for url in urls:
			try:
				request = requests.get(url,headers=random_useragent(),timeout=7.0)
				if (request.status_code == requests.codes.ok):
					with open("result.txt", 'a') as f:
						f.write(request.content + "\n")
						f.close()
				elif (request.status_code != 200):
					pass
			except Exception as e:
				pass
			except KeyboardInterrupt:
				sys.exit()

def proxie_tests():
	'''
	Load proxies and test them against url using fake User-Agents
	'''
	for proxy in proxie_list_load():
		proxies = {"http": "{}".format(proxy), "https": "{}".format(proxy)}
		try:
			request = requests.get(site,headers=random_useragent(),proxies=proxies,timeout=7.0)
			if (request.status_code == requests.codes.ok):
				with open('result-working.txt', 'a') as f:
					f.write(proxy + "\n")
					f.close()
			elif (request.status_code != 200):
				pass
		except Exception as E:
			pass
		except KeyboardInterrupt:
			sys.exit()

def main():
	banner()
	proxie_pull()
	
	thread = threading.Thread(target=proxie_tests)
	thread.start()

if __name__ == "__main__":
	main()
