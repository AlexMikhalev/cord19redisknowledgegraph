#!/usr/bin/env python
# coding: utf-8


from pathlib import Path
import json
import sys
import joblib
import ahocorasick

import sqlalchemy
from sqlalchemy import create_engine
# engine = create_engine('sqlite:///:memory:', echo=True)

from config import config

params=config()

engine = create_engine(params['db_uri'])


from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)
Entities_dict=Base.classes.entities_dict
A = ahocorasick.Automaton()

def build_automata(engine, A):
    """
    building automata should be single threat
    Automata in general are not threat safe structure
    """
    print("Building automata")
    session = Session(engine)
    for each_row in session.query(Entities_dict).all():
        A.add_word(each_row.syn_term, (each_row.concept_id, each_row.syn_term))

build_automata(engine, A)
A.make_automaton()
A.get_stats()


joblib.dump(A,"./kaggle/working/automata_syns.pkl")

