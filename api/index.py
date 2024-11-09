from flask import Flask, request, jsonify

app = Flask(__name__)

bits = {"1": False, "2": False, "3": False, "4": False, "5": False, "6": False, "Send": False}

# Ruta dinámica que captura el "bit" y el "estado" de la URL
@app.route('/<bit>/<estado>', methods=['POST'])
def controlar_bit(bit, estado):
    # Comprobar si el estado es válido (on o off)
    if estado not in ['on', 'off']:
        return jsonify({"error": "Estado inválido, usa 'on' o 'off'"}), 400
    
    number = bit.removeprefix("bit")
    bits[number] = True if estado == 'on' else False

    print(bit+" goes "+estado+".")

    # Respuesta con confirmación del cambio de estado
    return jsonify({"bit": bit, "estado": estado, "mensaje": f"Bit {bit} configurado a {estado}"}), 200

# Ejecutar el servidor en localhost:5000
if __name__ == '__main__':
    app.run(debug=True)
