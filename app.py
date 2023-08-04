from flask import Flask, render_template, request
from decimal import Decimal

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        primeros_compradores = int(request.form['primeros_compradores'])
        nivel_descuento = Decimal(request.form['nivel_descuento']) / 100  # Convertir a decimal
        porcentaje_retorno = Decimal(request.form['porcentaje_retorno']) / 100  # Convertir a decimal
        AOV = Decimal(request.form['AOV'])
        split_nivel = Decimal(request.form['split_nivel']) / 100  # Convertir a decimal

        # Calcular los ingresos sin Dynamic Discounts.
        ingresos_sin_dd = primeros_compradores * porcentaje_retorno * AOV * (1 - nivel_descuento)

        # Calcular los ingresos con Dynamic Discounts.
        descuento_nivel_2 = max(nivel_descuento - Decimal('0.05'), Decimal('0.05'))  # Convertir float a Decimal
        ingresos_nivel_1 = primeros_compradores * split_nivel * porcentaje_retorno * AOV * (1 - nivel_descuento)
        ingresos_nivel_2 = primeros_compradores * (1 - split_nivel) * porcentaje_retorno * AOV * (1 - descuento_nivel_2)
        ingresos_con_dd = ingresos_nivel_1 + ingresos_nivel_2
        diferencia_ingresos = ingresos_con_dd - ingresos_sin_dd
        diferencia_porcentual = ((ingresos_con_dd - ingresos_sin_dd) / ingresos_sin_dd) * 100
        proyeccion_anual = diferencia_ingresos * 12

        # Pasar los resultados a la plantilla para mostrarlos al usuario.
        return render_template('results.html',
                               ingresos_sin_dd=ingresos_sin_dd,
                               ingresos_con_dd=ingresos_con_dd,
                               diferencia_ingresos=diferencia_ingresos,
                               diferencia_porcentual=diferencia_porcentual,
                               proyeccion_anual=proyeccion_anual,
                               primeros_compradores=primeros_compradores,
                               nivel_descuento=nivel_descuento,
                               porcentaje_retorno=porcentaje_retorno,
                               AOV=AOV,
                               split_nivel=split_nivel)

    else:
        # Si el método es GET, simplemente renderizamos el formulario.
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
