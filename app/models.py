from typing import Optional
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

    def __repr__(self):
        return '<User {}>'.format(self.username) 