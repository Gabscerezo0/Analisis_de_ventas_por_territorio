#librerias para descargar archivo de sql
from sqlalchemy import create_engine 
import pandas as pd
#librerias para visualizar datos
import matplotlib.pyplot as plt
import seaborn as sns
#libreria para percentiles
import numpy as np

server="--------------------"
database="AdventureWorks2017"

engine = create_engine(f"mssql+pyodbc://{server}/{database}?driver=SQL+Server&trusted_connection=yes")

query = """
SELECT 
	st.Name AS nombre_territorio,
	so.TerritoryID,
	ROUND(SUM(so.SubTotal),2) AS total_de_ventas,
	COUNT(so.SalesOrderID) AS cantidad_de_ordenes,
	ROUND(AVG(so.SubTotal),2) AS prom_de_venta_por_orden
FROM AdventureWorks2017.Sales.SalesOrderHeader so
LEFT JOIN AdventureWorks2017.Sales.SalesTerritory st
ON st.TerritoryID=so.TerritoryID
GROUP BY st.Name,so.TerritoryID
ORDER BY total_de_ventas ASC
"""
with engine.connect() as conn:
    f=pd.read_sql(query,conn)

print(f.head())

#bar chart
f.plot( figsize=(12, 6))
sns.barplot(x='nombre_territorio', y='total_de_ventas', data=f, palette='viridis')
plt.xlabel('Territorio')
plt.ylabel('Ventas')
plt.title('Total de ventas por territorio')
plt.legend().remove()
plt.show()

#box plot
plt.figure(figsize=(14, 7))
sns.boxplot(x='total_de_ventas', data=f, color='lightblue',vert=False)
plt.title('Distribución de Ventas por Territorio', fontsize=16)
plt.xlabel('Total de Ventas ($)', fontsize=12)
plt.show()

##no hay valores atipicos de acuerdo al box plot
##para ello veamos que pasa con un histograma

plt.figure(figsize=(10, 6))
sns.histplot(f['total_de_ventas'], bins=10, kde=True, color='royalblue', alpha=0.7)
plt.xlabel('Total de Ventas ($)')
plt.ylabel('Frecuencia')
plt.title('Distribución de Ventas por Territorio')
plt.show()
# ¿Qué podemos analizar con este gráfico?
# ¿La distribución es normal o está sesgada?
# Si el histograma tiene forma de campana, es posible que estemos ante una distribución normal.
# Si notamos que hay más valores a la izquierda o a la derecha, eso indica que hay un sesgo en la distribución.
# ¿Existen valores extremos?
# Si vemos barras solitarias en los extremos, podrían ser considerados valores atípicos.
# ¿Y cómo se agrupan las ventas?
# Podemos observar si la mayoría de los territorios tienen ventas dentro de un rango específico.

