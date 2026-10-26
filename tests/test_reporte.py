import os
import shutil
import sys
import tempfile
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solicitudes.catalogos import Estado  # noqa: E402
from solicitudes.modelos import DatosSolicitud  # noqa: E402
from solicitudes.reloj import RelojFijo  # noqa: E402
from solicitudes.repositorio import RepositorioJSON, RepositorioMemoria  # noqa: E402
from solicitudes.reporte import generar_reporte  # noqa: E402
from solicitudes.servicio import ServicioSolicitudes  # noqa: E402

HOY = date(2025, 6, 30)
FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "solicitudes_formato_inicial.json")


class TestReporte(unittest.TestCase):
    def setUp(self):
        self.servicio = ServicioSolicitudes(RepositorioMemoria(), RelojFijo(HOY))

    def registrar(self, tipo, fecha, **kw):
        return self.servicio.registrar(DatosSolicitud("Ana Perez", "12345", "a@mail.com", tipo, "desc", fecha=fecha, **kw))

    def test_reporte_vacio(self):
        texto = generar_reporte([], HOY)
        self.assertIn("Total: 0", texto)
        self.assertTrue(texto.endswith("--- Detalle ---"))

    def test_marca_vencidas_y_ordena_por_prioridad_luego_fecha(self):
        self.registrar("CERTIFICADO", "2025-06-29")   # BAJA, no vencida
        self.registrar("REINCORPORACION", "2025-06-01")  # ALTA, limite 06-16 -> vencida
        lineas = generar_reporte(self.servicio.listar(), HOY).splitlines()
        self.assertTrue(lineas[-2].startswith("#2 [ALTA]") and lineas[-2].endswith("VENCIDA"))
        self.assertTrue(lineas[-1].startswith("#1 [BAJA]") and not lineas[-1].endswith("VENCIDA"))

    def test_conteo_por_estado(self):
        self.registrar("CERTIFICADO", "2025-06-29")
        self.servicio.cambiar_estado(1, Estado.RECHAZADA)
        texto = generar_reporte(self.servicio.listar(), HOY)
        self.assertIn("PENDIENTE: 0", texto)
        self.assertIn("RECHAZADA: 1", texto)


class TestCompatibilidadDeDatos(unittest.TestCase):
    def test_lee_archivo_generado_por_la_version_inicial(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "s.json")
            shutil.copy(FIXTURE, ruta)
            servicio = ServicioSolicitudes(RepositorioJSON(ruta), RelojFijo(HOY))
            solicitudes = servicio.listar()
            self.assertEqual([1, 2], [s.id for s in solicitudes])
            self.assertEqual("Julia Vega", solicitudes[1].responsable.nombre)
            self.assertEqual(Estado.EN_PROCESO, solicitudes[1].estado)
            self.assertEqual(3, servicio.registrar(DatosSolicitud("Otro", "99999", "o@m.com", "OTRO", "x")).id)


if __name__ == "__main__":
    unittest.main()
