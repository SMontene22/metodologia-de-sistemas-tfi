import os
import sys
import tempfile
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solicitudes.catalogos import Area, Estado, Prioridad, TipoSolicitud  # noqa: E402
from solicitudes.errores import (AsignacionInvalida, ErrorDePersistencia, SolicitudNoEncontrada,  # noqa: E402
                                 TransicionInvalida, ValidacionError)
from solicitudes.modelos import DatosSolicitud, FiltroSolicitudes, Responsable  # noqa: E402
from solicitudes.reloj import RelojFijo  # noqa: E402
from solicitudes.repositorio import RepositorioJSON, RepositorioMemoria  # noqa: E402
from solicitudes.servicio import ServicioSolicitudes  # noqa: E402

HOY = date(2025, 6, 30)


def datos(**kw):
    base = dict(nombre="Ana Perez", legajo="12345", mail="ana@mail.com",
                tipo="CERTIFICADO", descripcion="Certificado de alumno regular")
    base.update(kw)
    return DatosSolicitud(**base)


class TestRegistrar(unittest.TestCase):
    def setUp(self):
        self.servicio = ServicioSolicitudes(RepositorioMemoria(), RelojFijo(HOY))

    def test_registra_con_valores_por_defecto(self):
        s = self.servicio.registrar(datos())
        self.assertEqual(1, s.id)
        self.assertEqual(Estado.PENDIENTE, s.estado)
        self.assertEqual(Prioridad.BAJA, s.prioridad)  # prioridad por defecto de CERTIFICADO
        self.assertEqual(HOY, s.fecha)                 # fecha tomada del reloj inyectado

    def test_prioridad_explicita_pisa_la_de_defecto(self):
        self.assertEqual(Prioridad.ALTA, self.servicio.registrar(datos(prioridad="ALTA")).prioridad)

    def test_ids_correlativos(self):
        self.assertEqual([1, 2], [self.servicio.registrar(datos()).id for _ in range(2)])

    def test_cada_dato_invalido_informa_su_campo(self):
        casos = {
            "nombre": datos(nombre=""), "legajo": datos(legajo="12"), "mail": datos(mail="sinarroba"),
            "tipo": datos(tipo="VIAJE"), "descripcion": datos(descripcion="   "),
            "prioridad": datos(prioridad="URGENTE"), "fecha": datos(fecha="30/06/2025"),
        }
        for campo, d in casos.items():
            with self.subTest(campo=campo):
                with self.assertRaises(ValidacionError) as ctx:
                    self.servicio.registrar(d)
                self.assertEqual(campo, ctx.exception.campo)

    def test_un_registro_invalido_no_se_persiste(self):
        with self.assertRaises(ValidacionError):
            self.servicio.registrar(datos(nombre=""))
        self.assertEqual([], self.servicio.listar())


class TestOperaciones(unittest.TestCase):
    def setUp(self):
        self.servicio = ServicioSolicitudes(RepositorioMemoria(), RelojFijo(HOY))
        self.id = self.servicio.registrar(datos()).id

    def test_asignar_y_cambiar_estado(self):
        self.servicio.asignar_responsable(self.id, Responsable("Carlos", Area.ALUMNADO))
        self.assertEqual(Estado.EN_PROCESO, self.servicio.cambiar_estado(self.id, Estado.EN_PROCESO).estado)

    def test_errores_especificos(self):
        with self.assertRaises(SolicitudNoEncontrada):
            self.servicio.cambiar_estado(99, Estado.EN_PROCESO)
        with self.assertRaises(AsignacionInvalida):
            self.servicio.asignar_responsable(self.id, Responsable("X", Area.SECRETARIA))
        with self.assertRaises(TransicionInvalida):
            self.servicio.cambiar_estado(self.id, Estado.EN_PROCESO)  # sin responsable

    def test_reporte_usa_el_reloj_inyectado(self):
        self.assertIn("Total: 1", self.servicio.reporte())

    def test_buscar(self):
        self.servicio.registrar(datos(tipo="BAJA", descripcion="Baja de la carrera"))
        self.assertEqual([2], [s.id for s in self.servicio.buscar(FiltroSolicitudes(tipo=TipoSolicitud.BAJA))])
        self.assertEqual([1], [s.id for s in self.servicio.buscar(FiltroSolicitudes(texto="REGULAR"))])
        self.assertEqual(2, len(self.servicio.buscar()))


class TestRepositorioJSON(unittest.TestCase):
    def test_persiste_y_recarga(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "s.json")
            servicio = ServicioSolicitudes(RepositorioJSON(ruta), RelojFijo(HOY))
            s = servicio.registrar(datos())
            servicio.asignar_responsable(s.id, Responsable("Carlos", Area.ALUMNADO))
            recargado = ServicioSolicitudes(RepositorioJSON(ruta), RelojFijo(HOY)).listar()
            self.assertEqual(1, len(recargado))
            self.assertEqual(Responsable("Carlos", Area.ALUMNADO), recargado[0].responsable)

    def test_archivo_corrupto_informa_error(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "s.json")
            with open(ruta, "w") as f:
                f.write("{no es json")
            with self.assertRaises(ErrorDePersistencia):
                RepositorioJSON(ruta)


if __name__ == "__main__":
    unittest.main()
