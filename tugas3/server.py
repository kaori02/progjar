import rpyc                                       # rpyc - library koneksi
from rpyc.utils.helpers import classpartial
from rpyc.utils.server import ThreadedServer
from sqlite3 import Connection, Cursor, connect
from beautifultable import BeautifulTable
import argparse

class Sqlite():
  def __init__(self, database: str):                        # inisiasi
    self.connection: Connection = connect(database)         
    self.cursor: Cursor = self.connection.cursor()          

  def run_query(self, query: str) -> list:                  # run query
    self.cursor.execute(query)

    return self.cursor.fetchall()

# sqlite
class SqliteService(rpyc.Service):
  def __init__(self, database: str):                        # inisiasi
    self.sqlite_service = Sqlite(database)

  def exposed_rawquery(self, query: str) -> list:           # exposed rawquery   
    return self.sqlite_service.run_query(query)

  def exposed_tabquery(self, query: str) -> str:            # exposed tabquery
    result = self.sqlite_service.run_query(query)

    table = BeautifulTable()                                # using BeautifulTable
    for row in result:                                      # append rows from db to table
      table.rows.append(row)

    # rows header (S + number)
    table.rows.header = ["S"+str(i) for i in range(1, len(result) + 1)]
    
    # colums header (deskripsi kolom)
    table.columns.header = [description[0] for description in self.sqlite_service.cursor.description]

    return table

  def exposed_quit(self) -> None:
    exit()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='TCP Server Program')
  parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                      help='TCP port (default 1060)')
  parser.add_argument('-d', metavar='DATABASE', type=str, default='data.db',
                      help='Database (default data.db)')

  args = parser.parse_args()
  print(f'Server running on port {args.p} using {args.d}')

  
  service = classpartial(SqliteService, args.d)
  server = ThreadedServer(service, port=args.p)
  
  server.start()
