# supermercado
# Sistema Avanzado de Gestión de Inventario — Supermercado

## Descripción
Aplicación web desarrollada en **Flask** para la gestión de inventario de un supermercado.  
Incluye:
- **POO**: Clases `Producto` e `Inventario` con colecciones (diccionarios, sets, listas).
- **SQLite**: Persistencia de los productos.
- **Interfaz Web**: CRUD completo con plantillas Jinja2.
- **Interfaz en Consola**: Script `run_console.py` para gestionar inventario sin navegador.

## Requisitos
- Python 3.9 o superior
- Flask
- SQLite (incluido en Python)

## Instalación
```bash
git clone https://github.com/usuario/supermercado-inventario.git
cd supermercado-inventario
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\\Scripts\\activate   # Windows
pip install -r requirements.txt
