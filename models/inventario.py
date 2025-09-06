# models/inventario.py
from typing import Dict, List
from .producto import Producto

class Inventario:
    """
    Clase Inventario para gestionar productos usando:
    - Diccionario `productos` para acceso O(1) por ID.
    - Índice secundario `_index_nombre` para búsquedas rápidas por nombre.
    """
    def __init__(self):
        # Diccionario principal: id_producto -> Producto
        self.productos: Dict[int, Producto] = {}
        # Índice secundario: nombre.lower() -> set de IDs
        self._index_nombre: Dict[str, set] = {}

    # =========================
    # Métodos privados
    # =========================
    def _indexar(self, producto: Producto):
        """Agrega el producto al índice por nombre"""
        key = producto.nombre.lower()
        if key not in self._index_nombre:
            self._index_nombre[key] = set()
        self._index_nombre[key].add(producto.id)

    def _desindexar(self, producto: Producto):
        """Elimina el producto del índice por nombre"""
        key = producto.nombre.lower()
        if key in self._index_nombre:
            self._index_nombre[key].discard(producto.id)
            if not self._index_nombre[key]:
                del self._index_nombre[key]

    # =========================
    # Métodos públicos
    # =========================
    def agregar_producto(self, producto: Producto) -> bool:
        """Agrega un producto. Retorna False si el ID ya existe."""
        if producto.id in self.productos:
            return False
        self.productos[producto.id] = producto
        self._indexar(producto)
        return True

    def eliminar_producto(self, id_producto: int) -> bool:
        """Elimina un producto por ID. Retorna False si no existe."""
        if id_producto not in self.productos:
            return False
        producto = self.productos.pop(id_producto)
        self._desindexar(producto)
        return True

    def actualizar_producto(self, id_producto: int, nombre=None, cantidad=None, precio=None) -> bool:
        """Actualiza los atributos de un producto por ID"""
        if id_producto not in self.productos:
            return False
        p = self.productos[id_producto]
        if nombre is not None and nombre != p.nombre:
            self._desindexar(p)
            p.nombre = nombre
            self._indexar(p)
        if cantidad is not None:
            p.cantidad = cantidad
        if precio is not None:
            p.precio = precio
        return True

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        """Busca productos por nombre (case-insensitive)"""
        key = nombre.lower()
        ids = self._index_nombre.get(key, set())
        return [self.productos[i] for i in ids]

    def listar_todos(self) -> List[Producto]:
        """Devuelve todos los productos en el inventario"""
        return list(self.productos.values())

    def existe_id(self, id_producto: int) -> bool:
        """Verifica si existe un producto por ID"""
        return id_producto in self.productos

    def cargar_desde_lista(self, lista_dicts: List[Dict]):
        """Carga productos desde una lista de diccionarios (por ejemplo DB)"""
        for d in lista_dicts:
            p = Producto(d['id'], d['nombre'], d['cantidad'], d['precio'])
            self.agregar_producto(p)
