from multiprocessing import Process
from time import sleep


def sayHi(processName, sleepTime):
    while True:
        print(f"{__name__} - {processName}: hi")
        sleep(sleepTime)

if __name__ == "__main__":
    print("\nCode has been Initialized.\n")
    
    # The comma in "args=("Joel",)" is needed to the code understands it is a tuple, not 4 arguments
    joel = Process(target=sayHi, args=("= Joel", 1))
    ellie = Process(target=sayHi, args=("====Ellie ", 4))
    bob = Process(target=sayHi, args=("========Bob", 8))
    
    joel.start()
    ellie.start()
    #bob.start();
    
    # ---
    
    """ 
    # TESTE 01
    sleep(5)
    joel.terminate()
    
    sleep(5)
    ellie.terminate()
    
    sleep(5)
    bob.terminate()
    """
    
    # TESTE 02
    sleep(60)
    joel.terminate()
    ellie.terminate()
    #bob.terminate()
    
    print("\nCode has been Finished.\n")
