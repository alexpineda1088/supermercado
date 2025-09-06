# run_console.py — Menú en consola para gestionar inventario
from models.producto import Producto
from models.inventario import Inventario
import db

MENU = '''
==============================
Sistema Inventario (Consola)
==============================
1) Listar todos los productos
2) Buscar por nombre
3) Agregar producto
4) Editar producto
5) Eliminar producto
0) Salir
==============================
Elija una opción: '''


def main():
    # Inicializar base de datos y cargar inventario
    db.init_db()
    inventario = Inventario()
    inventario.cargar_desde_lista(db.obtener_todos())

    while True:
        opcion = input(MENU).strip()

        if opcion == '1':
            print("\n--- LISTA DE PRODUCTOS ---")
            for p in inventario.listar_todos():
                print(p)
            print("--------------------------\n")

        elif opcion == '2':
            nombre = input("Nombre a buscar: ").strip()
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                print(f"\nResultados para '{nombre}':")
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos con ese nombre.")
            print()

        elif opcion == '3':
            try:
                id_p = int(input("ID: "))
                nombre = input("Nombre: ").strip()
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
            except ValueError:
                print("Entrada inválida. Intente de nuevo.\n")
                continue

            if inventario.existe_id(id_p):
                print(f"El ID {id_p} ya existe.\n")
                continue

            producto = Producto(id_p, nombre, cantidad, precio)
            inventario.agregar_producto(producto)
            db.insertar_producto(producto.to_dict())
            print("Producto agregado con éxito.\n")

        elif opcion == '4':
            try:
                id_p = int(input("ID del producto a editar: "))
                if not inventario.existe_id(id_p):
                    print("No existe ese producto.\n")
                    continue

                nombre = input("Nuevo nombre (enter para no cambiar): ").strip()
                cantidad_input = input("Nueva cantidad (enter para no cambiar): ").strip()
                precio_input = input("Nuevo precio (enter para no cambiar): ").strip()

                kwargs = {}
                if nombre:
                    kwargs['nombre'] = nombre
                if cantidad_input:
                    kwargs['cantidad'] = int(cantidad_input)
                if precio_input:
                    kwargs['precio'] = float(precio_input)

                inventario.actualizar_producto(id_p, **kwargs)
                # Actualizar DB
                producto_actualizado = inventario.productos[id_p]
                db.actualizar_producto_db(producto_actualizado.to_dict())
                print("Producto actualizado con éxito.\n")
            except ValueError:
                print("Datos inválidos. Intente de nuevo.\n")

        elif opcion == '5':
            try:
                id_p = int(input("ID del producto a eliminar: "))
                if inventario.eliminar_producto(id_p):
                    db.eliminar_producto_db(id_p)
                    print("Producto eliminado con éxito.\n")
                else:
                    print("No existe ese producto.\n")
            except ValueError:
                print("ID inválido. Intente de nuevo.\n")

        elif opcion == '0':
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente de nuevo.\n")


if __name__ == "__main__":
    main()
