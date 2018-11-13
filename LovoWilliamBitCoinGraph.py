import matplotlib

matplotlib.use('Agg')

import networkx as nx

import pygeoip

bitcoin_graph = None


def create_undirected_graph(graph_file_path):
  global bitcoin_graph
  bitcoin_graph = nx.read_graphml(graph_file_path).to_undirected()


def find_country(ip_address):
  geo_ip = pygeoip.GeoIP("./GeoIP.dat", pygeoip.MEMORY_CACHE)  # Change to the proper path/filename as needed.

  country = geo_ip.country_name_by_addr(ip_address)
  return country


def main():
  # Based on the dataset
  bitcoin_data_path = './bitcoingraph.graphml'  # Change to the proper path/filename as needed.

  create_undirected_graph(bitcoin_data_path)

  # Question 1
  num_of_nodes = len(bitcoin_graph.nodes())
  print "Question 1:\nThere are " + str(num_of_nodes) + " nodes in the graph.\n"

  # Question 2
  num_of_edges = len(bitcoin_graph.edges())
  print "Question 2:\nThere are " + str(num_of_edges) + " edges in the graph.\n"

  # Question 3-6 set up
  nodes = bitcoin_graph.nodes()
  degree_dict = {node: bitcoin_graph.degree(node) for node in nodes}

  sorted_node_list = sorted(degree_dict.items(), key=lambda (key, value): value, reverse=True)

  # Question 3
  largest_node_value = sorted_node_list[0][1]
  print "Question 3:\nThe largest node degree is " + str(largest_node_value)
  print "\nThe IP address(es) with this degree is: "
  for node in sorted_node_list:
    if node[1] == largest_node_value:
      print node[0]
  print "\n"

  # Question 4
  smallest_node_value = sorted_node_list[-1][1]
  print "Question 4:\nThe smallest node degree is " + str(smallest_node_value)
  print "\nThe IP address(es) with this degree is: "
  for node in sorted_node_list:
    if node[1] == smallest_node_value:
      print node[0]
  print "\n"

  # Question 5
  print "Question 5: The top 10 nodes are as follows:"
  for node in sorted_node_list[:10]:
    country = "Unknown" if str(find_country(node[0])) is '' else str(find_country(node[0]))
    print str(node[0]) + " with degree " + str(node[1]) + " in the country of " + country

  # Question 6
  print "\nQuestion 6: The top 5 countries are as follows:"
  list_of_countries = {}

  for node in nodes:
    country = "Unknown" if str(find_country(node)) is '' else str(find_country(node))
    if country in list_of_countries:
      list_of_countries[country] = list_of_countries[country] + 1
    else:
      list_of_countries[country] = 1

  for country in sorted(list_of_countries.items(), key=lambda (key, value): (value, key), reverse=True)[:5]:
    print str(country[0]) + " with " + str(country[1]) + " nodes"


if __name__ == '__main__':
  main()
