import os 
import sys # argv
import urllib2
import re
import time #sleep

	
def parse_imdb_page(url) :
	
	if url == None :
		return
	
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

	headers={'User-Agent':user_agent,} 
	request=urllib2.Request(url,None,headers) 
	response = urllib2.urlopen(request)

		
	page_source = response.read()
	
	#Movie Rating
	rating_query = '<div class="titlePageSprite star-box-giga-star">'
	rating_pos = page_source.find(rating_query)
	rating = page_source[rating_pos+len(rating_query)+1:rating_pos+len(rating_query)+4]
	print "Movie rating : " + rating
	
	#Movie info bar (Generes,Age Rating,Running Time
	info_bar_query = '<div class="infobar">'
	info_bar_end_query = '</div>'
	info_bar_pos = page_source.find(info_bar_query)
	info_bar_end_pos = page_source.find(info_bar_end_query,info_bar_pos)
	info_bar_html = page_source[info_bar_pos:info_bar_end_pos]
	
	age_rating_query = 'title="'
	age_rating_pos = info_bar_html.find(age_rating_query)
	age_rating = info_bar_html[age_rating_pos+len(age_rating_query):age_rating_pos+len(age_rating_query)+5]
	print "Age rating : " + age_rating
	
	running_time_query = "</time>"
	running_time_pos = info_bar_html.find(running_time_query)
	running_time = info_bar_html[running_time_pos-10:running_time_pos]
	running_time = running_time.split(">")[0]
	running_time = running_time.strip()
	running_time = running_time.lstrip()
	print "Running time : " + str(running_time)
	
	
	genres = []
	start_genre_pos = 0
	genre_query ='"/genre/'
	while start_genre_pos != -1 :
		start_genre_pos = info_bar_html.find(genre_query,start_genre_pos+1)
		if start_genre_pos == -1 :
			continue
		cur_genre = info_bar_html[start_genre_pos+len(genre_query):start_genre_pos+len(genre_query)+20]
		cur_genre = cur_genre.split("?")[0]
		genres.append(cur_genre)
	
	print "genres : " + str(genres)
	
	
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

		
def main(argv):
	if len(sys.argv) < 2 :
		sys.stderr.write('Usage: sys.argv[0] imdb/duckduckgo folder \n')
		sys.exit(1)
		
	if(sys.argv[1] == "duckduckgo"):
		import duckduckgo
		from scan_films_duckduckgo import movie_name_to_imdb_page
	elif(sys.argv[1] == "google"):
		from scan_films_google import movie_name_to_imdb_page
	else :
		exit (-1)
	
	
	movie_dict = {}	
	movie_search_path = sys.argv[2]

	if not os.path.exists(movie_search_path) :
		sys.stderr.write('Error sys.argv[1] doesn\'t exist ')

	for filename in os.listdir(movie_search_path): 
		print "Raw filename :: " + filename
		name_parts = filename.split('.')
		i = 0
		movie_year = 0
		for part in name_parts :
			if not is_number(part) :
				i+=1
			elif(float(part) < 1990):
				i+=1
			else :
				movie_year = part
				break
		if (movie_year == 0) :
			pass 
		else :
			movie_name = " ".join(name_parts[0:i])
			
			movie_imdb_query = "+".join(name_parts[0:i]) +"+" + str(movie_year) + "+IMDB"
			
			imdb_movie_url = movie_name_to_imdb_page(movie_imdb_query)

				
			parse_imdb_page (imdb_movie_url)
			
			if movie_dict.has_key(movie_name) :
				print "Duplicate movie name ::: %s " % movie_name
			
			movie_dict[movie_name]  = movie_year
			print "Movie name : "  + movie_name + ' , Production Year : ' + str(movie_year)
			time.sleep(10)


if __name__ == "__main__":
   main(sys.argv[1:])

