# importing the requests library
import requests


def searchSpeciesIDs(species):
	"""
	Takes:
		- species (str) : species name (latin version)

	Returns:
		(list) : list of EOL ids matiching this species name exactly
	"""

  
	# api-endpoint
	URL = "https://eol.org/api/search/1.0.json"
	  

	# defining a params dict for the parameters to be sent to the API
	PARAMS = {'q':species,'exact':'true',}
	  
	# sending get request and saving the response as response object
	# url type: https://eol.org/api/search/1.0.json?q=Homo%2Bsapiens&page=1&key=
	r = requests.get(url = URL, params = PARAMS)
	  
	# extracting data in json format
	data = r.json()
	  


	matchingIDs = []
	## let's restrict ourselves to perfect matches only
	for r in data['results'] :
		if r['title'] == species:
			matchingIDs.append(r['id'])

	return matchingIDs

def getMediaList(ID , maxImage = 10 ):
	"""
	retrieves a list of image data linked to a given EOL ID (species, taxon, ...)
	NB : only recovers the image url, descri[tion, and license, not the image itself

	Takes:
		- ID (int) : EOL id 
		- maxImage = 10 (int) : maximum number of iamges to recover

	Returns:
		(list) of (dict) where keys are ['license','eolMediaURL','description','rightsHolder']
							 values are corresponding image license, image url on the EOL, image description, rights holder (all str)
	"""
	medias = []

	URL_pages = "https://eol.org/api/pages/1.0/{}.json".format(ID)
	PARAMS = {"details":"true" , "images_per_page":maxImage}


	# https://eol.org/api/pages/1.0/327955.json?details=true&images_per_page=10
	r_pages = requests.get(url = URL_pages, params = PARAMS)

	# extracting data in json format
	data_pages = r_pages.json()


	for o in data_pages['taxonConcept'].get('dataObjects',[]):
		if o['dataType']== 'http://purl.org/dc/dcmitype/StillImage':
			medias.append( {k:o.get(k,'') for k in ['license','eolMediaURL','description','rightsHolder'] } )
	return medias



if __name__ == "__main__":
	import sys
	import argparse

	parser = argparse.ArgumentParser(
				description="""fetch image media information from the EOL for a given species / taxon name""")
	parser.add_argument('-q','--query', type=str, required=True,
			 help='query species names (in latin)')
	parser.add_argument('-o','--output', type=str, required=True,
			 help='output file name')
	parser.add_argument('-a','--append', action="store_true",
			 help='append to the output file instead of overwriting it')
	
	parser.add_argument('-m','--max-image-per-record', type=int, default=10,
			 help='maximum number of images per record (default : 10)')


	args = parser.parse_args()

	species=args.query

	maxImage = args.max_image_per_record

	matchingIDs = searchSpeciesIDs(species)
	if len(matchingIDs) == 0:
		print("no IDs matching the query perfectly.")
		print("query: {}".format(species))
		print( 'results:' , *(['  ' + r['title'] for r in data['results']] ) , sep='\n' )

		exit(1)
	else: 
		print("found {} matching ID for query {}".format(len(matchingIDs),species))




	medias = {}
	N = 0

	for ID in matchingIDs:
		medias[ID] = getMediaList(ID , maxImage = maxImage )
		N += len(medias[ID])


	print("found {} medias for query {}".format(N,species))

	mode = 'w'
	if args.append :
		mode = 'a'


	with open( args.output , mode ) as OUT:

		for ID in medias :
			for media in medias[ID]:
				print(species , ID , 'https://eol.org/pages/{}'.format(ID) , 
						media['license'],
						media['eolMediaURL'],
						'"{}"'.format(media['description']),
						'"{}"'.format(media['rightsHolder']),sep=';' , file=OUT)


	print("results {} to {}".format( "wrote"*(mode=='w') + 'appended'*(mode=='a')  , args.output ))

