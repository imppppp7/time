import pythoncom
import PyHook3
import datetime
# from savetime import Savetime


def onMouseEvent(event):
    # 监听鼠标事件
    print("MessageName:", event.MessageName)
    print(str(datetime.datetime.now()))
    # print("Message:", event.Message)
    # print("Time:", event.Time)
    print("Window:", event.Window)
    print("WindowName:", event.WindowName)
    print("Position:", event.Position)
    # print("Wheel:"), event.Wheelkkk9
    # print("Injected:"), event.Injected
    print('---')

    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True


# 创建一个“钩子”管理对象
hm = PyHook3.HookManager()
# 监听所有鼠标事件
hm.MouseAll = onMouseEvent
# 设置鼠标“钩子”
hm.HookMouse()
# 进入循环，如不手动关闭，程序将一直处于监听状态

pythoncom.PumpMessages()

