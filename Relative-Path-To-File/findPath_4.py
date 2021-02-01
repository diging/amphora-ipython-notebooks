import re
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

            if title:
                self.articles.append({
                    "title": title,
                    "pmid": pmid,
                    "pmcid": pmcid,
                    "year": year,
                    "authors": authors
                })

class Journal:
    def __init__(self):
        self.metadata = "/Users/nowke/Documents/diging/metadata"
        self.folder = "/Users/nowke/Documents/diging/files/"
        self.destination = "/Users/nowke/Documents/diging/not_found"
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
        print(f"Found {len(self.files)} inside '{folder_path}'")

    def get_metadata_files(self):
        folder_path = Path(self.metadata)
        meta_files = list(folder_path.glob("**/*.xlsx"))
        self.meta_files = meta_files

    def perform_match(self):
        print(f"Scanning metadata - '{self.meta_files[0]}'")
        
        sheet = Sheet(self.meta_files[0])
        print(f"Found {len(sheet.articles)} inside the metadata sheet\n")

        for i, text_file in enumerate(self.files):
            print(f"Scanning File ({i + 1}/{len(self.files)}) {text_file}")
            for article_meta in sheet.articles:
                score = self.get_score_for_text(sheet, text_file, article_meta)
                # if score >= 30:
                #     print("===============")
                #     print(f"Matching {text_file} with {article_meta['title']}")
                #     print(score)
                #     print("===============")
                #     print()
                if score >= 80:
                    print("Matched all")
                    break

    def get_score_for_text(self, sheet, text_file, article_meta):
        # Match contents of `text_file` and `article_meta`
        with open(text_file, encoding='utf8') as f:
            size_to_read = self.get_file_size_to_read(text_file)
            data = f.read(size_to_read)
            data_cleaned = data.replace("’", "'").replace("-", "‐")
            pmid = self._parse_article_field(article_meta["pmid"])
            pmcid = self._parse_article_field(article_meta["pmcid"])
            title = article_meta["title"].replace("’", "'").replace("-", "‐")

            score = 0
            if title and title.replace(" ", "").lower() in re.sub(r"[\s]", "", data_cleaned.replace(" ", "").lower()):
                score += 50
            if pmid and pmid in data:
                score += 10
            if pmcid and pmcid in data:
                score += 10

            if len(article_meta["authors"]) > 0:
                # Match all authors
                author_matches = 0
                for author in article_meta["authors"]:
                    last_name = author[1].strip().replace("’", "'").replace("-", "‐")
                    first_name = author[0].strip().replace("’", "'").replace("-", "‐")
                    name = f"{last_name} {first_name}"
                    if name in data_cleaned:
                        author_matches += 1

                author_match_percentage = author_matches / len(article_meta["authors"])
                score += 30 * author_match_percentage

            # if score >= 30:
            #     print("Authors", article_meta["authors"])
            #     print(f"PMID {pmid}, PMCID {pmcid}")
            
            return score


    def get_file_size_to_read(self, text_file):
        size = text_file.stat().st_size
        if size <= 3000:
            return size
        elif size > 3000 and size <= 6000:
            return int(size * 2 / 3)
        else:
            return int(size / 3)

    def _parse_article_field(self, field):
        if type(field) is float and not isnan(field):
            return str(int(field))
        if type(field) is str:
            return field
        if type(field) is int:
            return str(field)

if __name__ == "__main__":
    journal = Journal()
    journal.search()
    