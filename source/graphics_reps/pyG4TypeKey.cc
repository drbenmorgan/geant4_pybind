#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

#include <G4TypeKey.hh>

#include <limits>

#include "typecast.hh"

namespace py = pybind11;

void export_G4TypeKey(py::module &m)
{
   py::class_<G4TypeKey, std::unique_ptr<G4TypeKey>>(m, "G4TypeKey")
      .def(py::init<>())

      .def("IsValid", &G4TypeKey::IsValid)
      .def(py::self == py::self)
      .def(py::self != py::self)
      .def(py::self > py::self)
      .def(py::self < py::self)

      .def("__call__", &G4TypeKey::operator())
      .def("__str__",
           [](const G4TypeKey &self) {
              std::stringstream ss;
              ss << std::setprecision(std::numeric_limits<G4double>::digits10 + 1) << self;
              return ss.str();
           })

      .def("__repr__", [](const G4TypeKey &self) {
         std::stringstream ss;
         ss << std::setprecision(std::numeric_limits<G4double>::digits10 + 1) << self;
         return ss.str();
      });
   ;
}
