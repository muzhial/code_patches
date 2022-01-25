import requests


url = 'http://www.tutorialspoint.com/python3/python_tutorial.pdf'
r = requests.get(url)
filename = url.split('/')[-1]
with open(filename,'wb') as output_file:
    output_file.write(r.content)


# large file
r = requests.get(url, stream = True)
with open("PythonBook.pdf", "wb") as Pypdf:
    for chunk in r.iter_content(chunk_size = 1024):
        if chunk:
            Pypdf.write(chunk)
