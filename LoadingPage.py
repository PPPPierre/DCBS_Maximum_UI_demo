import os
import wx
import MyWidget

sleep_time = 2


class Panel_LoadingPage(wx.Panel):
    def __init__(self, parent=None, id=-1, update_ui=None, data=None, showFlag=True):
        wx.Panel.__init__(self, parent, id)

        self.update_ui = update_ui
        self.data = data
        self.UI_init()
        self.Bind(wx.EVT_LEFT_DOWN, self.Parent.pos_reset)
        self.Show(showFlag)

    def UI_init(self):
        MyWidget.Background(self, "Maximus Demo Interface - Background Only-01.jpg")

    def activate(self):
        print("----------Loading Page-----------")
        self.timer_activate()

    def deactivate(self):
        self.timer.Stop()

    def timer_activate(self):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.status_check)
        self.timer.Start(sleep_time*1000)

    def status_check(self, event):
        err = 'Loading Error!\n'
        if self.data.check_status():
            if self.data.init_settings():
                self.update_ui(1)
                return True
        else:
            for str in self.data.err_list:
                err += str + "\n"
        MyWidget.MyOKDialog(self, err, OK_handler=self.err_Event())
        self.Parent.Destroy()
        os.system("sudo init 0")

    def err_Event(self):
        pass


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(parent=None, id=-1, size=(1280, 800))
    Panel_LoadingPage(frame)
    frame.Show()
    app.MainLoop()
