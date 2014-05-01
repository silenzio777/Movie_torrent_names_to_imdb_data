import urllib2

def movie_name_to_imdb_page(query) :

	user_agent = 'Mozilla/4.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

	url = "https://www.google.com/search?hl=en&safe=off&q=Monkey&q=%s" %(query)
	headers={'User-Agent':user_agent,} 
	request=urllib2.Request(url,None,headers) 
	response = urllib2.urlopen(request)
	
	page_source = response.read()
	imdb_url_pos = page_source.find("http://www.imdb.com/title/")
	if (imdb_url_pos != -1) :
		imdb_url = page_source[imdb_url_pos:imdb_url_pos+36]
	else :
		return None
		
	print imdb_url
	return imdb_url