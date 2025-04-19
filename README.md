# SC4021

## Solr
### Running Solr
```
solr-8.11.4/bin/solr start 
solr-8.11.4/bin/solr stop	
```
To access Solr UI, head to http://localhost:8983/solr/

### Installation
```
wget https://downloads.apache.org/lucene/solr/8.11.4/solr-8.11.4.tgz
tar -xvzf solr-8.11.4.tgz
```

### Creating a core & uploading csv
```
bin/solr create -c <core_name>
bin/post -c <core_name> <path_to_csv_file>
```

### Files modified
- managed-schema
    - added in tokenizer and filters 

- solrconfig.xml
    - added in spellcheck

- stopwords.txt
    - added in stopwords

- synonyms.txt
    - added in synonyms for query 