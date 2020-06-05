.. Yggdrasil: Covid19 - Redis Knowledge Graph documentation master file, created by

Welcome to Yggdrasil: Covid19 - Redis Knowledge Graph's documentation!
======================================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   
   submissionredishack
   Roadmap

First attempt to create documentation, so far best content inside submissionhack

Architecture Diagram
--------------------

.. mermaid::

   graph LR;
      A[Intake]-->B(Language Detector);
      B-->C(Spacy:Split paragraphs);
      C-->D(Spellchecker: SymSpell);
      D-->E(BERT: tokenizer);
      E-->F(Matcher: Match tokens to concepts);
      F-->G(RedisGraph);
      G-->H(API Server);
      H-->I(Visualisation)
      J(Build Automata)-->F;
      K(Read UMLS table)-->J;
   
      

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
