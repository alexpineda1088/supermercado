# app.py — Sistema Avanzado de Gestión de Inventario (Flask)
from flask import Flask, render_template, request, redirect, url_for, flash
from models.producto import Producto
from models.inventario import Inventario
import db

app = Flask(__name__)
app.secret_key = 'dev-secret'  # Necesario para flash messages

# Inicializar base de datos
db.init_db()

# Crear inventario y cargar productos desde la DB
inventario = Inventario()
productos = db.obtener_todos()
inventario.cargar_desde_lista(productos)


# =========================
# Rutas de la aplicación
# =========================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/productos')
def productos_view():
    """Listar todos los productos"""
    todos = inventario.listar_todos()
    return render_template('products.html', productos=todos)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    """Formulario para añadir un producto"""
    if request.method == 'POST':
        try:
            id_p = int(request.form['id'])
            nombre = request.form['nombre'].strip()
            cantidad = int(request.form['cantidad'])
            precio = float(request.form['precio'])
        except ValueError:
            flash('Datos inválidos. Revise los campos.', 'danger')
            return redirect(url_for('nuevo_producto'))

        if inventario.existe_id(id_p):
            flash(f'El ID {id_p} ya existe.', 'warning')
            return redirect(url_for('nuevo_producto'))

        p = Producto(id_p, nombre, cantidad, precio)
        inventario.agregar_producto(p)
        db.insertar_producto(p.to_dict())
        flash('Producto agregado con éxito.', 'success')
        return redirect(url_for('productos_view'))

    return render_template('product_form.html', accion='Nuevo', producto=None)


@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    """Formulario para editar un producto"""
    p_db = db.obtener_por_id(id_producto)
    if not p_db:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos_view'))

    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        # Actualizar inventario y DB
        inventario.actualizar_producto(id_producto, nombre=nombre, cantidad=cantidad, precio=precio)
        db.actualizar_producto_db({'id': id_producto, 'nombre': nombre, 'cantidad': cantidad, 'precio': precio})
        flash('Producto actualizado con éxito.', 'success')
        return redirect(url_for('productos_view'))

    return render_template('product_form.html', accion='Editar', producto=p_db)


@app.route('/productos/eliminar/<int:id_producto>', methods=['POST'])
def eliminar(id_producto):
    """Eliminar un producto"""
    if inventario.eliminar_producto(id_producto):
        db.eliminar_producto_db(id_producto)
        flash('Producto eliminado con éxito.', 'success')
    else:
        flash('Producto no encontrado.', 'danger')
    return redirect(url_for('productos_view'))


@app.route('/productos/buscar', methods=['GET'])
def buscar():
    """Buscar productos por nombre"""
    q = request.args.get('q', '').strip()
    resultados = []
    if q:
        resultados = inventario.buscar_por_nombre(q)
    return render_template('products.html', productos=resultados, query=q)


# =========================
# Ejecutar la aplicación
# =========================
if __name__ == '__main__':
    app.run(debug=True)
