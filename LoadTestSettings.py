import wx
import MyWidget


class Panel_LoadTestSettings(wx.Panel):
    def __init__(self, parent=None, id=-1, update_ui=None, data=None, showFlag=True):
        wx.Panel.__init__(self, parent, id)
        self.update_ui = update_ui
        self.data = data
        self.button_list = []
        self.UI_init()
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)
        self.Bind(wx.EVT_LEFT_DOWN, self.Parent.pos_reset)
        self.Show(showFlag)

    def UI_init(self):
        MyWidget.Background(self, "Maximus Demo Interface - Background Only - Load Test 07.jpg")
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.CCAtext = MyWidget.MyInput(self, content="50 ~ 750", min=50, max=750, textL=170, fontSize=20)
        self.TimeText = MyWidget.MyInput(self, content="5 ~ 15", min=5, max=15, textL=170, fontSize=20)
        self.buttonStart = self.create_button("12.png",
                                              self,
                                              handler=self.event_start)
        self.buttonBack = self.create_button("11.png",
                                             self,
                                             handler=self.back_to_menu)
        # Layout
        self.sizer.AddMany([(self.CCAtext, 0, wx.ALIGN_RIGHT | wx.TOP, 361),
                            (self.TimeText, 0, wx.ALIGN_RIGHT | wx.TOP, 88)])
        self.buttonSizer.AddMany([self.buttonBack,
                                  self.buttonStart])
        self.box.AddMany([(self.sizer, 0, wx.RIGHT | wx.ALIGN_RIGHT, 280),
                          (self.buttonSizer, 0, wx.TOP | wx.ALIGN_CENTER, 110)])
        self.SetSizer(self.box)

    def activate(self):
        print("----------Load Test Settings-----------")
        self.batt_check()

    def deactivate(self):
        self.CCAtext.reset()
        self.TimeText.reset()

    def create_button(self, label, parent, handler):
        button = MyWidget.MyBitButton(label, parent, -1, handler=handler)
        self.button_list.append(button)
        return button

    def buttons_reset(self, event):
        for button in self.button_list:
            button.reset()

    def event_start(self):
        if self.is_CCA_test_on():
            MyWidget.MyOKDialog(self.Parent, 'CCA testing, please wait.')
            return False
        if self.send_input():
            self.data.load_test_start()
            MyWidget.MyDialog(self, "Load Test Starting...", 5)
            self.update_ui(7)
            return True
        return False

    def back_to_menu(self):
        self.update_ui(1)

    def send_input(self):
        if self.values_check():
            CCA = int(self.CCAtext.get_value())
            second = int(self.TimeText.get_value())
            self.data.get_settings_from_load_test_panel(CCA, second)
            return self.data.set_load_test_settings()
        else:
            MyWidget.MyOKDialog(self.Parent, "Please enter settings!")
            return False

    def values_check(self):
        return self.CCAtext.value_OK & self.TimeText.value_OK

    def is_CCA_test_on(self):
        self.data.get_CCA_result()
        if self.data.is_on_CCA():
            return True
        return False

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
    Panel_LoadTestSettings(frame)
    frame.Show()
    app.MainLoop()
