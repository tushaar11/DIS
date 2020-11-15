import rpyc
import sys
import os
import logging


logging.basicConfig(level=logging.DEBUG)


# def get(master, file):
#     file_table = master.read(file)
#     if not file_table:
#         logging.info("file not found")
#         return

#     for block in file_table:
#         for host, port in block['block_addr']:
#             try:
#                 con = rpyc.connect(host, port=port).root
#                 data = con.get(block['block_id'])
#                 if data:
#                     sys.stdout.write(data)
#                     break
#             except Exception as e:
#                 continue
#         else:
#             logging.error("No blocks found. Possibly a corrupt file")


# def put(master, source, dest):
#     size = os.path.getsize(source)
#     blocks = master.write(dest, size)
#     with open(source) as f:
#         for block in blocks:
#             data = f.read(master.block_size)
#             block_id = block['block_id']
#             minions = block['block_addr']

#             minion = minions[0]
#             minions = minions[1:]
#             host, port = minion

#             con = rpyc.connect(host, port=port)
#             con.root.put(block_id, data, minions)

def current_dir(fs):
    print(fs.current_dir())

def moveup(fs):
    print(fs.moveup())

def movedown(fs):
    print("movedown")
    print(fs.movedown())

def show_content(fs,filename):
    myfile = fs.show_content(filename)
    print(myfile.read())

def show(fs):
    entries =fs.showfiles()

    for entry in entries:
        print(entry)

def copy(fs,filename):
    fs.copy(filename)
    print("file successfully copied")
    # with open(os.path.join(path, file), 'w') as fp: 
    # pass
    # shutil.copyfile(source, destintion)

def choose(master):
    fs_id = int(input())
    fs_info  = master.choose(fs_id)
    return fs_info

def main():
    con = rpyc.connect("localhost", port=2131)
    master = con.root
    print("client started")
    fs_info = choose(master)
    host = fs_info[0]
    port = fs_info[1]
    fs = rpyc.connect(host, port=port).root
    print(host)
    print(port)

    while True:
        choice = int(input())
        if(choice == 1):
            show(fs)
        elif(choice == 2):
            filename = input()
            print("calling func")
            copy(fs,filename)
        elif(choice == 3):
            filename = input()
            print("calling func")
            show_content(fs,filename)
        elif(choice == 4):
            current_dir(fs)
        elif(choice == 5):
            moveup(fs)
        elif(choice == 6):
            movedown(fs)
            


    # if args[0] == "get":
    #     get(master, args[1])
    # elif args[0] == "put":
    #     put(master, args[1], args[2])
    # else:
    #     logging.error("try 'put srcFile destFile OR get file'")


if __name__ == "__main__":
    main()
