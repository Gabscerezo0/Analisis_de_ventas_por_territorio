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

