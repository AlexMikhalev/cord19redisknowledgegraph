Scripts to import UMLS Metathesaurus into Redis cluster

need to run 
```
sudo mysql  umls_meta --skip-column-names --raw  < cui_term.sql | redis-cli -p 30004 --pipe
```
on all nodes. 
For demo load to single node:
```
sudo mysql  umls_meta --skip-column-names --raw  < cui_term.sql | redis-cli -h 10.144.17.211 --pipe 
```

To Extract All search terms for building Aho-Corasick automata:
```
#dump all words to CUI into file for Aho Corasick Automata
sudo mysql --skip-column-names --raw umls_meta -e "select WD, CUI from MRXW_ENG" >words_cui.tsv
```
To install UMLS Metathesaurus follow: 
https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/index.html 
