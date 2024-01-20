import os
from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from typing import Optional, Literal
from datetime import datetime, timezone

class Crags(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.String, index=True,
                                                unique=True)

    descr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200), index=True)
    
    lat: so.Mapped[float] = so.mapped_column(sa.Float)

    long: so.Mapped[float] = so.mapped_column(sa.Float)

    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    updated_at: so.Mapped[datetime] = so.mapped_column(
        index=True,default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def __init__(self, name, descr, lat, long):
        self.name = name
        self.descr = descr
        self.lat = lat
        self.long = long
    
    def __repr__(self):
        return '<Crag {}>'.format(self.name) 
    
    
