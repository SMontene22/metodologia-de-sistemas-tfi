import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solicitudes.cli import main  # noqa: E402


class TestCli(unittest.TestCase):
    def test_demo_registra_y_muestra_reporte(self):
        with tempfile.TemporaryDirectory() as d:
            salida = io.StringIO()
            with contextlib.redirect_stdout(salida):
                main(os.path.join(d, "s.json"))
        self.assertIn("=== REPORTE DE SOLICITUDES ===", salida.getvalue())
        self.assertIn("Ana Perez (12345)", salida.getvalue())


if __name__ == "__main__":
    unittest.main()
