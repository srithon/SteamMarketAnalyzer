WITH deleted AS
(DELETE FROM csgo_item_names returning *),
inserted AS
(SELECT name, ROW_NUMBER() OVER (PARTITION BY name ORDER BY name) RowNum
	FROM deleted)
INSERT INTO csgo_item_names SELECT name FROM inserted
WHERE RowNum = 1;
