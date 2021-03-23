import wx
import wx.lib.buttons as wxButton
from decimal import Decimal
import Inputer

path_background = './Backgrounds/'
path_button_unused = './Buttons/Unused/'
path_button_used = './Buttons/Used/'


class MyButton(wxButton.GenButton):
    def __init__(self, parent=None, id=-1, label="", handler=None, fonsize=13,
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,):
        wxButton.GenButton.__init__(self, parent, id, label, pos, size,
                                    style=wx.BORDER_MASK)
        font = wx.Font(fonsize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Candara')
        self.SetFont(font)
        self.SetBackgroundColour('#0a74f7')
        self.SetForegroundColour('White')
        parent.Bind(wx.EVT_BUTTON, handler, self)


class MyBitButton(wx.StaticBitmap):
    def __init__(self, image_file, parent=None, id=-1,
                 pos=wx.DefaultPosition, handler=None):
        self.handler = handler
        self.pic_unused = wx.Image(path_button_unused + image_file, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.pic_used = wx.Image(path_button_used + image_file, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        wx.StaticBitmap.__init__(self, parent, id, self.pic_unused, pos=pos,
                                 style=wx.BORDER_NONE)
        self.Bind(wx.EVT_LEFT_UP, self.event_up)
        self.Bind(wx.EVT_LEFT_DOWN, self.event_down)

    def event_up(self, event):
        self.reset()
        self.handler()

    def event_down(self, event):
        self.SetBitmap(self.pic_used)

    def Disable(self):
        self.Unbind(wx.EVT_LEFT_UP)
        self.Unbind(wx.EVT_LEFT_DOWN)

    def Enable(self, enable=True):
        self.Bind(wx.EVT_LEFT_UP, self.event_up)
        self.Bind(wx.EVT_LEFT_DOWN, self.event_down)

    def reset(self):
        self.SetBitmap(self.pic_unused)


class MyTitle(wx.StaticText):
    def __init__(self, parent=None, label="", size=wx.DefaultSize, wordSize=10):
        wx.StaticText.__init__(self, parent, -1, label, size=size)
        font = wx.Font(wordSize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Candara')
        self.SetFont(font)


class MyDisplay(wx.BoxSizer):
    def __init__(self, parent=None, lContent="", vContent="", fontSize=18, seperate=10):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        font = wx.Font(fontSize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Candara')
        self.label = wx.StaticText(parent, -1, lContent, style=wx.TE_CENTER)
        self.value = wx.StaticText(parent, -1, vContent, size=(120, -1), style=wx.TE_CENTER)
        self.label.SetFont(font=font)
        self.value.SetFont(font=font)
        self.AddMany([(self.label, 0, wx.ALIGN_RIGHT | wx.Right, seperate/2),
                      (self.value, 0, wx.ALIGN_LEFT | wx.LEFT, seperate/2)])

    def set_value(self, content):
        self.value.SetLabel(content)


class MyTimeDisplay(wx.BoxSizer):
    def __init__(self, parent=None, lContent="", value=(0, 0), seperate=10, fontSize=18):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.min = value[0]
        self.second = value[1]
        font = wx.Font(fontSize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Candara')
        self.label = wx.StaticText(parent, -1, lContent, style=wx.TE_CENTER)
        self.value = wx.StaticText(parent, -1, str(self.min) + ":" + str(self.second),
                                   size=(120, -1), style=wx.TE_CENTER)
        self.label.SetFont(font=font)
        self.value.SetFont(font=font)
        self.AddMany([(self.label, 0, wx.ALIGN_RIGHT | wx.RIGHT, seperate / 2),
                      (self.value, 0, wx.ALIGN_LEFT | wx.LEFT, seperate / 2)])

    def set_time(self, time):
        self.min = time[0]
        self.second = time[1]
        self.value.SetLabel(str(self.min) + ":" + str(self.second))


class MyInput(wx.TextCtrl):
    def __init__(self, parent=None, content="", min=0, max=0, textL=100, fontSize=10, keep_digit=0, mode=0):
        wx.TextCtrl.__init__(self, parent, -1, content, size=(textL, 50), style= wx.TE_CENTER | wx.TE_READONLY)
        font = wx.Font(fontSize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Candara')
        self.SetFont(font)
        self.content = content
        self.value_raw = 0
        self.min = min
        self.max = max
        self.value_OK = False
        self.digit = "0."
        self.mode = mode
        for i in range(0, keep_digit):
            self.digit += '0'
        self.inputer = None
        self.Bind(wx.EVT_LEFT_UP, self.call_inputer)
        self.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)

    def reset(self):
        self.SetValue(self.content)
        self.value_OK = False

    def call_inputer(self, event):
        self.SetValue("")
        self.inputer = Inputer.MyInputer(self, -1, self.get_value())
        self.inputer.ShowModal()

    def onKillFocus(self, event):
        value = self.get_value()
        if value == "":
            self.reset()
        event.Skip()

    def value_set(self):
        try:
            value = Decimal(float(self.value_raw)).quantize(Decimal(self.digit))
        except ValueError:
            self.reset()
            MyOKDialog(self.Parent, "Please enter a number!")
            self.value_OK = False
            return False
        else:
            self.SetValue(str(value))
            self.value_OK = True
            return True

    def range_check(self):
        try:
            value = float(self.value_raw)
        except ValueError:
            return False
        else:
            if (not self.max == 0) & (value > self.max):
                return False
            elif value < self.min:
                return False
            return True

    def is_lack_input(self):
        if self.get_value() == self.content:
            return True
        else:
            return False

    def get_value(self):
        return self.GetValue()


class MyReadOnlyInput(wx.TextCtrl):
    def __init__(self, parent=None, content="", textL=100, height=50, fontSize=10):
        wx.TextCtrl.__init__(self, parent, -1, content,
                             size=(textL, height),
                             style=wx.TE_READONLY|
                                   wx.TE_CENTER |
                                   wx.TE_PROCESS_ENTER)
        font = wx.Font(fontSize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Candara')
        self.content = content
        self.SetFont(font)
        self.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)

    def reset(self):
        self.SetValue(self.content)

    def onKillFocus(self, event):
        self.reset()
        event.Skip()

    def get_value(self):
        return self.GetValue()


class Background:
    def __init__(self, panel, image_file):
        self.path = path_background + image_file
        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Image(self.path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        dc.DrawBitmap(bmp, 0, 0)


class MyYNDialog(wx.Dialog):
    def __init__(self, parent=None, content="", yes_handler=None, no_handler=None):
        wx.Dialog.__init__(self, parent, size=(540, 300), style=wx.SIMPLE_BORDER | wx.TRANSPARENT_WINDOW)
        self.Bind(wx.EVT_LEFT_DOWN, null_handler)
        self.yes_handler = yes_handler
        self.no_handler = no_handler
        self.SetBackgroundColour('#2F2F2F')
        warning = wx.StaticText(self, -1, content)
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Candara')
        warning.SetForegroundColour('White')
        warning.SetFont(font)
        self.button_yes = MyBitButton("Yes.png",
                                      self, -1,
                                      handler=self.yes_event)
        self.button_no = MyBitButton("No.png",
                                     self, -1,
                                     handler=self.no_event)
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.BoxSizer(wx.VERTICAL)
        sizer_button.AddMany([(self.button_yes, 0, wx.ALIGN_LEFT | wx.Right, 100),
                              (self.button_no, 0, wx.ALIGN_RIGHT | wx.LEFT, 100)])
        box.AddMany([(warning, 0, wx.ALIGN_CENTER | wx.TOP, 80),
                     (sizer_button, 0, wx.ALIGN_CENTRE | wx.TOP, 80)])
        self.SetSizer(box)
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)
        self.ShowModal()

    def yes_event(self):
        if self.yes_handler:
            self.yes_handler()
        self.Destroy()

    def no_event(self):
        if self.no_handler:
            self.no_handler()
        self.Destroy()

    def buttons_reset(self, event):
        self.button_no.reset()
        self.button_yes.reset()


class MyOKDialog(wx.Dialog):
    def __init__(self, parent=None, content="", pos=wx.DefaultPosition, OK_handler=None):
        wx.Dialog.__init__(self, parent, size=(540, 300), pos=pos, style=wx.SIMPLE_BORDER | wx.TRANSPARENT_WINDOW)
        self.Bind(wx.EVT_LEFT_DOWN, null_handler)
        self.SetBackgroundColour('#2F2F2F')
        self.handler = OK_handler
        warning = wx.StaticText(self, -1, content, style=wx.TE_CENTER)
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Candara')
        warning.SetForegroundColour('White')
        warning.SetFont(font)
        self.button_OK = MyBitButton("OK.png",
                                     self, -1,
                                     handler=self.OK_event)
        seperate = 300 - 79 - warning.GetSize()[1] - 27 - 80
        print(seperate)
        box = wx.BoxSizer(wx.VERTICAL)
        box.AddMany([(warning, 0, wx.ALIGN_CENTER | wx.TOP, 80),
                     (self.button_OK, 0, wx.ALIGN_CENTRE | wx.TOP, seperate)])
        self.SetSizer(box)
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)
        self.ShowModal()

    def OK_event(self):
        if self.handler is not None:
            self.handler()
        self.Destroy()

    def buttons_reset(self, event):
        self.button_OK.reset()


class MyDialog(wx.Dialog):
    def __init__(self, parent=None, content="", lifeTime=-1, timer_handler=None):
        wx.Dialog.__init__(self, parent, size=(540, 300), style=wx.SIMPLE_BORDER | wx.TRANSPARENT_WINDOW)
        self.SetBackgroundColour('#2F2F2F')
        self.lifeTime = lifeTime
        self.handler = timer_handler
        warning = wx.StaticText(self, -1, content)
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Candara')
        warning.SetForegroundColour('White')
        warning.SetFont(font)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(warning, 0, wx.ALIGN_CENTER | wx.TOP, 120)
        self.SetSizer(box)
        self.Bind(wx.EVT_LEFT_DOWN, null_handler)
        if not self.lifeTime == -1:
            self.set_life_time()
        if timer_handler is not None:
            self.set_timer()
        self.ShowModal()

    def set_life_time(self):
        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_time, self.timer1)
        self.timer1.Start(self.lifeTime*1000)

    def on_time(self, event):
        self.timer1.Stop()
        self.Destroy()

    def set_timer(self):
        self.timer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.evt_handler, self.timer2)
        self.timer2.Start(500)

    def evt_handler(self, event):
        if self.handler is not None:
            if self.handler():
                self.timer2.Stop()
                self.Destroy()
                return True
        return False


def null_handler(event):
    pass
