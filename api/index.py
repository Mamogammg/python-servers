from flask import Flask, request, jsonify

app = Flask(__name__)

# Diccionario inicial con el estado de los bits
bits = {"1": False, "2": False, "3": False, "4": False, "5": False, "6": False, "7": False, "Send": False}

# Función para obtener el carácter basado en el estado de los bits
def obtener_caracter(bits):
    # Combinar bits 1-5 para obtener un índice numérico
    indice = sum((1 << (i - 1)) * bits[str(i)] for i in range(1, 6))
    
    # Determinar si es una letra
    if bits["7"]:
        # Verificar si es mayúscula o minúscula
        es_mayuscula = bits["6"]
        # Letras y caracteres especiales
        if 1 <= indice <= 26:  # Letras a-z
            letra = chr(ord('A') + indice - 1) if es_mayuscula else chr(ord('a') + indice - 1)
        elif indice == 27:  # Letra ñ o Ñ
            letra = 'Ñ' if es_mayuscula else 'ñ'
        elif 28 <= indice <= 32:  # Letras con tilde á, é, í, ó, ú
            tildes = ['á', 'é', 'í', 'ó', 'ú']
            letra = tildes[indice - 28].upper() if es_mayuscula else tildes[indice - 28]
        else:
            letra = ' '  # Blanco para valores fuera del rango
        
    else:
        # No es letra, procesar como número o símbolo especial
        if 1 <= indice <= 10:  # Números 0-9
            letra = str(indice - 1)
        elif 11 <= indice <= 16:  # Símbolos especiales
            simbolos = ['.', ',', ':', '-', '_', '"']
            letra = simbolos[indice - 11]
        else:
            letra = ' '  # Blanco para valores fuera del rango
        
    return letra

# Ruta para controlar los bits
@app.route('/<bit>/<estado>', methods=['POST'])
def controlar_bit(bit, estado):
    print(bits)
    
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

    # Imprimir carácter si bitSend está activo
    if bits["Send"]:
        caracter = obtener_caracter(bits)
        print(f"Carácter generado: {caracter}")
    
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
