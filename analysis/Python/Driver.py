import Analysis
import Trend
import psycopg2

table_name = 'tf2'

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
cursor.execute(f'SELECT DISTINCT name FROM {table_name}')
item_names = [item[0] for item in cursor.fetchall()]

"""
GOAL
Sort items by abs(fluctuation)
Plot the top n items
"""

shortlist = list()

for item in item_names:
	cursor.execute(f'SELECT volume, price, time FROM {table_name} WHERE name=%s ORDER BY time DESC', (item,))
	entries = cursor.fetchall()

	volume = entries[0][0]

	if Analysis.check_volume(volume) and Analysis.check_price(entries[0][1]):
		prices = [entry[1] for entry in entries]

		fluc = Trend.fluctuationFirstToRest(prices)
		action = Analysis.suggested_action(prices, fluc)

		if action != Analysis.Action.IGNORE:
			shortlist.append( (item, fluc, prices, [entry[0] for entry in entries], [entry[2] for entry in entries], action) )

shortlist.sort(key=absolute_value_of_nth_element_in_tuple_callable(1), reverse=True)

[print(f'{row[0]}:{row[-1]}:{row[1]}') for row in shortlist]

Analysis.plot_items(shortlist)

# print (Analysis.suggested_action(8,[4, 8, 6, 4, 2, 0]))