from datetime import datetime, timezone
from typing import Optional, Literal
import sqlalchemy as sa
import sqlalchemy.orm as so
#import db instance
from app import db

#db.Model - a base class for all models
class User(db.Model):
    #so.Mapped[int] means required
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    updated_at: so.Mapped[datetime] = so.mapped_column(
        index=True,default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return '<User {}>'.format(self.username) 

class Crag(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)

    descr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200), index=True)
    
    lat: so.Mapped[float] = so.mapped_column(sa.Float)

    long: so.Mapped[float] = so.mapped_column(sa.Float)

    climbs: so.WriteOnlyMapped['Climb'] = so.relationship(
        back_populates='crag')

    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    updated_at: so.Mapped[datetime] = so.mapped_column(
        index=True,default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<Crag {}>'.format(self.name) 

    
Angle = Literal["slab", "vertical", "overhang"]
Type = Literal["boulder", "toprope", "lead", "trad"]


class Climb(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, default="unnamed")

    descr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200), index=True)

    crag_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Crag.id),
                                               index=True)

    crag: so.Mapped[Crag] = so.relationship(back_populates="climbs")

    angle: so.Mapped[Angle] = so.mapped_column(sa.Enum("slab", "vertical", "overhang", name="angle_enum"))

    type: so.Mapped[Type] = so.mapped_column(sa.Enum("boulder", "toprope", "lead", "trad", name="type_enum"))

    grade: so.Mapped[str] = so.mapped_column(sa.String(20))

    img_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(80))

    tags: so.WriteOnlyMapped['Tag'] = so.relationship(
        back_populates='climb')


    set_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    updated_at: so.Mapped[datetime] = so.mapped_column(
        index=True,default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return '<{}: {}, {}>'.format(self.type, self.name, self.grade) 

class Tag(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    content: so.Mapped[str] = so.mapped_column(sa.String(200), index=True,
                                                    unique=True)
    
    climb_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Climb.id),
                                                index=True)
    
    climb: so.Mapped[Climb] = so.relationship(back_populates='tags')

    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    updated_at: so.Mapped[datetime] = so.mapped_column(
        index=True,default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<Tag: {}>'.format(self.descr)

