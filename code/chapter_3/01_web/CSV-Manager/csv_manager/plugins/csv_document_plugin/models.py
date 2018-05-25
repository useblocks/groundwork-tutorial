#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, PickleType
from sqlalchemy.orm import relationship, backref


def get_models(db):

    Base = db.Base
    metadata = Base.metadata

    class CsvFile(Base):
        __tablename__ = 'csv_file'

        id = Column(Integer, primary_key=True)
        name = Column(String(2048), nullable=False)
        created = Column(String(255))
        current_version = Column(Integer)

        # version_id = Column(ForeignKey(u'version.id'))
        # version = relationship(u'Version')

        def __str__(self):
            return str(self.name)

    class Version(Base):
        __tablename__ = 'version'

        id = Column(Integer, primary_key=True)
        version = Column(Integer, nullable=False)
        created = Column(String(255))
        csv_file_id = Column(Integer, ForeignKey('csv_file.id'))
        csv_file = relationship("CsvFile", backref="version")
        new_row = relationship("NewRow", back_populates="version", cascade="all, delete-orphan")
        missing_row = relationship("MissingRow", back_populates="version", cascade="all, delete-orphan")

        def __str__(self):
            return str(self.version)

    class MissingRow(Base):
        __tablename__ = 'missing_row'

        id = Column(Integer, primary_key=True)
        row = Column(PickleType, nullable=False)
        version_id = Column(Integer, ForeignKey('version.id'))
        version = relationship("Version", back_populates="missing_row")

        def __str__(self):
            return str(self.row)

    class NewRow(Base):
        __tablename__ = 'new_row'

        id = Column(Integer, primary_key=True)
        row = Column(PickleType, nullable=False)
        version_id = Column(Integer, ForeignKey('version.id'))
        version = relationship("Version", back_populates="new_row")

        def __str__(self):
            return str(self.row)

    return CsvFile, Version, MissingRow, NewRow
