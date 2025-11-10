from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Variable qui dit si oui ou non je suis en production afin de desactiver le mode débogage
production = False

@app.route('/')
def home():
    return "🍕 Pizzeria - Le serveur fonctionne!"

if __name__ == '__main__':
    print("🍕 Serveur démarré sur http://localhost:5000")

    if(production):
        app.run(debug=False)  # Desactivation du mode debogage
    else:
        app.run(debug=True)  # Activation du mode debogage