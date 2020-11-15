import rpyc
import os
import sys
import logging
import shutil

from rpyc.utils.server import ThreadedServer

DATA_DIR = "/tmp/fs/"
PORT = 8888
logging.basicConfig(level=logging.DEBUG)


class Minion(rpyc.Service):

    # def exposed_put(self, block_id, data, minions):
    #     logging.debug("put block: " + block_id)
    #     out_path = os.path.join(DATA_DIR, block_id)
    #     with open(out_path, 'w') as f:
    #         f.write(data)
    #     if len(minions) > 0:
    #         self.forward(block_id, data, minions)

    # def exposed_get(self, block_id):
    #     logging.debug("get block: " + block_id)
    #     block_addr = os.path.join(DATA_DIR, block_id)
    #     if not os.path.isfile(block_addr):
    #         logging.debug("block not found")
    #         return None
    #     with open(block_addr) as f:
    #         return f.read()

    # def forward(self, block_id, data, minions):
    #     logging.debug("forwarding block: " + block_id + str(minions))
    #     next_minion = minions[0]
    #     minions = minions[1:]
    #     host, port = next_minion

    #     rpyc.connect(host, port=port).root.put(block_id, data, minions)

    
    def exposed_showfiles(self):
        # for root, dirs, files in os.walk(DATA_DIR):
        #     for filename in files:
        #         print(filename)
        entries = os.listdir(DATA_DIR)
        return entries

    def exposed_copy(self,filename):
        # print("inside file server")
        file=filename[0:-4]+'(copy).txt'   
        with open(os.path.join(DATA_DIR, file), 'w') as fp: 
            pass
        source = DATA_DIR + "/" + filename
        dest = DATA_DIR + "/" + file
        shutil.copyfile(source, dest)        

    def exposed_show_content(self,filename):
        path = DATA_DIR + "/" + filename
        my_file = open(path, "r+")
        print("checking")
        return my_file

    def exposed_current_dir(self):
        return DATA_DIR

    def exposed_moveup(self):
        DATA_DIR=""

    def exposed_movedown(self):
        print(DATA_DIR)
        print(os.path.abspath(os.curdir))
        print(DATA_DIR)


if __name__ == "__main__":
    PORT = int(sys.argv[1])
    DATA_DIR = sys.argv[2]

    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

    logging.debug("starting file server")
    rpyc_logger = logging.getLogger('rpyc')
    rpyc_logger.setLevel(logging.WARN)
    t = ThreadedServer(Minion(), port=PORT,  logger=rpyc_logger, protocol_config={
    'allow_public_attrs': True,
    })
    t.start()
