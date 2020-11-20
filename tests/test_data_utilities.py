from datetime import time as dt
from pytrains import data
import pytest

def test_getCRS():
    assert data.getCRS("Lympstone Village") == "LYM"
    assert data.getCRS("London Paddington") == "PAD"
    assert data.getCRS("Bristol Temple Meads") == "BRI"
    with pytest.raises(Exception):
        assert data.getCRS("PogChamp")

def test_getName():
    assert data.getName("LYM") == "Lympstone Village"
    assert data.getName("PAD") == "London Paddington"
    assert data.getName("BRI") == "Bristol Temple Meads"
    with pytest.raises(Exception):
        assert data.getName("POG")

def test_timeParse():
    assert data.timeParse("1234") == dt(12, 34)
    assert data.timeParse("0000") == dt(0, 0)
    with pytest.raises(Exception):
        assert data.timeParse("69420")

def test_search():
    assert data.search("Lympst") == ["Lympstone Commando", "Lympstone Village"]
    assert data.search("lYmPsT") == ["Lympstone Commando", "Lympstone Village"]
    assert data.search("a") == []
    assert data.search("Poggerithm") == []