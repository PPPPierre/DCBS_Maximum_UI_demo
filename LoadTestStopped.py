import wx
import MyWidget


class Panel_LoadTestStopped(wx.Panel):
    def __init__(self, parent=None, id=-1, update_ui=None, data=None, showFlag=True):
        wx.Panel.__init__(self, parent, id)
        self.update_ui = update_ui
        self.data = data
        self.button_list = []
        self.chart_generate()
        self.UI_init()
        self.Bind(wx.EVT_LEFT_DOWN, self.Parent.pos_reset)
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)
        self.Show(showFlag)

    def UI_init(self):
        MyWidget.Background(self, "Maximus Demo Interface - Background Only - Load Test-09.jpg")
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box2 = wx.BoxSizer(wx.VERTICAL)
        self.buttonChart = self.create_button("6.png",
                                              self,
                                              handler=self.get_chart)
        self.buttonSave = self.create_button("5.png",
                                             self,
                                             handler=self.save_data)
        self.buttonMain = self.create_button("10.png",
                                             self,
                                             handler=self.return_to_MM)

        # Layout
        box1.AddMany([(self.buttonChart, 0, wx.RIGHT, 100),
                      (self.buttonSave, 0, wx.LEFT, 100)])
        box2.AddMany([(box1, 0, wx.ALIGN_CENTRE | wx.TOP, 377),
                      (self.buttonMain, 0, wx.ALIGN_CENTRE | wx.TOP, 132)])
        self.SetSizer(box2)

    def chart_generate(self):
        title = self.get_test_title()
        self.data.plot_measurement(title=title, type='v', mode='save', path="./TestGraph/temp_graph.png")

    def activate(self):
        print("----------Load Stopped Page-----------")
        self.chart_generate()

    def deactivate(self):
        pass

    def create_button(self, label, parent, handler):
        button = MyWidget.MyBitButton(label, parent, -1, handler=handler)
        self.button_list.append(button)
        return button

    def buttons_reset(self, event):
        for button in self.button_list:
            button.reset()

    def get_chart(self):
        pic = wx.Image("./TestGraph/temp_graph.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.img = wx.StaticBitmap(self, -1, pic)
        self.img.Bind(wx.EVT_LEFT_DOWN, self.chart_close)
        self.buttonMain.Disable()
        self.buttonSave.Disable()
        self.buttonChart.Disable()

    def chart_close(self, event):
        self.img.Destroy()
        self.buttonMain.Enable()
        self.buttonSave.Enable()
        self.buttonChart.Enable()

    def save_data(self):
        MyWidget.MyDialog(self, "Data Saving...", -1, self.save_data_helper)

    def save_data_helper(self):
        path = self.data.save_data('v', self.get_test_title())
        if path != '0':
            title = self.get_test_title()
            file_path = path + '_figure.png'
            self.data.plot_measurement(title, 'v', mode='save', path=file_path)
            content = "Save success!"
        else:
            content = "Please insert USB-disk!"
        MyWidget.MyOKDialog(self, content)
        return True

    def return_to_MM(self):
        self.update_ui(1)

    def get_test_title(self):
        title = 'Load ' + \
                'CCA ' + str(self.data.CCA) + ' A ' + \
                'Time ' + str(self.data.Load_second) + ' s'
        return title


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(parent=None, id=-1, size=(1280, 800))
    Panel_LoadTestStopped(frame)
    frame.Show()
    app.MainLoop()
