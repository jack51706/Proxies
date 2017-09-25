import requests
import time
import os
import thread
import sys

urls = ["http://pubproxy.com/api/proxy?format=txt&type=http&limit=20&user_agent=true"]		

def banner():
	os.system("cls" if os.name == "nt" else "clear")
	
	print '\033[36m' +'''
    ___o .--.
   /___| |OO|
  /'   |_|  |_    - Downloads proxies via open api and remove duplicates.
       (_    _)     Tests each proxy, saves the working ones in a text file
       | |   \      
       | |__./
	''' + '\033[37m'

def systime():
	'''
	Grab systemtime
	'''
	return time.strftime("%H:%M:%S")

def clean():
	'''
	Attempt to remove the tmp files
	'''
	try:
		if os.path.isfile("http.tmp"):
			os.remove("http.tmp")
		else:
			pass
		if os.path.isfile("http_non_dupes.tmp"):
			os.remove("http_non_dupes.tmp")
		else:
			pass
	except:
		pass

def proxie_sort():
	'''
	Sort the list and remove duplicate proxies
	'''
	print "[{}] Checking for duplicates".format(systime())
	content = open("http.tmp","r").readlines()
	content_set = set(content)
	
	cleandata = open("http_non_dupes.tmp","w")
	for line in content_set:
		cleandata.write(line)
	print "[{}] Duplicates removed".format(systime())

def proxie_pull():
	'''
	Pull proxies via api
	'''
	print "[{}] Pulling proxies".format(systime())
	for _ in range(1):
		for url in urls:
			try:
				r = requests.get(url)
				if (r.status_code == requests.codes.ok):
					print "[{}] API call ({})".format(systime(),'\033[33m' + url + '\033[37m')
					with open('http.tmp', 'a') as f:
						f.write(r.content + "\n")
						f.close()
				elif (r.status_code != 200):
					print "[{}] Error".format(systime())
			except Exception as e:
				print "[{}] Error".format(systime())
			except KeyboardInterrupt:
				print "[{}] Quiting".format(systime())
				sys.exit()

def proxie_tests():
	'''
	Testing all the proxies found in the sorted list
	Auto timeout after 7 seconds.
	'''
	
	proxylist = open("http_non_dupes.tmp").readlines()
	proxylist = [x.strip() for x in proxylist]

	def run():
		for proxy in proxylist:
			sites = "http://google.com","http://facebook.com"
			proxies = {"http": "{}".format(proxy),"https": "{}".format(proxy)}
			for site in sites:
				try:
					r = requests.get(site,proxies=proxies,timeout=7.0)
					if (r.status_code == requests.codes.ok):
						print "[{}] Testing Proxy: {} against ({})".format(systime(),
							'\033[32m' + proxy + '\033[37m',site)
						with open('result.txt', 'a') as f:
							f.write(proxy + "\n")
							f.close()
					elif (r.status_code != 200):
						# Print yellow text if response is bad
						print "[{}] Testing Proxy: {} against ({})".format(systime(),
							'\033[33m'+ proxy + '\033[37m',site)
				except Exception as E:
					# Print red text if response is none
					print "[{}] Testing Proxy: {} against ({})".format(systime(),
						'\033[31m'+ proxy + '\033[37m',site)
				except KeyboardInterrupt:
					print "[{}] Quiting".format(systime())
					sys.exit()

	'''
	Start two threads
	'''
	try:
		thread.start_new_thread(run(),())
		thread.start_new_thread(run(),())
	except TypeError:
		pass

def main():
	'''
	Load all functions
	'''
	banner()
	clean()
	proxie_pull()
	proxie_sort()
	proxie_tests()
	print "[{}] Finished".format(systime())

if __name__ == "__main__":
	main()