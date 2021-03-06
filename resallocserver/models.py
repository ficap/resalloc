# DB object abstraction for resalloc server.
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import time
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func, LargeBinary
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from resalloc.helpers import RState, TState

Base = declarative_base()

class TagMixin(object):
    @property
    def tag_set(self):
        return set(map(str, self.tags))


class Pool(Base):
    __tablename__ = 'pools'
    name = Column(String, primary_key=True)
    last_start = Column(Float, default=0)


class Ticket(Base, TagMixin):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.id'))
    resource = relationship('Resource',
                            backref=backref('ticket', uselist=False))
    state = Column(String, default=TState.OPEN)
    tid = Column(String)


class Resource(Base, TagMixin):
    __tablename__ = 'resources'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    user = Column(String, nullable=True)
    # The output from 'allocation' script.
    data = Column(LargeBinary)
    pool = Column(String, nullable=False)
    state = Column(String, nullable=False, default=RState.STARTING)
    check_last_time = Column(Float, default=time.time())
    check_failed_count = Column(Integer, default=0)


class ResourceTag(Base):
    __tablename__ = 'resource_tags'
    id = Column(String, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    resource = relationship('Resource', backref=backref('tags'))

    def __str__(self):
        return str(self.id)


class TicketTag(Base):
    __tablename__ = 'ticket_tags'
    id = Column(String, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), primary_key=True)
    ticket = relationship('Ticket', backref=backref('tags'))

    def __str__(self):
        return str(self.id)
