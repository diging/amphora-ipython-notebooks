import pandas as pd
from math import isnan
from pathlib import Path

class Sheet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.parse_excel_file()

    def parse_excel_file(self):
        self.articles = []
        df = pd.read_excel(self.file_name)
        
        for i, row in df.iterrows():
            title = row["Title"]
            pmid = row["PMID"]
            pmcid = row["PMCID"]
            year = row["Publication_Years"]
            authors = []
            for i in range(1, 11):
                first_name = row[f"AuthorFirstName{i}"]
                last_name = row[f"AuthorLastName{i}"]
                affiliation = row[f"AuthorAff{i}"]
                if isinstance(last_name, str) and isinstance(first_name, str):
                    authors.append([last_name, first_name, affiliation])
                else:
                    break

            self.articles.append({
                "title": title,
                "pmid": pmid,
                "pmcid": pmcid,
                "year": year,
                "authors": authors
            })
            if i == 10: break

class Journal:
    def __init__(self):
        self.metadata = "/Users/nowke/Desktop/diging/metadata"
        self.folder = "/Users/nowke/Desktop/diging/files/"
        self.destination = "/Users/nowke/Desktop/diging/not_found"
        self.files = []
        self.meta_files = []

    def search(self):
        self.scan_folder()
        self.get_metadata_files()
        self.perform_match()

    def scan_folder(self):
        folder_path = Path(self.folder)
        text_files = list(folder_path.glob("**/*.txt"))
        self.files = text_files

    def get_metadata_files(self):
        folder_path = Path(self.metadata)
        meta_files = list(folder_path.glob("**/*.xlsx"))
        self.meta_files = meta_files

    def perform_match(self):
        sheet = Sheet(self.meta_files[0])
        text_file = self.files[657]
        article_meta = sheet.articles[0]

        # Match contents of `text_file` and `article_meta`
        with open(text_file) as f:
            size_to_read = self.get_file_size_to_read(text_file)
            data = f.read(size_to_read)
            print(article_meta["title"])
            score = 0
            if article_meta["title"] and article_meta["title"] in data:
                score += 50
            if article_meta["pmid"] and str(article_meta["pmid"]) in data:
                score += 10
            if article_meta["pmcid"] and str(article_meta["pmcid"]) in data:
                score += 10
            author_matches = 0
            for author in article_meta["authors"]:
                name = f"{author[1]} {author[0]}"
                if name in data:
                    author_matches += 1

            author_match_percentage = author_matches / len(article_meta["authors"])
            if author_match_percentage == 1:
                score += 30
            print(score)

    def get_file_size_to_read(self, text_file):
        size = text_file.stat().st_size
        if size <= 3000:
            return size
        elif size > 3000 and size <= 6000:
            return int(size * 2 / 3)
        else:
            return int(size / 3)

if __name__ == "__main__":
    journal = Journal()
    journal.search()
    