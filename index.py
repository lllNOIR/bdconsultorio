from flask import Flask, render_template, request,redirect, url_for, flash
import pymysql


app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'

def connect_to_db():
    return pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='con_medico',
    cursorclass=pymysql.cursors.DictCursor,
    ssl_disabled=True 
    )

@app.route("/")
def index():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pacientes")
    pacientes = cur.fetchall()
    cur.execute("SELECT * FROM consultorios")
    consultorios = cur.fetchall()
    cur.execute("SELECT * FROM medicos")
    medicos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('registrar.html', pacientes=pacientes, consultorios=consultorios, medicos=medicos)

@app.route('/pacientes', methods=['GET', 'POST'])
def paciente():
    if request.method == 'POST':
        identificacion = request.form['PACidentificacion']
        nombres = request.form['PACnombres']
        apellidos = request.form['PACapellidos']
        fechaNacimiento = request.form['PACfechaNacimiento']
        Sexo = request.form['PACSexo']
        CONnumero = request.form['CONnumero']
        MEDidentificacion = request.form['MEDidentificacion']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO pacientes (PACidentificacion, PACnombres, PACapellidos, PACfechaNacimiento, PACSexo) VALUES (%s,%s,%s,%s,%s)",
                (identificacion, nombres, apellidos, fechaNacimiento, Sexo)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash('Paciente agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar paciente: {e}")
        return redirect(url_for('paciente'))

    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pacientes")
            pacientes = cursor.fetchall()
            cursor.execute("SELECT * FROM consultorios")
            consultorios = cursor.fetchall()
            cursor.execute("SELECT * FROM medicos")
            medicos = cursor.fetchall()
        return render_template('registrar.html', pacientes=pacientes, consultorios=consultorios, medicos=medicos)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrar.html', pacientes=[])

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        identificacion = request.form['PACidentificacion']
        nombres = request.form['PACnombres']
        apellidos = request.form['PACapellidos']
        fechaNacimiento = request.form['PACfechaNacimiento']
        Sexo = request.form['PACSexo']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO pacientes (PACidentificacion, PACnombres, PACapellidos, PACfechaNacimiento, PACSexo) VALUES (%s,%s,%s,%s,%s)",
                (identificacion, nombres, apellidos, fechaNacimiento, Sexo))
            conn.commit()
            cur.close()
            conn.close()
            flash('paciente agregado correctamente')
            return redirect(url_for('registrar'))
        except Exception as e:
            flash(f"Error al agregar paciente: {e}")
            return redirect(url_for('registrar'))
    # Consulta para mostrar la tabla
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pacientes")
            pacientes = cursor.fetchall()
        return render_template('registrar.html', pacientes=pacientes)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrar.html', pacientes=[])

@app.route('/elimina/<string:PACidentificacion>', methods=['POST'])
def elimina(PACidentifiacion):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM pacientes WHERE PACidentificacion=%s", (PACidentifiacion,))
        conn.commit()
        cur.close()
        conn.close()
        flash('Aprendiz eliminado correctamente')
    except Exception as e:
        flash(f"Error al eliminar aprendiz: {e}")
    return redirect(url_for('registrar'))

@app.route('/elimina-paciente/<string:PACidentificacion>', methods=['POST'])
def eliminaPAC(PACidentificacion):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM pacientes WHERE PACidentificacion=%s", (PACidentificacion,))
        conn.commit()
        cur.close()
        conn.close()
        flash('Paciente eliminado correctamente')
    except Exception as e:
        flash(f"Error al eliminar paciente: {e}")
    return redirect(url_for('registrar'))

@app.route('/edita/<PACidentificacion>', methods=['GET', 'POST'])
def editaPAC(PACidentificacion):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pacientes WHERE PACidentificacion=%s", (PACidentificacion,))
        paciente = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"Error al obtener paciente: {e}")
        return redirect(url_for('registrar'))

    if request.method == 'POST':
        PACnombres = request.form['PACnombres']
        PACapellidos = request.form['PACapellidos']
        PACfechaNacimiento = request.form['PACfechaNacimiento']
        PACSexo = request.form['PACSexo']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("""
                UPDATE pacientes
                SET PACnombres=%s, PACapellidos=%s, PACfechaNacimiento=%s, PACSexo=%s
                WHERE PACidentificacion=%s
            """, (PACnombres, PACapellidos, PACfechaNacimiento, PACSexo, PACidentificacion))
            conn.commit()
            cur.close()
            conn.close()
            flash('Paciente actualizado correctamente')
            return redirect(url_for('registrar'))
        except Exception as e:
            flash(f"Error al actualizar paciente: {e}")
            return redirect(url_for('registrar'))
    return render_template('editarPAC.html', paciente=paciente)

@app.route('/consultorios', methods=['GET', 'POST'])
def consultorios():
    if request.method == 'POST':
        numero = request.form['CONnumero']
        nombre = request.form['CONnombre']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO consultorios (CONnumero, CONnombre) VALUES (%s,%s)", (numero, nombre))
            conn.commit()
            cur.close()
            conn.close()
            flash('Consultorio agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar consultorio: {e}")
        return redirect(url_for('registrarCON'))
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM consultorios")
            consultorios = cursor.fetchall()
        return render_template('registrarCON.html', consultorios=consultorios)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrarCON.html', consultorios=[])

@app.route('/registrarCON', methods=['GET', 'POST'])
def registrarCON():
    if request.method == 'POST':
        numero = request.form['CONnumero']
        nombre = request.form['CONnombre']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO consultorios (CONnumero, CONnombre) VALUES (%s,%s)", (numero, nombre))
            conn.commit()
            cur.close()
            conn.close()
            flash('Consultorio agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar consultorio: {e}")
        return redirect(url_for('registrarCON'))
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM consultorios")
            consultorios = cursor.fetchall()
        return render_template('registrarCON.html', consultorios=consultorios)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrarCON.html', consultorios=[])

@app.route('/elimina-consultorio/<string:CONnumero>', methods=['POST'])
def eliminaCON(CONnumero):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM consultorios WHERE CONnumero=%s", (CONnumero,))
        conn.commit()
        cur.close()
        conn.close()
        flash('Consultorio eliminado correctamente')
    except Exception as e:
        flash(f"Error al eliminar consultorio: {e}")
    return redirect(url_for('registrarCON'))

@app.route('/edita-consultorio/<string:CONnumero>', methods=['GET', 'POST'])
def editaCON(CONnumero):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM consultorios WHERE CONnumero=%s", (CONnumero,))
        consultorio = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"Error al obtener consultorio: {e}")
        return redirect(url_for('registrarCON'))

    if request.method == 'POST':
        CONnombre = request.form['CONnombre']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("""
                UPDATE consultorios
                SET CONnombre=%s
                WHERE CONnumero=%s
            """, (CONnombre, CONnumero))
            conn.commit()
            cur.close()
            conn.close()
            flash('Consultorio actualizado correctamente')
            return redirect(url_for('registrarCON'))
        except Exception as e:
            flash(f"Error al actualizar consultorio: {e}")
            return redirect(url_for('registrarCON'))
    return render_template('editarCON.html', consultorio=consultorio)
   
@app.route('/medicos', methods=['GET', 'POST'])
def medicos():
    if request.method == 'POST':
        identificacion = request.form['MEDidentificacion']
        nombres = request.form['MEDnombres']
        apellidos = request.form['MEDapellidos']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO medicos (MEDidentificacion, MEDnombres, MEDapellidos) VALUES (%s,%s,%s)",
                        (identificacion, nombres, apellidos))
            conn.commit()
            cur.close()
            conn.close()
            flash('Médico agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar médico: {e}")
        return redirect(url_for('registrarMED'))
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM medicos")
            medicos = cursor.fetchall()
        return render_template('registrarMED.html', medicos=medicos)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrarMED.html', medicos=[])

@app.route('/registrarMED', methods=['GET', 'POST'])
def registrarMED():
    if request.method == 'POST':
        identificacion = request.form['MEDidentificacion']
        nombres = request.form['MEDnombres']
        apellidos = request.form['MEDapellidos']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO medicos (MEDidentificacion, MEDnombres, MEDapellidos) VALUES (%s,%s,%s)",
                        (identificacion, nombres, apellidos))
            conn.commit()
            cur.close()
            conn.close()
            flash('Médico agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar médico: {e}")
        return redirect(url_for('registrarMED'))
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM medicos")
            medicos = cursor.fetchall()
        return render_template('registrarMED.html', medicos=medicos)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrarMED.html', medicos=[])

@app.route('/elimina-medico/<string:MEDidentificacion>', methods=['POST'])
def eliminaMED(MEDidentificacion):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM medicos WHERE MEDidentificacion=%s", (MEDidentificacion,))
        conn.commit()
        cur.close()
        conn.close()
        flash('Médico eliminado correctamente')
    except Exception as e:
        flash(f"Error al eliminar médico: {e}")
    return redirect(url_for('registrarMED'))

@app.route('/edita-medico/<string:MEDidentificacion>', methods=['GET', 'POST'])
def editaMED(MEDidentificacion):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicos WHERE MEDidentificacion=%s", (MEDidentificacion,))
        medico = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"Error al obtener médico: {e}")
        return redirect(url_for('registrarMED'))

    if request.method == 'POST':
        MEDnombres = request.form['MEDnombres']
        MEDapellidos = request.form['MEDapellidos']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("""
                UPDATE medicos
                SET MEDnombres=%s, MEDapellidos=%s
                WHERE MEDidentificacion=%s
            """, (MEDnombres, MEDapellidos, MEDidentificacion))
            conn.commit()
            cur.close()
            conn.close()
            flash('Médico actualizado correctamente')
            return redirect(url_for('registrarMED'))
        except Exception as e:
            flash(f"Error al actualizar médico: {e}")
            return redirect(url_for('registrarMED'))
    return render_template('editarMED.html', medico=medico)




if __name__ == '__main__':
    app.run(debug=True)
