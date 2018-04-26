# -*- coding:utf-8 -*-
from cmd import Cmd
import os



class Client(Cmd):
    u"""help
    这是doc
    """
    prompt = 'pyFun>'
    intro = 'Welcom to pyFun!'

    def __init(self):
        # reload(sys)
        # sys.setdefaultencoding('utf-8')
        Cmd.__init__(self)

    def do_hello(self,arg):
        print('hello',arg)

    def do_exit(self,arg):
        print('Bye!')
        return True #返回True，直接输入exit命令将会退出

    def preloop(self):
        print("print this line before entering the loop")

    def postloop(self):
        # print 'Bye!'
        print("print this line after leaving the loop")

    def precmd(self, line):
        print("print this line before do a command")
        return Cmd.precmd(self, line)

    def postcmd(self, stop, line):
        print("print this line after do a command")
        return Cmd.postcmd(self, stop, line)   

if __name__ == '__main__':
    try:
        os.system('cls')
        client = Client()
        client.cmdloop()
    except:
        exit()