# Project tasks/Roadmap:

## Phase 1

- [x]  rewrite intake:
    - [x]  JSON parse into Redis, creates:  article_id,paragraph_id
    - [x]  Redis paragraph split into sentences (BERT tokenised) into article_id, sentence_id, sentence
    - [x]  processed article keys are store cbloom in redis

- [x]  Detect sentence language
- [x]  Apply symspell
- [x]  tokenise sentence, storing model details in DB, input sentence, output tokenised sentence,
        - [ ]  Idea worth trying: add tokens to ids and feed into BART model deployed on RedisAI to create a summary of article.
        - [] add to tokeniser so output is ids and written into tensor to be fed into RedisAI BART model for summary of the article (parked)
  [x]  change tokeniser so output is strings (return as strings from tokeniser), add stopwords and punctuation removal into the same step 
- [x]  Remove stopwords
- [ ]  Expand abbreviations, store abbreviations dictionary in Redis (cache)

## Phase 2

- [x]  Match tokens to OWL ready search token to canonical term, store:
    - canonical_term, sentence_key
    - synonim, sentence_key
- [x]  Create Aho corasick from above - need for matching input as well
- [x]  Form pairs and create:
    - [x]  node, rank
        - [x]  set of article_keys mapped to node
    - [x]  edge, rank
        - []  set of article_key mapped to edge
- [ ] Idea worth trying: Use write behind pattern to automatically map nodes and edges into Redis Graph

## Phase 3
- [x] Create a node Article with attributes {id}, title, sentence_key:sentence
- [x]  Visualisation D3
- [x]  search terms matched into aho corasic
- [x]  nodes + edges
    - [ ]  on click to node show concept definition
    - [x]  on click to edge list articles
    - [ ]  On mouse over show definition of term
- [ ]  add autocomplete into search

Datamodel for Visualisation:
datamodel:
* node is a medical term from UMLS (medical dictionary). It will have a properties: canonical name, rank, description (and edges). It can will have synonyms  (internally)

* edge is pair of nodes (terms) met in article. Edge will have a list of articles (article_id) associated with it, sorted by - each edge have a rank, we can change thickness of it