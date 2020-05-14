# Project tasks/Roadmap:

## Phase 1

- [ ]  rewrite intake:
    - [x]  JSON parse into Redis, creates:  article_id,paragraph_id
    - [ ]  Redis paragraph split into sentences (BERT tokenised) into article_id, paragraph_id, sentence_id, sentence
    - [x]  processed article keys are store cbloom in redis

- [ ]  Detect sentence language
- [ ]  Apply symspell
- [ ]  tokenise sentence, storing model details in DB, input sentence, output tokenised sentence, with reference to table with model configuration
- [ ]  Remove stopwords
- [ ]  Expand abbreviations, store abbreviations dictionary in Redis (cache)

## Phase 2

- [ ]  Match tokens to OWL ready search token to canonical term, store:
    - canonical_term, sentence_key
    - synonim, sentence_key
- [ ]  Create Aho corasick from above - need for matching input as well
- [ ]  Form pairs and create:
    - [ ]  node, rank
        - [ ]  set of article_keys mapped to node
    - [ ]  edge, rank
        - [ ]  set of article_key mapped to edge

## Phase 3

- [ ]  Visualisation D3
- [ ]  search terms matched into aho corasic
- [ ]  nodes + edges
    - [ ]  on click to node list articles
    - [ ]  on click to edge list articles
    - [ ]  On mouse over show definition of term
- [ ]  add autocomplete into search
