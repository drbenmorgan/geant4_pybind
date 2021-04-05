#include <pybind11/pybind11.h>

#include <G4UserRunAction.hh>
#include <G4Run.hh>

#include "holder.hh"
#include "typecast.hh"

namespace py = pybind11;

// Trampolin class
class TRAMPOLINE_NAME(G4UserRunAction) : public G4UserRunAction {

public:
   using G4UserRunAction::G4UserRunAction;

   void BeginOfRunAction(const G4Run *aRun) override
   {
      PYBIND11_OVERRIDE(void, G4UserRunAction, BeginOfRunAction, aRun);
   }

   void EndOfRunAction(const G4Run *aRun) override { PYBIND11_OVERRIDE(void, G4UserRunAction, EndOfRunAction, aRun); }

   G4Run *GenerateRun() override
   {
      py::gil_scoped_acquire gil;
      py::function           override = py::get_override(static_cast<const G4UserRunAction *>(this), "GenerateRun");
      if (override) {
         py::object o = override();
         o.inc_ref();

         G4Run *ptr;
         if (py::detail::cast_is_temporary_value_reference<G4Run *>::value) {
            static py::detail::override_caster_t<G4Run *> caster;
            ptr = py::detail::cast_ref<G4Run *>(std::move(o), caster);
         } else {
            ptr = py::detail::cast_safe<G4Run *>(std::move(o));
         }

         owntrans_ptr<G4Run>::remove(ptr);
         return ptr;
      }

      return G4UserRunAction::GenerateRun();
   }

   void SetMaster(G4bool val) override { PYBIND11_OVERRIDE(void, G4UserRunAction, SetMaster, val); }

   TRAMPOLINE_DESTRUCTOR(G4UserRunAction);
};

void export_G4UserRunAction(py::module &m)
{
   py::class_<G4UserRunAction, TRAMPOLINE_NAME(G4UserRunAction), owntrans_ptr<G4UserRunAction>>(m, "G4UserRunAction",
                                                                                                "run action class")

      .def(py::init<>())
      .def("BeginOfRunAction", &G4UserRunAction::BeginOfRunAction)
      .def("EndOfRunAction", &G4UserRunAction::EndOfRunAction)
      .def("GenerateRun", &G4UserRunAction::GenerateRun, py::return_value_policy::reference)
      .def("SetMaster", &G4UserRunAction::SetMaster, py::arg("val") = true)
      .def("IsMaster", &G4UserRunAction::IsMaster);
}
