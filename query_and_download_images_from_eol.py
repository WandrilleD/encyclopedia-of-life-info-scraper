# importing the requests library
import requests


from eol_basic_api_request import searchSpeciesIDs, getMediaList
from grab_image_from_url import getImageData, writeImageData



if __name__ == "__main__":
    import sys
    import os
    import argparse

    parser = argparse.ArgumentParser(
                description="""fetch image media from the EOL for a given list of species / taxon name.
The retrieved images will be documented in a csv file while the images themselves will take the species/taxon name (with spaces replaced by a '_')
                """)
    parser.add_argument('-q','--query', type=str, required=True,
             help='file containin one query per lines (ie, species/taxa names in latin')
    parser.add_argument('-o','--output', type=str, required=True,
             help='output folder name (the folder must already exist)')    
    parser.add_argument('-m','--max-image-per-record', type=int, default=10,
             help='maximum number of images per record (default : 10)')


    args = parser.parse_args()


    if not os.path.isdir( args.output ):
        print("ERROR: the designated output folder {} does not exists or is not a directory.".format(args.output))

    with open(args.query ,'r') as IN , open( os.path.join( args.output , 'medialist.csv' ) , 'w' ) as OUT:
        print("taxon" , 'eolID' , 'eolURL' , 
            'mediaLicense',
            'eolMediaURL',
            'description',
            'rightsHolder',
            'localFileName',sep=';' , file=OUT)

        for l in IN:
            species=l.strip()

            maxImage = args.max_image_per_record

            matchingIDs = searchSpeciesIDs(species)
            if len(matchingIDs) == 0:
                print("no IDs matching the query perfectly.")
                print("  query: {}".format(species))

            else: 
                print("found {} matching ID for query {}".format(len(matchingIDs),species))

            medias = {}
            N = 0

            for ID in matchingIDs:
                medias[ID] = getMediaList(ID , maxImage = maxImage )
                N += len(medias[ID])


            print("found {} medias for query {}".format(N,species))


            N = 0
            for ID in medias :
                for media in medias[ID]:

                    N += 1 
                    URL = media['eolMediaURL']
                    name = species.replace(' ','_') + '_' + str(N)
                    filename = os.path.join( args.output, name + '.' + URL.rpartition('.')[-1] )

                    img_data = getImageData(URL)
                    if img_data is None:
                        print("ERROR: unable to recover data from {}".format(URL))
                        continue


                    writeImageData(img_data, filename)

                    print(species , ID , 'https://eol.org/pages/{}'.format(ID) , 
                            media['license'],
                            media['eolMediaURL'],
                            '"{}"'.format(media['description'].replace('\n',' ')),
                            '"{}"'.format(media['rightsHolder']),
                                filename,sep=';' , file=OUT)


