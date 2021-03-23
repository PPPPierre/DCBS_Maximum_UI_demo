import wx
import MyWidget


class Panel_RCTestInterface(wx.Panel):
    def __init__(self, parent=None, id=-1, update_ui=None, data=None, showFlag=True):
        wx.Panel.__init__(self, parent, id)
        self.update_ui=update_ui
        self.data = data
        self.button_list = []
        self.timer = wx.Timer(self)
        self.UI_init()
        self.Bind(wx.EVT_LEFT_DOWN, self.Parent.pos_reset)
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)
        self.Show(showFlag)

    def UI_init(self):
        MyWidget.Background(self, "Maximus Demo Interface - Background Only - RC Test-11.jpg")
        box = wx.BoxSizer(wx.VERTICAL)
        boxLive = wx.BoxSizer(wx.VERTICAL)

        # Widgets creation
        self.Voltage = MyWidget.MyDisplay(self,
                                          lContent="",
                                          vContent="0.000",
                                          seperate=10,
                                          fontSize=20)
        self.Capacity= MyWidget.MyDisplay(self,
                                          lContent="",
                                          vContent="0.000",
                                          seperate=10,
                                          fontSize=20)
        self.Time = MyWidget.MyTimeDisplay(self,
                                           lContent="",
                                           value=(0, 0),
                                           seperate=10,
                                           fontSize=20)
        self.buttonStop = self.create_button("9.png",
                                             self,
                                             handler=self.test_stop)

        # Layout
        boxLive.AddMany([(self.Voltage, 0, wx.ALIGN_CENTRE | wx.TOP, 330),
                         (self.Capacity, 0, wx.ALIGN_CENTRE | wx.TOP, 73),
                         (self.Time, 0, wx.ALIGN_CENTRE | wx.TOP, 73)])
        # box.Add(boxLive, 0, wx.RIGHT | wx.ALIGN_RIGHT, 334)
        box.AddMany([(boxLive, 0, wx.RIGHT | wx.ALIGN_RIGHT, 334),
                     (self.buttonStop, 0, wx.TOP | wx.ALIGN_CENTRE, 61)])
        self.SetSizer(box)

    def activate(self):
        print("----------RC Test Interface-----------")
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
        self.timer_activate(None)

    def timer_activate(self, event):
        self.Bind(wx.EVT_TIMER, self.data_refresh, self.timer)
        self.timer.Start(500)

    def data_refresh(self, event):
        if self.data.on_time == 1:
            self.test_stop()
            return
        self.data.refresh_data(c_on=True)
        time_min = int(self.data.liveTime // 60)
        time_second = int(self.data.liveTime % 60 // 1)
        self.Voltage.set_value(str(self.data.voltage12))
        self.Capacity.set_value(str(self.data.capacity))
        self.Time.set_time((time_min, time_second))
        self.Layout()

    def test_stop(self):
        self.timer.Stop()
        self.data.RC_test_stop()
        self.update_ui(12)

    def mode_switch(self, event):
        self.update_ui(9)

    def back_to_settings(self, event):
        self.update_ui(6)


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(parent=None, id=-1, size=(1280, 800))
    Panel_RCTestInterface(frame)
    frame.Show()
    app.MainLoop()
