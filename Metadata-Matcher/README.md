# Metadata matcher script

This script is used for matching journal articles and metadata. Requires Python 3.6+ and [`pandas`](https://pypi.org/project/pandas/)

## Configuration

Set the following configurations in `config.py`

* `METADATA_FILE` - Path to journal metadata file: supports `.xlsx` and `.csv` files
* `TEXT_FILES_FOLDER` - Folder containing all the raw journal article text files. Supports nested folder structure
* `NOT_FOUND_FOLDER` - Path to an empty folder. All the unmatched raw text files will be copied here
* `FOUND_METADATA` - Path to the target metadata file: supports `.xlsx`. This is a copy of `METADATA_FILE`, prepended with 3 columns: **raw text** of the matched file, **path** of the matched file, and **matching score**.
* Set the `FLAG_USE_ABSTRACT = True` for including the ***abstract*** column in the matching process.

### Matching authors

The script supports two types of parsing authors from metadata file. 

1. Authors are listed in a single column. 
    * Example: `Yu, Zhongtang; Morrison, Mark`.
    * Set `META_AUTHOR_SINGLE_FIELD = True` for this case
    * Use `META_AUTHOR_SINGLE_SEPARATOR` to set the separator character
2. Authors are listed in multiple column.
    * Example: `AuthorFirstName1`, `AuthorLastName1`, `AuthorFirstName2`, `AuthorLastName2`, ... etc.
    * Set `META_AUTHOR_SINGLE_FIELD = False` for this case

## Run Script

After setting all configurations in `config.py`, run the following command:

```
python run_script.py
```

## Scoring

The current scoring schema is as follows:

### 1. Without Abstract (FLAG_USE_ABSTRACT = False)

```
title      - 30
authors    - 20
pmid       -  5
pmcid      -  5

Cutoff     - 50
```

### 2. With Abstract (FLAG_USE_ABSTRACT = True)

```
abstract   - 40
title      - 30
authors    - 20
pmid       -  5
pmcid      -  5

Cutoff     - 70
```