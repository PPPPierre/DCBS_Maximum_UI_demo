import os
import wx
import MyWidget
import LoadingPage
import MainMenu
import ChargeTestSettings
import ChargeTestInterface
import ChargeTestStopped
import CCATest
import LoadTestSettings
import LoadTestInterface
import LoadTestStopped
import LoadTestGraph
import RCTestSettings
import RCTestInterface
import RCTestStopped
from ControlCentre import DataBase


class MyFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, position=(0, 0)):
        wx.Frame.__init__(self, parent, id, 'DCBS Maximum Demo Interface',
                          size=(1280, 800),
                          pos=position,
                          style=wx.SIMPLE_BORDER | wx.TRANSPARENT_WINDOW)
        self.panel = []
        self.current_Panel = 0
        self.data_init()
        self.UI_init()
        self.Bind(wx.EVT_LEFT_DOWN, self.pos_reset)

    def UI_init(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(0, 13):
            self.panel.append(self.create_panel(i, False))
        self.panel[0].Show()
        self.panel[0].activate()
        self.SetSizer(self.sizer)

    def data_init(self):
        self.data = DataBase()
        if self.data.is_port_on() == 1:
            print("Device DCBS found!")
            return True
        else:
            print("Can not find the device DCBS!")
            MyWidget.MyOKDialog(self, "Can not find the device DCBS!")
            self.Close(True)
            os.system("sudo init 0")
            return False

    def update_UI(self, type, change_function=True):
        if change_function:
            self.panel[self.current_Panel].deactivate()
        self.panel[self.current_Panel].Hide()
        self.current_Panel = type
        self.panel[type].Show()
        if change_function:
            self.panel[type].activate()
        self.Layout()

    def create_panel(self, type=-1, showFlag=True):
        panel = None
        if type == 0:
            panel = LoadingPage.Panel_LoadingPage(self, -1, self.update_UI, self.data, showFlag)
        elif type == 1:
            panel = MainMenu.Panel_MainMenu(self, -1, self.update_UI, self.data, showFlag)
        elif type == 2:
            panel = ChargeTestSettings.Panel_ChargeSettings(self, -1, self.update_UI, self.data, showFlag)
        elif type == 3:
            panel = ChargeTestInterface.Panel_ChargeInterface(self, -1, self.update_UI, self.data, showFlag)
        elif type == 4:
            panel = ChargeTestStopped.Panel_ChargeStopped(self, -1, self.update_UI, self.data, showFlag)
        elif type == 5:
            panel = CCATest.Panel_CCATest(self, -1, self.update_UI, self.data, showFlag)
        elif type == 6:
            panel = LoadTestSettings.Panel_LoadTestSettings(self, -1, self.update_UI, self.data, showFlag)
        elif type == 7:
            panel = LoadTestInterface.Panel_LoadTestInterface(self, -1, self.update_UI, self.data, showFlag)
        elif type == 8:
            panel = LoadTestStopped.Panel_LoadTestStopped(self, -1, self.update_UI, self.data, showFlag)
        elif type == 9:
            panel = LoadTestGraph.Panel_LoadTestGraph(self, -1, self.update_UI, self.data, showFlag)
        elif type == 10:
            panel = RCTestSettings.Panel_RCTestSettings(self, -1, self.update_UI, self.data, showFlag)
        elif type == 11:
            panel = RCTestInterface.Panel_RCTestInterface(self, -1, self.update_UI, self.data, showFlag)
        elif type == 12:
            panel = RCTestStopped.Panel_RCTestStopped(self, -1, self.update_UI, self.data, showFlag)
        if panel:
            self.sizer.Add(panel, 1, wx.EXPAND)
        return panel

    def pos_reset(self, event):
        if event.ButtonDown():
            if self.GetPosition()[1] > 10:
                self.SetPosition((0, 0))
        elif event.Dragging():
            pass
        elif event.ButtonUp():
            if self.GetPosition()[1] > 10:
                self.SetPosition((0, 0))
        self.Layout()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
