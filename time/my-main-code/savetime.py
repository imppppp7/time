import cv2
import xlwt
import datetime
import PyHook3
import pythoncom


'''

write_data 每次调用都会返回系统的当前时间，并且存入excel中，调用一次返回一次时间
onmouseevent 存储鼠标事件供 hook调用 每次调用会将onmouseevent的信息存储进excel
hook1 用的是pythoncom.PumpMessages(),调用之后会一直返回想要的信息，但是要一直在循环中才可以，所以要单独运行这个程序

'''


class Savetime:

    def __init__(self,bookname,sheetname):
        self.bookname = bookname
        self.sheetname = sheetname
        self.number = 1
        # 新建工作簿
        self.workbook = xlwt.Workbook(encoding='utf-8')
        # 新建sheet
        self.sheet1 = self.workbook.add_sheet('%s'%self.sheetname)
        self.sheet1.write(0, 0, '次数')
        self.sheet1.write(0, 1, '日期')
        self.sheet1.write(0, 2, '时间')
        self.sheet1.write(0, 3, '分钟数')
        self.sheet1.write(0, 4, '秒数')
        self.sheet1.write(0, 5, 'messagename')
        # self.sheet1.write(0, 6, 'Windowname')
        self.sheet1.write(0, 7, 'Position')

    def write_time(self):
        print("系统当前时间", str(datetime.datetime.now()), self.number)
        _date, _time = str(datetime.datetime.now()).split(' ')
        a, b, c = _time.split(':')
        self.sheet1.write(self.number, 0, self.number)
        self.sheet1.write(self.number, 1, _date)
        self.sheet1.write(self.number, 2, _time)
        self.sheet1.write(self.number, 3, b)
        self.sheet1.write(self.number, 4, c)
        self.number = self.number + 1
        # k = cv2.waitKey(5000)
        # 保存
        self.workbook.save(r'C:\Users\Administrator\Desktop\%s.xls'%self.bookname)

    def hook(self):

        def onmouseevent(event):
            # 监听鼠标事件
            print("MessageName:", event.MessageName)
            print('系统当前时间', str(datetime.datetime.now()), self.number)
            print("WindowName:", event.WindowName)
            print("Position:", event.Position)
            print('---')
            _date, _time = str(datetime.datetime.now()).split(' ')
            a, b, c = _time.split(':')
            self.sheet1.write(self.number, 0, self.number)
            self.sheet1.write(self.number, 1, _date)
            self.sheet1.write(self.number, 2, _time)
            self.sheet1.write(self.number, 3, b)
            self.sheet1.write(self.number, 4, c)
            self.sheet1.write(self.number, 5, str(event.MessageName))
            # self.sheet1.write(self.number, 6, str(event.WindowName))
            self.sheet1.write(self.number, 7, str(event.Position))
            self.number = self.number + 1
            self.workbook.save(r'C:\Users\Administrator\Desktop\%s.xls' % self.bookname)
            # 返回 True 以便将事件传给其它处理程序
            # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
            # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
            return True

        #  设置钩子管理对象
        hm = PyHook3.HookManager()
        # 监听所有鼠标事件
        hm.MouseAll = onmouseevent
        # 设置鼠标钩子
        hm.HookMouse()
        # 无限循环一直存储信息
        pythoncom.PumpMessages()
