import os
import wx
import MyWidget


class Panel_MainMenu(wx.Panel):
    def __init__(self, parent=None, id=-1, update_UI=None, data=None, showFlag=True):
        wx.Panel.__init__(self, parent, id)
        self.update_UI = update_UI
        self.data = data
        self.button_list = []
        self.UI_init()
        self.Bind(wx.EVT_MOUSE_EVENTS, self.Parent.pos_reset)
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)
        self.Show(showFlag)

    def UI_init(self):
        MyWidget.Background(self, "Maximus Demo Interface - Background Only-02.jpg")

        ButtonCharge = self.create_button("1.png",
                                          self,
                                          handler=self.enter_charge_test)
        ButtonCCA = self.create_button("3.png",
                                       self,
                                       handler=self.enter_CCA_test)
        ButtonLoad = self.create_button("4.png",
                                        self,
                                        handler=self.enter_Load_test)
        ButtonRC = self.create_button("2.png",
                                      self,
                                      handler=self.enter_RC_test)
        ButtonOnOff = self.create_button("7.png",
                                         self,
                                         handler=self.event_ButtonOnOff)
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=0, vgap=72)
        self.sizer.AddMany([(ButtonCharge, 0, wx.ALIGN_RIGHT | wx.RIGHT, 56),
                            (ButtonCCA, 0, wx.ALIGN_LEFT | wx.LEFT, 56),
                            (ButtonRC, 0, wx.ALIGN_RIGHT | wx.RIGHT, 145),
                            (ButtonLoad, 0, wx.ALIGN_LEFT | wx.LEFT, 147)])
        self.box.AddMany([(self.sizer, 0, wx.TOP | wx.ALIGN_CENTER, 284),
                          (ButtonOnOff, 0, wx.TOP | wx.ALIGN_CENTRE, 20)])
        self.SetSizer(self.box)

    def activate(self):
        print("----------Main Menu-----------")
        self.batt_check()

    def deactivate(self):
        pass

    def create_button(self, label, parent, handler):
        button = MyWidget.MyBitButton(label, parent, -1, handler=handler)
        self.button_list.append(button)
        return button

    def buttons_reset(self, event):
        for button in self.button_list:
            button.reset()

    def enter_charge_test(self):
        self.update_UI(2)

    def enter_CCA_test(self):
        self.update_UI(5)

    def enter_Load_test(self):
        self.update_UI(6)

    def enter_RC_test(self):
        self.update_UI(10)

    def event_ButtonOnOff(self):
        MyWidget.MyYNDialog(self, "Are you sure you want to close DCBS?", yes_handler=self.quit_DCBS)

    def quit_DCBS(self):
        print("Quit DCBS Maximum Demo Interface!")
        # self.Parent.Close(True)
        os.system("sudo init 0")

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
    Panel_MainMenu(frame)
    frame.Show()
    app.MainLoop()
