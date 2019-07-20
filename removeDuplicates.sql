WITH ItemNamesCTE AS (
	SELECT *, ROW_NUMBER() OVER (PARTITION BY name ORDER BY name) AS RowNum
	from tf2_item_names
)
DELETE FROM ItemNamesCTE WHERE RowNum > 1;
