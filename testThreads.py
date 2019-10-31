import threading

# Global lock


def write_to_file(global_lock,file_contents):
    while global_lock.locked():
        continue
    global_lock.acquire()
    file_contents.append(threading.get_ident())
    global_lock.release()

# Create a 200 threads, invoke write_to_file() through each of them,
# and 
def threadsFuncion():
    threads = []
    file_contents = []
    global_lock = threading.Lock()
    for i in range(1, 500):
        t = threading.Thread(target=write_to_file,args=(global_lock,file_contents))
        threads.append(t)
        t.start()
    [thread.join() for thread in threads]
    return file_contents

threads=threadsFuncion()
with open("thread_writes", "a+") as file:
    file.write('\n'.join([str(content) for content in file_contents]))
    file.close()