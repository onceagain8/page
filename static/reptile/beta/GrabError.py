import os
import time
import traceback
def write_error(local_Dir,e): 
    print(traceback.format_exc())
    with open(os.path.join(local_Dir,'error','log.txt'),'a+') as cerr:
        cerr.write('='*50+'\n')
        cerr.write('Error at'+time.asctime(time.localtime(time.time()))+'\n')
        cerr.write(traceback.format_exc())
        cerr.write('\n\n')