# observer pattern base classes, si suffix calculator, utility functions
#
#(C) 2004 Chris Liechti <cliechti@gmx.net>
# this is distributed under a free software license, see license.txt

import sys, traceback

#observer pattern
class Observer:
    def __init__(self):
        pass
    def update(self, theChangedSubject):
        pass

class Subject:
    def __init__(self):
        self.observerList = []
    def attach(self, observer):
        self.observerList.append(observer)
    def detach(self, observer):
        try:
            self.observerList.remove(observer)
        except ValueError: #ignore if x not in list
            pass
    def notify(self, *args):
        for observer in self.observerList:
            try:
                observer.update(self, *args)
            except Exception, msg:
                sys.stderr.write("Subject.notify() exception in update() for %r:\n" % observer)
                traceback.print_exc()

unitprefixes = ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
def bytes2string(num):
    """give a nice formated byte count"""
    prefix = 0
    while num >= 1024*1024:
        prefix += 1
        num /= 1024
    num = float(num)
    if num >= 1024:
        prefix += 1
        num /= 1024
    if prefix > 0:
        try:
            str_p = unitprefixes[prefix]
        except IndexError:
            str_p = "* 2**%d" % (prefix*10)
        return "%.2f %sB" % (num, str_p)
    else:
        return "%d B" % (num)

def limit(min, max, value):
    """limit value to the given range"""
    if value < min:
        return min
    if value > max:
        return max
    return value

if __name__ == '__main__':
    import sys, unittest
    
    class Test(unittest.TestCase):
        def test_limit(self):
            self.failUnlessEqual(limit(0, 10, 7), 7)
            self.failUnlessEqual(limit(0, 7, 7), 7)
            self.failUnlessEqual(limit(0, 6, 7), 6)
            self.failUnlessEqual(limit(7, 10, 7), 7)
            self.failUnlessEqual(limit(8, 10, 7), 8)
            
        def test_bytestext(self):
            self.failUnlessEqual(bytes2string(0), '0 B')
            self.failUnlessEqual(bytes2string(123), '123 B')
            self.failUnlessEqual(bytes2string(1024), '1.00 kB')
            self.failUnlessEqual(bytes2string(1024**2), '1.00 MB')
            self.failUnlessEqual(bytes2string(1024**8), '1.00 YB')

    sys.argv = sys.argv[0:1] + ['-v']
    unittest.main()
