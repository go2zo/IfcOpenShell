###############################################################################
#                                                                             #
# This file is part of IfcOpenShell.                                          #
#                                                                             #
# IfcOpenShell is free software: you can redistribute it and/or modify        #
# it under the terms of the Lesser GNU General Public License as published by #
# the Free Software Foundation, either version 3.0 of the License, or         #
# (at your option) any later version.                                         #
#                                                                             #
# IfcOpenShell is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# Lesser GNU General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the Lesser GNU General Public License    #
# along with this program. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################

import numbers
import functools

from . import ifcopenshell_wrapper
from .entity_instance import entity_instance

class file(object):
	def __init__(self, f=None):
		self.wrapped_data = f or ifcopenshell_wrapper.file(True)
	def create_entity(self,type,*args,**kwargs):
		e = entity_instance(ifcopenshell_wrapper.entity_instance(type))
		attrs = list(enumerate(args)) + \
			[(e.wrapped_data.get_argument_index(name), arg) for name, arg in kwargs.items()]
		for idx, arg in attrs: e[idx] = arg
		self.wrapped_data.add(e.wrapped_data)
		e.wrapped_data.this.disown()
		return e
	def __getattr__(self, attr):
		if attr[0:6] == 'create': return functools.partial(self.create_entity,attr[6:])
		else: return getattr(self.wrapped_data, attr)
	def __getitem__(self, key):
		if isinstance(key, numbers.Integral):
			return entity_instance(self.wrapped_data.by_id(key))
		elif isinstance(key, str):
			return entity_instance(self.wrapped_data.by_guid(key))
	def by_id(self, id): return self[id]
	def by_guid(self, guid): return self[guid]
	def add(self, inst):
		inst.wrapped_data.this.disown()
		return entity_instance(self.wrapped_data.add(inst.wrapped_data))
	def by_type(self, type):
		return [entity_instance(e) for e in self.wrapped_data.by_type(type)]
	def traverse(self, inst):
		return [entity_instance(e) for e in self.wrapped_data.traverse(inst.wrapped_data)]
	def remove(self, inst):
		return self.wrapped_data.remove(inst.wrapped_data)
	def __iter__(self):
		return iter(self[id] for id in self.wrapped_data.entity_names())
