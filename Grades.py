import SocketServer
import gspread
import json

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # print "{} wrote:".format(self.client_address[0])

        data = json.loads(self.data)
        req = data.split()
        name = req[0]
        item = req[1]
        #print name
        #print item

        gspread_client = gspread.login('niwandou5@gmail.com','sherlock123')
        worksheet = gspread_client.open("Grades").sheet1
        name_cell = worksheet.find(name)
        item_cell = worksheet.find(item)
        score_cell = worksheet.cell(name_cell.row, item_cell.col)
        score = score_cell.value

        #print 'Corresponding cell is (%d, %d)' %(cell.row, cell.col)

        #print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(score)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    # only deal with packets from localhost
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()