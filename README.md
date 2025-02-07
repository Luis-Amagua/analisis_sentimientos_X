# Análisis de Sentimiento en Tweets
## Carga de Datos
Se utiliza twikit para buscar y recolectar tweets relacionados con palabras clave predefinidas.
Los datos recolectados incluyen texto del tweet, usuario, métricas de interacción (retweets, favoritos) y marcas temporales.

## Limpieza de Texto

Se eliminan URLs, menciones y hashtags para evitar información irrelevante en el análisis.
Se eliminan signos de puntuación para mejorar la calidad del texto.
Se convierten emojis a texto usando la librería emoji.
Se convierte el texto a minúsculas para estandarizar los datos.
Selección del Modelo de Análisis de Sentimiento
Se utiliza un modelo preentrenado de BERT:

Modelo: nlptown/bert-base-multilingual-uncased-sentiment.
Pertenece a la familia BERT (Bidirectional Encoder Representations from Transformers), desarrollado por Google.
Especializado en análisis de sentimiento multilingüe, lo que permite evaluar tweets en varios idiomas.
Usa una clasificación de 1 a 5, que se agrupa en positivo, negativo o neutral.

Se procesa cada tweet con el modelo y se obtiene su puntuación de sentimiento.
Se asigna la categoría:
- positivo (puntuaciones > 3)
- negativo (< 3)
- neutral (= 3)
  
Se limita el texto a 512 caracteres, la capacidad máxima del modelo.
Exportación de Resultados
Se guardan los tweets analizados en un nuevo archivo CSV para futuras consultas.

## Visualización de Resultados

Se cuentan los tweets clasificados en cada categoría.
Se crea un gráfico de pastel para visualizar la distribución de sentimientos.
Este proceso permite analizar opiniones en Twitter de forma automatizada, mejorando la comprensión de la percepción pública sobre un tema específico.

![image](https://github.com/user-attachments/assets/714734d4-58f7-4e82-9cc5-a5a91faef6ac)
