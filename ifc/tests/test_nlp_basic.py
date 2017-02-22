
from ifc import nlp

def test_clean_text():
    dirty = "*abc. hello' (TICKER.O) thing&"
    clean = "abc hello ticker.o thing"
    print clean
    print nlp.preprocess_text(dirty)
    assert clean == nlp.preprocess_text(dirty)
 
