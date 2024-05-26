from cassandra.cluster import Cluster
from src import constants


cluster = Cluster([constants.CASSANDRA_HOSTS], port=constants.CASSANDRA_PORT)
session = cluster.connect(constants.CASSANDRA_KEYSPACE)
