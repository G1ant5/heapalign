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
    def align64(self,size,hexadecimal=False,verbose=False):
        aligned = 0
        while  aligned ==0:
            tmp = size % 0x10
            if tmp !=0:
                size = size + tmp
                if verbose == True:
                    print 'size :{}'.format(size)
                    self.align64(size,True)
                else :
                    self.align64(size,False)    
            else:
                aligned = 1
        if hexadecimal :
            return hex(size)
        else:
            return size
    def align32(self,size,hexadecimal=False,verbose=False):
        aligned = 0
        while  aligned ==0:
            tmp = size % 0x8
            if tmp !=0:
                size = size + tmp
                if verbose == True:
                    print 'size :{}'.format(size)
                    self.align32(size,True)
                else :
                    self.align32(size,False)    
            else:
                aligned = 1
        if hexadecimal :
            return hex(size)
        else:
            return size
