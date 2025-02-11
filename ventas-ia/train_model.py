import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Configuración de conexión con MySQL
DB_CONFIG = {
    "host": "pruebai.mysql.database.azure.com",
    "user": "oebwvuukfg",
    "password": "Afsmnz78",
    "database": "ventas_db"
}

# Conectar a MySQL y cargar datos históricos
conn = mysql.connector.connect(**DB_CONFIG)
query = "SELECT cliente_id, monto_venta, monto_cobranza, dias_atraso FROM historico"
df = pd.read_sql(query, conn)
conn.close()

# Convertir la variable objetivo (1 = buen pagador, 0 = mal pagador)
df['buena_paga'] = df['dias_atraso'].apply(lambda x: 1 if x == 0 else 0)

# Variables de entrada (X) y salida (y)
X = df[['monto_venta', 'monto_cobranza', 'dias_atraso']]
y = df['buena_paga']

# Separar datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión del modelo: {accuracy * 100:.2f}%')

# Guardar el modelo en un archivo para usarlo después
joblib.dump(model, 'modelo_credito.pkl')
print("Modelo guardado como modelo_credito.pkl")
