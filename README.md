
## Example usage

First, fetch a set of image infos and urls from the EOL

```
python eol_basic_api_request.py -q "Homo sapiens" -o homo_sapiens.txt
```

Isolate the URLs

```
awk 'BEGIN{FS=";"}{print "Homo_sapiens_" NR-1 ";" $5}' homo_sapiens.txt > homo_sapiens.img_to_download.txt
```

Download the images

```
python grab_image_from_url.py -i homo_sapiens.img_to_download.txt
```

You can also perform similar operation in a single step for multiple queries.

For instance, the following will download (at most) 5 pictures per species listed in the query file:

```
mkdir primates_images/ # creating output folder
python  query_and_download_images_from_eol.py -q primates_10species_list.txt -o primates_images -m 5 
```
