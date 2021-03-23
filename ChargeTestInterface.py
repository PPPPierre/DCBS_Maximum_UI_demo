import wx
import MyWidget


class Panel_ChargeInterface(wx.Panel):
    def __init__(self, parent=None, id=-1, update_ui=None, data=None, showFlag=True):
        wx.Panel.__init__(self, parent, id)
        self.update_ui = update_ui
        self.data = data
        self.timer = wx.Timer(self)
        self.button_list= []
        self.UI_init()
        self.Bind(wx.EVT_LEFT_DOWN, self.Parent.pos_reset)
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)
        self.Show(showFlag)

    def UI_init(self):
        MyWidget.Background(self, "Maximus Demo Interface - Background Only-04.jpg")
        box = wx.BoxSizer(wx.VERTICAL)
        boxLive = wx.BoxSizer(wx.VERTICAL)
        # Widgets creation
        self.LVValue = MyWidget.MyDisplay(self,
                                          lContent="",
                                          vContent="0.000",
                                          seperate=10)
        self.LCValue = MyWidget.MyDisplay(self,
                                          lContent="",
                                          vContent="0.000",
                                          seperate=10)
        self.LTValue = MyWidget.MyTimeDisplay(self,
                                              lContent="",
                                              value=(0, 0),
                                              seperate=10)
        self.create_button("9.png", self, handler=self.test_stop)

        # Layout
        boxLive.AddMany([(self.LVValue, 0, wx.ALIGN_CENTRE | wx.TOP, 331),
                         (self.LCValue, 0, wx.ALIGN_CENTRE | wx.TOP, 76),
                         (self.LTValue, 0, wx.ALIGN_CENTRE | wx.TOP, 76,)])
        box.AddMany([(boxLive, 0, wx.RIGHT | wx.ALIGN_RIGHT, 338),
                     (self.button_list[0], 0, wx.TOP | wx.ALIGN_CENTER, 69)])
        self.SetSizer(box)

    def activate(self):
        print("----------Charge Test Interface-----------")
        self.test_start()

    def deactivate(self):
        pass

    def create_button(self, label, parent, handler):
        button = MyWidget.MyBitButton(label, parent, -1, handler=handler)
        self.button_list.append(button)
        return button

    def buttons_reset(self, event):
        for button in self.button_list:
            button.reset()

    def test_start(self):
        self.data.init_measure_data()
        self.data.charge_start()
        self.timer_activate()

    def timer_activate(self):
        self.Bind(wx.EVT_TIMER, self.data_refresh)
        self.timer.Start(500)

    def data_refresh(self, event):
        if self. data.is_charge_finished() == 1 | self.data.on_time == 1:
            self.test_stop()
            self.data.charge_End = 1
            return
        self.data.refresh_data(i_on=True)
        time_min = int(self.data.liveTime // 60)
        time_second = int((self.data.liveTime % 60) // 1)
        self.LVValue.set_value(str(self.data.voltage12))
        self.LCValue.set_value(str(self.data.current))
        self.LTValue.set_time((time_min, time_second))
        self.Layout()

    def test_stop(self):
        self.timer.Stop()
        self.data.charge_stop()
        self.update_ui(4)

    def back_to_settings(self):
        self.update_ui(2)


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(parent=None, id=-1, size=(1280, 800))
    Panel_ChargeInterface(frame)
    frame.Show()
    app.MainLoop()
