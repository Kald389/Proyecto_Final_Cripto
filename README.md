# Proyecto_Final_Cripto

El objetivo de este proyecto es desarrollar un código de Python que permita mostrar las cotizaciones de criptomonedas en Streamlit. El código debe permitir visualizar los siguientes indicadores: crecimiento o decrecimiento del precio, estocástico, media móvil y volumen.
Para ello, el código utilizará las siguientes bibliotecas y herramientas:
•	Streamlit: es una librería de Python que permite crear aplicaciones web interactivas de forma sencilla.
•	Plotly: es una librería de Python para crear gráficos y visualizaciones interactivas.
•	Numpy: es una librería de Python para trabajar con matrices y arreglos.
•	KrakenAPI: se utilizó para acceder a datos del mercado de criptomonedas de la API de Kraken.
•	Datetime y Timedelta: son tipos de datos de Python para trabajar con fechas y horas.
El enfoque del proyecto se basa en los siguientes pasos:
1.	Obtención de las cotizaciones
El primer paso es obtener las cotizaciones de las criptomonedas. Para ello, el código utilizará la API de Kraken. La API de Kraken proporciona acceso a datos históricos y en tiempo real sobre las cotizaciones de las criptomonedas.
2.	Cálculo de los indicadores
Una vez que se tienen las cotizaciones, el siguiente paso es calcular los indicadores. Para ello, el código utilizará las funciones de NumPy y Pandas.
•	El estocástico es un indicador que mide la sobrecompra y la sobreventa de una criptomoneda.
•	La media móvil es un indicador de tendencia que suaviza los datos para identificar tendencias a largo plazo.
•	El volumen es una medida de la actividad comercial de una criptomoneda.
•	El crecimiento o decrecimiento del precio es un indicador que muestra si el precio de una criptomoneda está subiendo o bajando.

3.	Visualización de los datos
Por último, el código utilizará Plotly para mostrar los datos en gráficos interactivos. Plotly es una biblioteca muy potente y flexible, y se puede utilizar para crear gráficos de alta calidad de forma sencilla.
La interfaz gráfica de usuario debe ser intuitiva y fácil de usar. Debe permitir al usuario seleccionar la criptomoneda que desea visualizar, el período de tiempo que desea analizar y los indicadores que desea mostrar.
El código se desarrollará utilizando la versión 3.11 de Python. Se utilizarán las bibliotecas NumPy, Pandas, Streamlit y Plotly.
El código se probará utilizando un conjunto de datos de prueba. El conjunto de datos de prueba debe incluir datos de cotizaciones de criptomonedas de un período de tiempo determinado.
Una vez que el código esté probado, se publicará en un repositorio de GitHub.