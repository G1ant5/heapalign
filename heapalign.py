#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
size：本堆块的长度。长度计算方式：size字段长度+用户申请的长度+对齐。libc以size_T长度*2为粒度对齐。
例如32bit以4*2=8byte对齐，64bit以8*2=0×10对齐。因为最少以8字节对齐，所以size一定是8的倍数，故size字段的最后三位恒为0，libc用这三个bit做标志flag。
比较关键的是最后一个bit（pre_inuse），用于指示相邻的前一个堆块是alloc还是free。如果正在使用，则bit=1。
libc判断当前堆块是否处于free状态的方法就是判断下一个堆块的pre_inuse是否为1。这里也是double free和null byte offset等漏洞利用的关键。
'''
from sys import *
class heapalign:
    verbose = False
    log = ''
    def __init__(self):
        print 'Heap align tips:'.strip()
        print '''
        fast bin  : <= 128 (0x80)
        small bin :  > 128 (0x80) <= 512 (0x200)
        large bin :  > 512 (0x200)
        '''
    def align64(self,size,hexadecimal=False,verbose=False):
        aligned = 0
        log = ''
        while  aligned ==0:
            tmp = size % 0x10
            if tmp !=0:
                size = size + tmp
                if verbose == True:
                    log += 'aligning size :{}\n'.format(size)
                    self.align64(size,True)
                else :
                    self.align64(size,False)    
            else:
                aligned = 1
        if hexadecimal :
            return hex(size),log.strip()
        else:
            return size,log.strip()
    def align32(self,size,hexadecimal=False,verbose=False):
        aligned = 0
        log =''
        while  aligned ==0:
            tmp = size % 0x8
            if tmp !=0:
                size = size + tmp
                if verbose == True:
                    log += 'aligning size :{}\n'.format(size)
                    self.align32(size,True)
                else :
                    self.align32(size,False)    
            else:
                aligned = 1
        if hexadecimal :
            return hex(size),log.strip()
        else:
            return size,log.strip()

    def show(self,arch,size,hexadecimal=False,verbose=False):
        if arch == 'i386':
            if verbose == True:
                size,info = self.align32(size,hexadecimal=False,verbose=True)
                print info+'\n'
                if hexadecimal == True:
                    print '[*] chunk size: 0x%x'%(size)
                    print '[*]memory size: 0x%x'%(size-0x8)
                else:
                    print '[*] chunk size: %d'%(size)
                    print '[*]memory size: %d'%(size-0x8)
            elif verbose == False:
                size,info = self.align32(size,hexadecimal=False,verbose=False)
                if hexadecimal == True:
                    print '[*] chunk size: 0x%x'%(size)
                    print '[*]memory size: 0x%x'%(size-0x8)
                else:
                    print '[*] chunk size: %d'%(size)
                    print '[*]memory size: %d'%(size-0x8)

        elif arch == 'amd64':
            if verbose == True:
                size,info = self.align64(size,hexadecimal=False,verbose=True)
                print info+'\n'
                if hexadecimal == True:
                    print '[*] chunk size: 0x%x'%(size+0x10)
                    print '[*]memory size: 0x%x'%(size)
                else:
                    print '[*] chunk size: %d'%(size+0x10)
                    print '[*]memory size: %d'%(size)
            elif verbose == False:
                size,info = self.align64(size,hexadecimal=False,verbose=False)
                if hexadecimal == True:
                    print '[*] chunk size: 0x%x'%(size+0x10)
                    print '[*]memory size: 0x%x'%(size)
                else:
                    print '[*] chunk size: %d'%(size+0x10)
                    print '[*]memory size: %d'%(size)

align = heapalign()
try :
    align.show(argv[1],int(argv[2]),int(argv[3]),int(argv[4]))
except :
    print '''usage :python heapalign.py arch size hexadecimal verbose
       arch        : i386 or amd64
       size        : the size you need to align
       hexadecimal : 1 or 0 
       verbose     : 1 or 0 
       '''.strip()
    exit(0)
#finally :
#    align.show(argv[1],int(argv[2]))
#print align.show('i386',10,1,1)