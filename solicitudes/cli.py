"""Punto de entrada de demostracion (equivale al bloque __main__ de la version inicial)."""
from .modelos import DatosSolicitud
from .reloj import RelojSistema
from .repositorio import RepositorioJSON
from .reporte import generar_reporte
from .servicio import ServicioSolicitudes


def main(ruta="solicitudes.json"):
    servicio = ServicioSolicitudes(RepositorioJSON(ruta), RelojSistema())
    servicio.registrar(DatosSolicitud("Ana Perez", "12345", "ana@mail.com", "CERTIFICADO",
                                      "Certificado de alumno regular"))
    print(generar_reporte(servicio.listar(), servicio.hoy()))
