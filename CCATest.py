import MyWidget
import wx


class Panel_CCATest(wx.Panel):
    def __init__(self, parent=None, id=-1, update_UI=None, data=None,showFlag=True):
        wx.Panel.__init__(self, parent, id)
        self.update_UI = update_UI
        self.data = data
        self.button_list = []
        self.UI_init()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.get_CCA_result)
        self.Bind(wx.EVT_LEFT_DOWN, self.Parent.pos_reset)
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)
        self.Show(showFlag)

    def UI_init(self):
        MyWidget.Background(self, "Maximus Demo Interface - Background Only - CCA Result-05.jpg")
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box2 = wx.BoxSizer(wx.VERTICAL)
        self.SOHValue = MyWidget.MyDisplay(self, lContent="", vContent="0.000", fontSize=20)
        self.create_button("10.png", self, handler=self.return_to_MM)
        box1.Add(self.SOHValue, 0, wx.ALIGN_RIGHT | wx.RIGHT, 302)
        box2.AddMany([(box1, 0, wx.ALIGN_RIGHT | wx.TOP, 428),
                      (self.button_list[0], 0, wx.ALIGN_CENTRE | wx.TOP, 179)])
        self.SetSizer(box2)

    def activate(self):
        print("----------CCA Test Interface-----------")
        self.batt_check()
        if not self.data.is_on_CCA():
            self.test_start()
        self.timer.Start(500)

    def deactivate(self):
        pass

    def create_button(self, label, parent, handler):
        button = MyWidget.MyBitButton(label, parent, -1, handler=handler)
        self.button_list.append(button)

    def buttons_reset(self, event):
        for button in self.button_list:
            button.reset()

    def test_start(self):
        self.data.start_CCA_test()

    def get_CCA_result(self, event):
        flag = self.data.get_CCA_result()
        if flag == 2:
            self.SOHValue.set_value("Testing...")
        elif flag == 1:
            self.SOHValue.set_value(str(self.data.Rinterne))
            self.timer.Stop()
        elif flag == 0:
            self.SOHValue.set_value("Test stopped.")
            self.timer.Stop()
        elif flag == -1:
            self.SOHValue.set_value("Error!")
            self.timer.Stop()

    def test_stop(self):
        self.timer.Stop()

    def return_to_MM(self):
        self.test_stop()
        self.update_UI(1)

    def err_connection(self):
        MyWidget.MyOKDialog(self.Parent, "Connection error!")

    def batt_check(self):
        self.data.check_status()
        if self.data.is_batt_connected():
            return True
        MyWidget.MyDialog(self.Parent, 'Please connect the battery!', timer_handler=self.handler_batt_on)
        return False

    def handler_batt_on(self):
        self.data.check_status()
        if self.data.is_batt_connected():
            return True
        return False


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(parent=None, id=-1, size=(1280, 800))
    Panel_CCATest(frame)
    frame.Show()
    app.MainLoop()
