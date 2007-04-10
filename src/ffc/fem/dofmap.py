__author__ = "Anders Logg (logg@simula.no)"
__date__ = "2007-01-24 -- 2007-04-10"
__copyright__ = "Copyright (C) 2007 Anders Logg"
__license__  = "GNU GPL Version 2"

# Modified by Marie E. Rognes (meg@math.uio.no), 2007

# FFC common modules
from ffc.common.utils import *

# FIXME: Temporary fix, do this in mixed element
from mixedelement import *

class DofMap:

    """A DofMap represents a description of the degrees of a freedom
    of a finite element space, from which the mapping from local to
    global degrees of freedom can be computed."""

    def __init__(self, element):
        "Create dof map from given finite element"

        # Get entity dofs from element
        entity_dofs = element.entity_dofs()

        # Generate dof map data
        self.__signature        = "FFC dof map for " + element.signature()
        self.__local_dimension  = element.space_dimension()
        self.__entity_dofs      = entity_dofs
        self.__num_dofs_per_dim = self.__compute_num_dofs_per_dim(entity_dofs)
        self.__num_facet_dofs   = self.__compute_num_facet_dofs(entity_dofs)
        self.__dof_entities     = self.__compute_dof_entities(entity_dofs)
        self.__dof_coordinates  = self.__compute_dof_coordinates(element)
        self.__dof_components   = self.__compute_dof_components(element)

    def signature(self):
        "Return a string identifying the dof map"
        return self.__signature

    def local_dimension(self):
        "Return the dimension of the local finite element function space"
        return self.__local_dimension

    def entity_dofs(self):
        """Return a dictionary mapping the mesh entities of the
        reference cell to the degrees of freedom associated with the
        entity"""
        return self.__entity_dofs

    def num_facet_dofs(self):
        "Return the number of dofs on each cell facet"
        return self.__num_facet_dofs

    def num_dofs_per_dim(self, sub_dof_map=None):
        "Return the number of dofs associated with each topological dimension for sub dof map or total"
        if sub_dof_map == None:
            D = max(self.__entity_dofs[0])
            num_dofs_per_dim = (D + 1)*[0]
            for sub_num_dofs_per_dim in self.__num_dofs_per_dim:
                for dim in sub_num_dofs_per_dim:
                    num_dofs_per_dim[dim] += sub_num_dofs_per_dim[dim]
            return num_dofs_per_dim
        else:
            return self.__num_dofs_per_dim[sub_dof_map]

    def dof_entities(self):
        "Return a list of which entities are associated with each dof"
        return self.__dof_entities

    def dof_coordinates(self):
        """Return a list of which coordinates are associated with each
        dof. This only makes sense for Lagrange elements and other
        elements which have dofs defined by point evaluation."""
        return self.__dof_coordinates

    def dof_components(self):
        """Return a list of which components are associated with each
        dof. This only makes sense for Lagrange elements and other
        elements which have dofs defined by point evaluation."""
        return self.__dof_components

    def __compute_num_dofs_per_dim(self, entity_dofs):
        "Compute the number of dofs associated with each topological dimension"
        num_dofs_per_dim = []
        for sub_entity_dofs in entity_dofs:
            sub_num_dofs_per_dim = {}
            for dim in sub_entity_dofs:
                num_dofs = [len(sub_entity_dofs[dim][entity]) for entity in sub_entity_dofs[dim]]
                if dim in sub_num_dofs_per_dim:
                    sub_num_dofs_per_dim[dim] += pick_first(num_dofs)
                else:
                    sub_num_dofs_per_dim[dim] = pick_first(num_dofs)
            num_dofs_per_dim += [sub_num_dofs_per_dim]
        return num_dofs_per_dim

    def __compute_num_facet_dofs(self, entity_dofs):
        "Compute the number of dofs on each cell facet"

        #print ""
        #print entity_dofs

        #for sub_entity_dofs in entity_dofs:
        #    for dim in sub_entity_dofs:
                #print "dim = " + str(dim)
                #for entity in sub_entity_dofs[dim]:
                #    print str(entity) + ": " + str(sub_entity_dofs[dim])
        
        return 1

    def __compute_dof_entities(self, entity_dofs):
        "Compute the entities associated with each dof"
        dof_entities = {}
        offset = 0
        for sub_entity_dofs in entity_dofs:
            for dim in sub_entity_dofs:
                for entity in sub_entity_dofs[dim]:
                    for dof in sub_entity_dofs[dim][entity]:
                        dof_entities[offset + dof] = (dim, entity)
            offset = max(dof_entities) + 1
        return dof_entities

    def __compute_dof_coordinates(self, element):
        "Compute the coordinates associated with each dof"

        # We can handle scalar Lagrange elements
        if element.family() == "Lagrange":
            points = element.sub_element(0).dual_basis().pts
            return [tuple([0.5*(x + 1.0) for x in point]) for point in points]

        # We can handle tensor products of scalar Lagrange elements
        if self.__is_vector_lagrange(element):
            points = element.sub_element(0).dual_basis().pts
            repeated_points = []
            for i in range(element.value_dimension(0)):
                repeated_points += points
            return [tuple([0.5*(x + 1.0) for x in point]) for point in repeated_points]

        # Can't handle element
        return None

    def __compute_dof_components(self, element):
        "Compute the components associated with each dof"

        # We can handle scalar Lagrange elements
        if element.family() == "Lagrange":
            return [0 for i in range(element.space_dimension())]

        # We can handle tensor products of scalar Lagrange elements        
        if self.__is_vector_lagrange(element):
            components = []
            for i in range(element.value_dimension(0)):
                components += element.sub_element(0).space_dimension()*[i]
            return components

        # Can't handle element
        return None

    def __is_vector_lagrange(self, element):
        "Check if element is vector Lagrange element"
        if not element.family() == "Mixed":
            return False
        families = [element.sub_element(i).family() for i in range(element.num_sub_elements())]
        dimensions = [element.sub_element(i).space_dimension() for i in range(element.num_sub_elements())]
        return families[:-1] == families[1:] and dimensions[:-1] == dimensions[1:]
        
    def __repr__(self):
        "Pretty print"
        return self.signature()
