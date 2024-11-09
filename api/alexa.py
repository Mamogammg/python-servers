from flask import Flask, request, jsonify

app = Flask(__name__)

# Diccionario inicial con el estado de los bits
bits = {
    "1": False, "2": False, "3": False, "4": False, "5": False,
    "6": False, "7": False, "Send": False
}

# Tabla de caracteres para valores especiales
caracteres_especiales = "0123456789.,:-_\"     "  # Índices 0-15 son estos caracteres

# Función para interpretar el carácter según el estado de los bits
def interpretar_caracter():
    # Leer los valores de los bits
    es_letra = bits["7"]
    es_mayuscula = bits["6"]

    # Calcular el valor de bits 1-5 como un número binario
    valor_bits = sum(2**(i-1) if bits[str(i)] else 0 for i in range(1, 6))

    # Interpretar como letra
    if es_letra:
        # Si es una letra, determinar si es una letra común, ñ o una vocal con acento
        if 0 <= valor_bits <= 25:  # Letras a-z
            caracter = chr(ord('A') + valor_bits) if es_mayuscula else chr(ord('a') + valor_bits)
        elif valor_bits == 26:  # Letra ñ
            caracter = 'Ñ' if es_mayuscula else 'ñ'
        elif 27 <= valor_bits <= 31:  # Letras con acento
            acentos = ["Á", "É", "Í", "Ó", "Ú"] if es_mayuscula else ["á", "é", "í", "ó", "ú"]
            caracter = acentos[valor_bits - 27]
        else:
            caracter = " "  # Blanco si el valor está fuera de rango
    else:
        # Interpretar como carácter especial o número
        if 0 <= valor_bits <= 9:
            caracter = str(valor_bits)  # Dígitos 0-9
        elif 10 <= valor_bits <= 15:
            caracter = caracteres_especiales[valor_bits - 10]  # Caracteres especiales
        else:
            caracter = " "  # Blanco si el valor está fuera de rango

    return caracter

# Ruta para actualizar el estado de los bits
@app.route('/<bit>/<estado>', methods=['POST'])
def controlar_bit(bit, estado):
    # Comprobar si el estado es válido (on o off)
    if estado not in ['on', 'off']:
        return jsonify({"error": "Estado inválido, usa 'on' o 'off'"}), 400
    
    # Obtener el número del bit quitando el prefijo "bit"
    number = bit.replace("bit", "", 1)
    
    # Validar si el bit existe en el diccionario `bits`
    if number not in bits:
        return jsonify({"error": "Bit no válido"}), 400

    # Actualizar el estado del bit en el diccionario
    bits[number] = (estado == 'on')

    print(f"{bit} goes {estado}.")

    print(bits)

    # Comprobar si el bit `Send` está activado para interpretar el carácter
    if bits["Send"]:
        caracter = interpretar_caracter()
        print(f"Carácter interpretado: '{caracter}'")
        # Desactivar el bit Send después de procesar
        bits["Send"] = False

    # Respuesta con el estado de todos los bits
    return jsonify({
        "bit": bit,
        "estado": estado,
        "mensaje": f"Bit {bit} configurado a {estado}",
        "estado_actual": bits  # Muestra el estado de todos los bits
    }), 200

# Ejecutar el servidor en localhost:5000
if __name__ == '__main__':
    app.run(debug=True)
