#include <pybind11/pybind11.h>

#include <G4EmExtraPhysics.hh>

#include "holder.hh"
#include "typecast.hh"

namespace py = pybind11;

void export_G4GLNPhysics(py::module &m)
{
   py::class_<G4EmExtraPhysics, G4VPhysicsConstructor, owntrans_ptr<G4EmExtraPhysics>>(m, "G4EmExtraPhysics")
      .def(py::init<>())
      .def("ConstructParticle", &G4EmExtraPhysics::ConstructParticle)
      .def("ConstructProcess", &G4EmExtraPhysics::ConstructProcess);
}
