# This module contains the utilities to take a page and extract information from it.

from .types import LabeledCandidate, LinkType

# Very simple classification functions
def is_price(cand: Candidate):
    return "euro" in cand.text

def is_size(cand: Candidate):
    return "m2" in cand.text

def is_rooms(cand: Candidate):
    return "Zi." in cand.text

# For each source we create a new record.

# In this case we have records of this kind: We need to build it
# from various relationships
class Record:
    record_id: str
    title: str
    location: str
    price: str
    rooms: str



def extract_data(candidates: List[Candidate], links: LinkType):
    """Extract data"""
    # Step 1: obtain all the links
    # Step 2: construct graphs
    # Step 3: classify 

    for link in links:
        # We have to
        id = get_id(link)
        rel_type = get_rel_type(link)
        subject_data = get_subject_data(link)
        predicate_data = get_predicate_data(link) 