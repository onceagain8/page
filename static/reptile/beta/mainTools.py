import constant as con
import GrabPages
import GrabError
from verb import js_table
class mainTool:
    def find(**args) :
        f'''
            find with pram id or {','.join(con.page_contains)}
        '''
        if 'index' in args:
            if args['index'] in js_table:
                raise Exception('index Error,Not found')
            return {args['index']:js_table[args['index']]}
        for it in args:
            if it not in con.page_contains:
                raise Exception(f'Error, illegal parameter name with {it} ')
        ret = {}
        for index in js_table:
            if all([(args[name] in js_table[index][name]) for name in args]):
                ret[index]=js_table[index]
        if len(ret) == 0:
            raise Exception('Not Found')
        return ret
    
    def pa(**args):
        for it in args:
            if it not in con.page_contains:
                raise Exception(f'Error, illegal parameter name with {it}')
        if 'l' in args:
            l=int(args['l'])
        else :
            l=None
        if 'r' in args:
            r=int(args['r'])
        else:
            r=None
        try:
            GrabPages.grab(url,l=l,r=r)
        except Exception as e:
            GrabError.write_error(con.local_Dir,e)
        return ''

tools={'find':mainTool.find,'pa':mainTool.pa}

def run(ss):
    s=ss.split(' ')
    if s[0] == 'show':
        print(js_table)
        return 
    if s[0] not in tools:
        return 'Error,tool not found'
    args={}
    for it in s[1:]:
        a,b=it.split('=')
        args[a]=b
    try:
        ans=tools[s[0]](**args)
        return str(ans)
    except Exception as e:
        return str(e)