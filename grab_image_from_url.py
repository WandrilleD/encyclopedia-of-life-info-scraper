import requests


def getImageData(image_url):

    response = requests.get(image_url)

    if not response.ok:
        print(response)
        return None

    img_data = response.content
    return img_data


def writeImageData(img_data, file):
    with open( file , 'wb') as OUT:
        OUT.write(img_data)






if __name__ == "__main__":
    import sys
    import os
    import argparse

    parser = argparse.ArgumentParser(
                description="""fetch image from a set of urls given in an input file.
                                recovered images will be wrote in a file with the name given in the input file.""")
    parser.add_argument('-i','--input', type=str, required=True,
             help='input file.\n  Expected format: name;image_url , 1 image per line')
    parser.add_argument('-o','--output', type=str, default='.',
             help='output folder name (must already exists). default : .')


    args = parser.parse_args()

    with open(args.input) as IN: 
        for l in IN:
            name,image_url = l.strip().split(';')

            img_data = getImageData(image_url)
            if img_data is None:
                print("ERROR: unable to recover data from {}".format(image_url))

            fileName = os.path.join( args.output, name + '.' + image_url.rpartition('.')[-1] )
            print("writing to {}".format(fileName))
            writeImageData(img_data, fileName)

