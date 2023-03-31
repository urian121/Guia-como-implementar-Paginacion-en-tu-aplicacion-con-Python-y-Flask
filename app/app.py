from flask import Flask, request, render_template
from flask_paginate import Pagination #Importando paquete de paginación
from conexionBD import connectionBD #Importando conexión a BD


# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)


# Creando mi Decorador Home
@app.route("/")
def inicio():
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)

    # Contar el número total de registros
    cursor.execute(
        "SELECT COUNT(*) AS total FROM pais ")
    count = cursor.fetchone()['total']

    # Obtener el número de página actual y la cantidad de resultados por página
    page_num = request.args.get('page', 1, type=int)
    per_page = 6

    # Calcular el índice del primer registro y limitar la consulta a un rango de registros
    start_index = (page_num - 1) * per_page + 1

    querySQL = (f"SELECT id, paisnombre "
                f"FROM pais WHERE id >= 1 "
                f"ORDER BY id DESC LIMIT {per_page} OFFSET {start_index - 1}")
    cursor.execute(querySQL)
    paises = cursor.fetchall()

    # Calcular el índice del último registro
    end_index = min(start_index + per_page, count)
    # end_index = start_index + per_page - 1
    if end_index > count:
        end_index = count

    # Crear objeto paginable
    pagination = Pagination(page=page_num, total=count, per_page=per_page,
                            display_msg=f"Mostrando registros {start_index} - {end_index} de un total de <strong>({count})</strong>")
    conexion_MySQLdb.commit()


    return render_template('public/index.html', paises=paises, pagination=pagination)




# Ejecutando el objeto Flask
if __name__ == '__main__':
    app.run(debug=True, port=5020)
