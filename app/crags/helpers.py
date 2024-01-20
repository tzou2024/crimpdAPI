from app import db
from app.crags.models import Crags

def get_crags():
    crags = Crags.query.all()

    return [{"id": i.id,
             "name": i.name,
             "descr": i.descr,
             "lat": i.lat,
             "long": i.long} for i in crags]

def get_crag(crag_id):
    crags = Crags.query.all()
    crag = list(filter(lambda x: x.id == crag_id, crags))[0]
    return {"id": crag.id,
             "name": crag.name,
             "descr": crag.descr,
             "lat": crag.lat,
             "long": crag.long}

