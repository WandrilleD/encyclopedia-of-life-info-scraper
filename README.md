
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
``