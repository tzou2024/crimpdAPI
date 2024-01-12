from datetime import datetime, timezone
from typing import Optional, Literal
import sqlalchemy as sa
import sqlalchemy.orm as so
#import db instance
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

#db.Model - a base class for all models
class User(db.Model):
    #so.Mapped[int] means required
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    sessions: so.WriteOnlyMapped['Session'] = so.relationship(
            back_populates='climber'
    )

    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    updated_at: so.Mapped[datetime] = so.mapped_column(
        index=True,default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Crag(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.String, index=True,
                                                unique=True)

    descr: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200), index=True)
    
    lat: so.Mapped[float] = so.mapped_column(sa.Float)

    long: so.Mapped[float] = so.mapped_column(sa.Float)

    climbs: so.WriteOnlyMapped['Climb'] = so.relationship(
        back_populates='crag')

    sessions: so.WriteOnlyMapped['Session'] = so.relationship(
        back_populates='crag'
    )

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

    descr: so.Mapped[Optional[str]] = so.mapped_column(sa.String, index=True)

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

    content: so.Mapped[str] = so.mapped_column(sa.String, index=True,
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

class Session(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String, index=True)

    climber_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                                    index=True)
    
    climber: so.Mapped[User] = so.relationship(back_populates='sessions')              

    crag_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Crag.id),
                                                    index=True)
    
    crag: so.Mapped[Crag] = so.relationship(back_populates='sessions')     

    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    updated_at: so.Mapped[datetime] = so.mapped_column(
        index=True,default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<Session by: {} @ {}>'.format(self.climber.username, self.crag.name)

class Rep(db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String, index=True)

    session_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Session.id),
                                                    index=True)
    
    session: so.Mapped[Session] = so.relationship(back_populates='reps') 

    climb_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Climb.id),
                                                    index=True)
    
    climb: so.Mapped[Climb] = so.relationship(back_populates='reps') 

    completed: so.Mapped[bool] = so.mapped_column(sa.Boolean, index=True)

    rpe: so.Mapped[int] = so.mapped_column(sa.Integer)

    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    updated_at: so.Mapped[datetime] = so.mapped_column(
        index=True,default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
            return '<Rep by: {} on {}>'.format(self.climber.username, self.climb.name)
    

