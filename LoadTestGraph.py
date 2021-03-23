import wx
import MyWidget


class Panel_LoadTestGraph(wx.Panel):
    def __init__(self, parent=None, id=-1, update_ui=None, data=None, showFlag=True):
        wx.Panel.__init__(self, parent, id)
        self.update_ui = update_ui
        self.data = data
        self.button_list = []
        self.timer = wx.Timer(self)
        self.img = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.UI_init()
        self.Bind(wx.EVT_LEFT_DOWN, self.Parent.pos_reset)
        self.Show(showFlag)

    def UI_init(self):
        MyWidget.Background(self, "Maximus Demo Interface - Background Only - Load Test-08.jpg")
        box = wx.BoxSizer(wx.VERTICAL)

        self.buttonStop = self.create_button("9.png",
                                             self,
                                             handler=self.test_stop)

        # Layout
        box.Add(self.buttonStop, 0, wx.TOP | wx.ALIGN_CENTER, 638)
        self.SetSizer(box)

    def activate(self):
        print("----------Load Test Interface-----------")
        self.timer_activate()

    def deactivate(self):
        pass

    def create_button(self, label, parent, handler):
        button = MyWidget.MyBitButton(label, parent, -1, handler=handler)
        self.button_list.append(button)
        return button

    def buttons_reset(self, event):
        for button in self.button_list:
            button.reset()

    def timer_activate(self):
        self.Bind(wx.EVT_TIMER, self.img_refresh, self.timer)
        self.timer.Start(500)

    def img_refresh(self, event):
        if self.data.on_time == 1:
            self.test_stop(None)
            return
        self.data.plot_measurement(1, 'save')
        pic = wx.Image("./TestGraph/temp_graph.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        if self.img:
            self.img.Destroy()
        self.img = wx.StaticBitmap(self, -1, pic)
        self.sizer.Add(self.img, 0, wx.ALIGN_CENTRE | wx.TOP, 250)
        self.SetSizer(self.sizer)
        self.Layout()

    def test_stop(self, event):
        self.timer.Stop()
        self.update_ui(7, False)


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(parent=None, id=-1, size=(1280, 800))
    panel = Panel_LoadTestGraph(frame)
    pic = wx.Image("./TestGraph/temp_graph.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    img = wx.StaticBitmap(panel, -1, pic)
    img.Centre()
    panel.Layout()
    frame.Show()
    app.MainLoop()
