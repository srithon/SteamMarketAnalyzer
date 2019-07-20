WITH deleted AS
(DELETE FROM tf2_item_names returning *),
inserted AS
(SELECT name, ROW_NUMBER() OVER (PARTITION BY name ORDER BY name) RowNum
	FROM deleted)
INSERT INTO tf2_item_names SELECT name FROM inserted
WHERE RowNum = 1;
