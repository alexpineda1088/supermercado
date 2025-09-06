# models/producto.py

class Producto:
    """
    Clase Producto que representa un ítem del inventario.
    Atributos: id, nombre, cantidad, precio
    """
    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        self._id = int(id_producto)
        self._nombre = str(nombre)
        self._cantidad = int(cantidad)
        self._precio = float(precio)

    # =========================
    # Getters y Setters
    # =========================
    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        self._nombre = str(nuevo_nombre)

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad: int):
        self._cantidad = int(nueva_cantidad)

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio: float):
        self._precio = float(nuevo_precio)

    # =========================
    # Métodos útiles
    # =========================
    def to_dict(self) -> dict:
        """
        Representación del producto como diccionario.
        Útil para guardar en DB o JSON.
        """
        return {
            "id": self._id,
            "nombre": self._nombre,
            "cantidad": self._cantidad,
            "precio": self._precio
        }

    def __repr__(self):
        return f"Producto(id={self._id}, nombre='{self._nombre}', cantidad={self._cantidad}, precio={self._precio:.2f})"
