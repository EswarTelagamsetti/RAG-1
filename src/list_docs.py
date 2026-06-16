import os

files = os.listdir("data/pdfs")

for file in files:
    if file.endswith(".pdf"):
        print(file)