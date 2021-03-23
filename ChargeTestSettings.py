import wx
import MyWidget


class Panel_ChargeSettings(wx.Panel):
    def __init__(self, parent=None, id=-1, update_ui=None, data=None, showFlag=True):
        wx.Panel.__init__(self, parent, id)
        self.update_ui = update_ui
        self.data = data
        self.button_list = []
        self.UI_init()
        self.Bind(wx.EVT_LEFT_DOWN, self.Parent.pos_reset)
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)
        self.Show(showFlag)

    def UI_init(self):
        MyWidget.Background(self, "Maximus Demo Interface - Background Only-03-New.jpg")
        self.inputBox = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.Vtext = MyWidget.MyInput(self, content="1 ~ 15.00", min=1, max=15, textL=170, fontSize=20, keep_digit=2)
        self.Ctext = MyWidget.MyInput(self, content="1 ~ 100.00", min=1, max=100, textL=170, fontSize=20, keep_digit=2)
        self.TtextMin = MyWidget.MyInput(self, content="1 ~ 120", min=1, max=120, textL=170, fontSize=20)
        self.Etext = MyWidget.MyInput(self, content="1 ~ 10", min=1, max=10, textL=170, fontSize=20, keep_digit=2, mode=1)
        self.buttonStart = self.create_button("12.png",
                                              self,
                                              handler=self.event_start)
        self.buttonBack = self.create_button("11.png",
                                             self,
                                             handler=self.back_to_menu)
        # Layout
        self.inputBox.AddMany([(self.Vtext, 0, wx.ALIGN_RIGHT | wx.TOP, 290),
                               (self.Ctext, 0, wx.ALIGN_RIGHT | wx.TOP, 40),
                               (self.TtextMin, 0, wx.ALIGN_RIGHT | wx.TOP, 39),
                               (self.Etext, 0, wx.ALIGN_RIGHT | wx.TOP, 39)])
        self.buttonSizer.AddMany([self.buttonBack,
                                  self.buttonStart])
        self.mainSizer.Add(self.inputBox, 0, wx.RIGHT | wx.ALIGN_RIGHT, 278)
        self.mainSizer.Add(self.buttonSizer, 0, wx.TOP | wx.ALIGN_CENTER, 51)
        self.SetSizer(self.mainSizer)

    def activate(self):
        print("----------Charge Test Settings-----------")
        self.batt_check()

    def deactivate(self):
        self.Vtext.reset()
        self.Ctext.reset()
        self.TtextMin.reset()
        self.Etext.reset()

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
            MyWidget.MyDialog(self, "Charge Test Starting...", 1)
            self.update_ui(3)
            return True
        return False

    def back_to_menu(self):
        self.update_ui(1)

    def send_input(self):
        if self.values_check():
            try:
                voltage = float(self.Vtext.get_value())
                maxCurrent = float(self.Ctext.get_value())
                min = int(self.TtextMin.get_value())
                endCurrent = float(self.Etext.get_value())
            except ValueError:
                MyWidget.MyOKDialog(self.Parent, "Please enter correct input form!")
                return False
            else:
                self.data.get_settings_from_charge_panel(voltage, maxCurrent, min, endCurrent)
                return self.data.set_charge_settings()
        else:
            MyWidget.MyOKDialog(self.Parent, "Please enter settings!")
            return False

    def values_check(self):
        return self.Vtext.value_OK & self.Ctext.value_OK & self.TtextMin.value_OK & self.Etext.value_OK

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
    Panel_ChargeSettings(frame)
    frame.Show()
    app.MainLoop()
