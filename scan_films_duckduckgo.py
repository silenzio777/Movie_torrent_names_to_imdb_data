
def movie_name_to_imdb_page(query) :
	import duckduckgo
	print query
	r = duckduckgo.query(query)
	
	print r.results
	#imdb_url= r.results[0].url
	print imdb_url
	return imdb_url