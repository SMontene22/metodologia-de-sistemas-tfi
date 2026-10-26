import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solicitudes.catalogos import Area, Estado, Prioridad, TipoSolicitud  # noqa: E402
from solicitudes.errores import AsignacionInvalida, TransicionInvalida, ValidacionError  # noqa: E402
from solicitudes.modelos import Estudiante, FiltroSolicitudes, Responsable, Solicitud  # noqa: E402


def solicitud(tipo=TipoSolicitud.CERTIFICADO, fecha=date(2025, 6, 1), **kw):
    return Solicitud(1, Estudiante("Ana Perez", "12345", "ana@mail.com"), tipo, "Certificado",
                     tipo.regla.prioridad_por_defecto, fecha, **kw)


class TestCatalogos(unittest.TestCase):
    def test_desde_texto_valido_e_invalido(self):
        self.assertIs(Estado.desde_texto("RESUELTA", "estado"), Estado.RESUELTA)
        with self.assertRaises(ValidacionError) as ctx:
            TipoSolicitud.desde_texto("VIAJE", "tipo")
        self.assertEqual("tipo", ctx.exception.campo)

    def test_todos_los_tipos_tienen_regla(self):
        for tipo in TipoSolicitud:
            self.assertGreater(tipo.regla.sla_dias, 0)
            self.assertTrue(tipo.regla.areas_permitidas)

    def test_estados_finales(self):
        self.assertTrue(Estado.RESUELTA.es_final)
        self.assertTrue(Estado.RECHAZADA.es_final)
        self.assertFalse(Estado.PENDIENTE.es_final)

    def test_orden_de_prioridad(self):
        self.assertLess(Prioridad.ALTA.orden, Prioridad.MEDIA.orden)
        self.assertLess(Prioridad.MEDIA.orden, Prioridad.BAJA.orden)


class TestSolicitud(unittest.TestCase):
    def test_flujo_completo(self):
        s = solicitud()
        s.asignar(Responsable("Carlos", Area.ALUMNADO))
        s.cambiar_estado(Estado.EN_PROCESO)
        s.cambiar_estado(Estado.RESUELTA)
        self.assertTrue(s.esta_cerrada)

    def test_no_pasa_a_en_proceso_sin_responsable(self):
        with self.assertRaises(TransicionInvalida):
            solicitud().cambiar_estado(Estado.EN_PROCESO)

    def test_transicion_invalida(self):
        with self.assertRaises(TransicionInvalida):
            solicitud().cambiar_estado(Estado.RESUELTA)

    def test_area_incorrecta(self):
        with self.assertRaises(AsignacionInvalida):
            solicitud().asignar(Responsable("X", Area.SECRETARIA))

    def test_no_asigna_si_esta_cerrada(self):
        s = solicitud()
        s.cambiar_estado(Estado.RECHAZADA)
        with self.assertRaises(AsignacionInvalida):
            s.asignar(Responsable("X", Area.ALUMNADO))

    def test_vencimiento_por_sla(self):
        s = solicitud(fecha=date(2025, 6, 1))  # certificado: 5 dias -> limite 2025-06-06
        self.assertFalse(s.esta_vencida(date(2025, 6, 6)))
        self.assertTrue(s.esta_vencida(date(2025, 6, 7)))

    def test_cerrada_nunca_vence(self):
        s = solicitud(estado=Estado.RESUELTA)
        self.assertFalse(s.esta_vencida(date(2030, 1, 1)))

    def test_filtro_combina_criterios_con_and(self):
        s = solicitud()
        self.assertTrue(FiltroSolicitudes(tipo=TipoSolicitud.CERTIFICADO, texto="CERTIF").coincide(s))
        self.assertFalse(FiltroSolicitudes(tipo=TipoSolicitud.CERTIFICADO, legajo="99999").coincide(s))


if __name__ == "__main__":
    unittest.main()
