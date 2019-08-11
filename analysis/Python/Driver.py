import Analysis
import Trend
import psycopg2
import sys

if len(sys.argv) < 2:
	print('Please specify a tablename!')
	raise SystemExit()

table_name = sys.argv[1]

if ';' in table_name:
	print('Why is there a semicolon in the table name? -_-')
	sys.exit()

def absolute_value_of_nth_element_in_tuple_callable(n):
	def g(tuple):
		return abs(tuple[n])
	return g


with open('C:/Development/SteamMarketAnalyzer/password.txt', 'r') as password_file:
	connection = psycopg2.connect(host='localhost',
								dbname='steammarket',
								user='postgres',
								password=password_file.read().rstrip(),
								port=7538)

cursor = connection.cursor()
cursor.execute(
	'WITH all_entries AS ('
	'	SELECT *,'
	'	ROW_NUMBER() OVER (PARTITION BY name ORDER BY time DESC) row_num'
	f'	FROM {table_name}'
	'),'
	'eligible_items AS ('
	'	SELECT name FROM all_entries '
	'	WHERE row_num = 1 AND volume > %s '
	'	AND price > %s AND price < %s'
	')'
	f' SELECT name, price, volume, time FROM {table_name} WHERE name IN (SELECT name FROM eligible_items) ORDER BY name DESC, time DESC',
	(Analysis.volume_thresh, Analysis.price_lower_thresh, Analysis.price_upper_thresh))

rows = cursor.fetchall()
cursor.close()
connection.close()

"""
GOAL
Sort items by abs(fluctuation)
Plot the top n items
"""

shortlist = list()

current_index = 0

# name price volume time

while current_index < len(rows):
	entries = list()

	current_item_name = rows[current_index][0]

	while current_index < len(rows) and rows[current_index][0] == current_item_name:
		entries.append(rows[current_index])
		current_index += 1

	prices = [entry[1] for entry in entries]

	fluc = Trend.fluctuationFirstToRest(prices)
	action = Analysis.suggested_action(prices, fluc)

	if action != Analysis.Action.IGNORE:
		shortlist.append( (current_item_name, fluc, prices, [entry[2] for entry in entries], [entry[3] for entry in entries], action) )
	
	entries.clear()

shortlist.sort(key=absolute_value_of_nth_element_in_tuple_callable(1), reverse=True)

[print(f'{row[0]}:{row[-1]}:{row[1]}') for row in shortlist]

Analysis.plot_items(shortlist)

# print (Analysis.suggested_action(8,[4, 8, 6, 4, 2, 0]))