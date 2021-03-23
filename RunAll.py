#! /usr/bin/env python3

# This is the main app for the whole project
# Based on the mainloop of wx.App

import wx
from TopWindows import MyFrame


class App(wx.App):
    def __init__(self, redirect=True, filename=None):
        print("App __init__")
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        print("OnInit")  # 输出到stdout
        self.frame = MyFrame(parent=None, id=-1)  # 创建框架
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        print("OnExit")


def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
