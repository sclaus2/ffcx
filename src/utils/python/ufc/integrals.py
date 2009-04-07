# Code generation format strings for UFC (Unified Form-assembly Code) v. 1.1.2.
# This code is released into the public domain.
#
# The FEniCS Project (http://www.fenics.org/) 2006-2008.

cell_integral_combined = """\
/// This class defines the interface for the tabulation of the cell
/// tensor corresponding to the local contribution to a form from
/// the integral over a cell.

class %(classname)s: public ufc::cell_integral
{%(members)s
public:

  /// Constructor
  %(classname)s() : ufc::cell_integral()
  {
%(constructor)s
  }

  /// Destructor
  virtual ~%(classname)s()
  {
%(destructor)s
  }

  /// Tabulate the tensor for the contribution from a local cell
  virtual void tabulate_tensor(double* A,
                               const double * const * w,
                               const ufc::cell& c) const
  {
%(tabulate_tensor)s
  }

};
"""

cell_integral_header = """\
/// This class defines the interface for the tabulation of the cell
/// tensor corresponding to the local contribution to a form from
/// the integral over a cell.

class %(classname)s: public ufc::cell_integral
{%(members)s
public:

  /// Constructor
  %(classname)s();

  /// Destructor
  virtual ~%(classname)s();

  /// Tabulate the tensor for the contribution from a local cell
  virtual void tabulate_tensor(double* A,
                               const double * const * w,
                               const ufc::cell& c) const;

};
"""

cell_integral_implementation = """\
/// Constructor
%(classname)s::%(classname)s() : ufc::cell_integral()
{
%(constructor)s
}

/// Destructor
%(classname)s::~%(classname)s()
{
%(destructor)s
}

/// Tabulate the tensor for the contribution from a local cell
void %(classname)s::tabulate_tensor(double* A,
                                    const double * const * w,
                                    const ufc::cell& c) const
{
%(tabulate_tensor)s
}
"""

exterior_facet_integral_combined = """\
/// This class defines the interface for the tabulation of the
/// exterior facet tensor corresponding to the local contribution to
/// a form from the integral over an exterior facet.

class %(classname)s: public ufc::exterior_facet_integral
{%(members)s
public:

  /// Constructor
  %(classname)s() : ufc::exterior_facet_integral()
  {
%(constructor)s
  }

  /// Destructor
  virtual ~%(classname)s()
  {
%(destructor)s
  }

  /// Tabulate the tensor for the contribution from a local exterior facet
  virtual void tabulate_tensor(double* A,
                               const double * const * w,
                               const ufc::cell& c,
                               unsigned int facet) const
  {
%(tabulate_tensor)s
  }

};
"""

exterior_facet_integral_header = """\
/// This class defines the interface for the tabulation of the
/// exterior facet tensor corresponding to the local contribution to
/// a form from the integral over an exterior facet.

class %(classname)s: public ufc::exterior_facet_integral
{%(members)s
public:

  /// Constructor
  %(classname)s();

  /// Destructor
  virtual ~%(classname)s();

  /// Tabulate the tensor for the contribution from a local exterior facet
  virtual void tabulate_tensor(double* A,
                               const double * const * w,
                               const ufc::cell& c,
                               unsigned int facet) const;

};
"""

exterior_facet_integral_implementation = """\
/// Constructor
%(classname)s::%(classname)s() : ufc::exterior_facet_integral()
{
%(constructor)s
}

/// Destructor
%(classname)s::~%(classname)s()
{
%(destructor)s
}

/// Tabulate the tensor for the contribution from a local exterior facet
void %(classname)s::tabulate_tensor(double* A,
                                    const double * const * w,
                                    const ufc::cell& c,
                                    unsigned int facet) const
{
%(tabulate_tensor)s
}
"""

interior_facet_integral_combined = """\
/// This class defines the interface for the tabulation of the
/// interior facet tensor corresponding to the local contribution to
/// a form from the integral over an interior facet.

class %(classname)s: public ufc::interior_facet_integral
{%(members)s
public:

  /// Constructor
  %(classname)s() : ufc::interior_facet_integral()
  {
%(constructor)s
  }

  /// Destructor
  virtual ~%(classname)s()
  {
%(destructor)s
  }

  /// Tabulate the tensor for the contribution from a local interior facet
  virtual void tabulate_tensor(double* A,
                               const double * const * w,
                               const ufc::cell& c0,
                               const ufc::cell& c1,
                               unsigned int facet0,
                               unsigned int facet1) const
  {
%(tabulate_tensor)s
  }

};
"""

interior_facet_integral_header = """\
/// This class defines the interface for the tabulation of the
/// interior facet tensor corresponding to the local contribution to
/// a form from the integral over an interior facet.

class %(classname)s: public ufc::interior_facet_integral
{%(members)s
public:

  /// Constructor
  %(classname)s();

  /// Destructor
  virtual ~%(classname)s();

  /// Tabulate the tensor for the contribution from a local interior facet
  virtual void tabulate_tensor(double* A,
                               const double * const * w,
                               const ufc::cell& c0,
                               const ufc::cell& c1,
                               unsigned int facet0,
                               unsigned int facet1) const;

};
"""

interior_facet_integral_implementation = """\
/// Constructor
%(classname)s::%(classname)s() : ufc::interior_facet_integral()
{
%(constructor)s
}

/// Destructor
%(classname)s::~%(classname)s()
{
%(destructor)s
}

/// Tabulate the tensor for the contribution from a local interior facet
void %(classname)s::tabulate_tensor(double* A,
                                    const double * const * w,
                                    const ufc::cell& c0,
                                    const ufc::cell& c1,
                                    unsigned int facet0,
                                    unsigned int facet1) const
{
%(tabulate_tensor)s
}
"""
