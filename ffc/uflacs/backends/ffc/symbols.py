# -*- coding: utf-8 -*-
# Copyright (C) 2011-2016 Martin Sandve Alnæs
#
# This file is part of UFLACS.
#
# UFLACS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UFLACS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with UFLACS. If not, see <http://www.gnu.org/licenses/>

"""FFC/UFC specific symbol naming."""

from ffc.log import error


# TODO: Get restriction postfix from somewhere central
def ufc_restriction_postfix(restriction):
    if restriction == "+":
        res = "_0"
    elif restriction == "-":
        res = "_1"
    else:
        res = ""
    return res


def format_mt_name(basename, mt):
    "Format variable name for modified terminal."
    access = str(basename)

    # Add averaged state to name
    if mt.averaged:
        avg = "_a{0}".format(mt.averaged)
        access += avg

    # Format restriction
    res = ufc_restriction_postfix(mt.restriction).replace("_", "_r")
    access += res

    # Format local derivatives
    assert not mt.global_derivatives
    if mt.local_derivatives:
        der = "_d{0}".format(''.join(map(str, mt.local_derivatives)))
        access += der

    # Add flattened component to name
    if mt.component:
        comp = "_c{0}".format(mt.flat_component)
        access += comp

    return access


class FFCBackendSymbols(object):
    """FFC specific symbol definitions. Provides non-ufl symbols."""
    def __init__(self, language, coefficient_numbering):
        self.L = language
        self.S = self.L.Symbol
        self.coefficient_numbering = coefficient_numbering

        # Used for padding variable names based on restriction
        self.restriction_postfix = { r: ufc_restriction_postfix(r)
                                     for r in ("+", "-", None) }

    def element_tensor(self):
        "Symbol for the element tensor itself."
        return self.S("A")

    def entity(self, entitytype, restriction):
        "Entity index for lookup in element tables."
        if entitytype == "cell":
            # Always 0 for cells (even with restriction)
            return self.L.LiteralInt(0)
        elif entitytype == "facet":
            return self.S("facet" + ufc_restriction_postfix(restriction))
        elif entitytype == "vertex":
            return self.S("vertex")
        else:
            error("Unknown entitytype {}".format(entitytype))

    def cell_orientation_argument(self, restriction):
        "Cell orientation argument in ufc. Not same as cell orientation in generated code."
        return self.S("cell_orientation" + ufc_restriction_postfix(restriction))

    def cell_orientation_internal(self, restriction):
        "Internal value for cell orientation in generated code."
        return self.S("co" + ufc_restriction_postfix(restriction))

    def num_quadrature_points(self, num_points):
        if num_points is None:
            return self.S("num_quadrature_points")
        else:
            return self.L.LiteralInt(num_points)

    def weights_array(self, num_points):
        if num_points is None:
            return self.S("quadrature_weights")
        else:
            return self.S("weights%d" % (num_points,))

    def points_array(self, num_points):
        # Note: Points array refers to points on the integration cell
        if num_points is None:
            return self.S("quadrature_points")
        else:
            return self.S("points%d" % (num_points,))

    def quadrature_loop_index(self, num_points):
        """Reusing a single index name for all quadrature loops,
        assumed not to be nested."""
        if num_points == 1:
            return self.L.LiteralInt(0)
        elif num_points is None:
            return self.S("iq")
        else:
            return self.S("iq%d" % (num_points,))

    def argument_loop_index(self, iarg):
        "Loop index for argument #iarg."
        return self.S("ia%d" % (iarg,))

    def coefficient_dof_sum_index(self):
        """Reusing a single index name for all coefficient dof*basis sums,
        assumed to always be the innermost loop."""
        return self.S("ic")

    def x_component(self, mt):
        "Physical coordinate component."
        return self.S(format_mt_name("x", mt))

    def J_component(self, mt):
        "Jacobian component."
        return self.S(format_mt_name("J", mt))

    def domain_dof_access(self, dof, component, gdim, num_scalar_dofs,
                          restriction, interleaved_components):
        # TODO: Add domain number?
        vc = self.S("coordinate_dofs" + ufc_restriction_postfix(restriction))
        if interleaved_components:
            return vc[gdim*dof + component]
        else:
            return vc[num_scalar_dofs*component + dof]

    def domain_dofs_access(self, gdim, num_scalar_dofs, restriction,
                           interleaved_components):
        # TODO: Add domain number?
        return [self.domain_dof_access(dof, component, gdim, num_scalar_dofs,
                                       restriction, interleaved_components)
                for component in range(gdim)
                for dof in range(num_scalar_dofs)]

    def coefficient_dof_access(self, coefficient, dof_number):
        # TODO: Add domain number?
        c = self.coefficient_numbering[coefficient]
        w = self.S("w")
        return w[c, dof_number]

    def coefficient_value(self, mt):  #, num_points):
        "Symbol for variable holding value or derivative component of coefficient."
        c = self.coefficient_numbering[mt.terminal]
        return self.S(format_mt_name("w%d" % (c,), mt))
        # TODO: Should we include num_points here? Not sure if there is a need.
        #return self.S(format_mt_name("w%d_%d" % (c, num_points), mt))