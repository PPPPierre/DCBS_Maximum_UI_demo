import wx
import MyWidget

button_used_path = './Button_inputer/used/'
button_unused_path = './Button_inputer/unused/'


class BitNumberButton(wx.StaticBitmap):
    def __init__(self, parent=None, image_file='', label='',
                 pos=wx.DefaultPosition, handler=None):
        self.label = label
        self.handler = handler
        self.pic_unused = wx.Image(button_unused_path + image_file, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.pic_used = wx.Image(button_used_path + image_file, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        wx.StaticBitmap.__init__(self, parent, -1, self.pic_unused, pos=pos,
                                 style=wx.BORDER_NONE)
        self.Bind(wx.EVT_LEFT_UP, self.event_up)
        self.Bind(wx.EVT_LEFT_DOWN, self.event_down)

    def event_up(self, event):
        self.SetBitmap(self.pic_unused)
        if self.handler is None:
            self.Parent.input(self.label)
        else:
            self.handler()

    def event_down(self, event):
        self.SetBitmap(self.pic_used)

    def reset(self):
        self.SetBitmap(self.pic_unused)


class MyInputer(wx.Dialog):
    def __init__(self, parent=None, id=-1, value=''):
        wx.Dialog.__init__(self, parent, id, 'Inputer',
                           size=(480, 540),
                           pos=(0, 0),
                           style=wx.SIMPLE_BORDER | wx.TRANSPARENT_WINDOW)
        self.SetBackgroundColour('#2F2F2F')
        self.value = value
        self.string = value
        self.insertion_pos = 0
        self.button_list = []
        self.UI_init()
        self.Bind(wx.EVT_LEFT_DOWN, self.null_function)
        self.Bind(wx.EVT_LEFT_UP, self.buttons_reset)

    def UI_init(self):
        # Sizer initial
        self.button_number_sizer = wx.FlexGridSizer(3, 3, 10, 10)
        self.button_function_sizer = wx.BoxSizer(wx.VERTICAL)
        self.zero_point_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create buttons
        self.inputText = MyWidget.MyReadOnlyInput(self, self.value, textL=320, height=60, fontSize=25)
        self.inputText.SetInsertionPointEnd()
        for i in ['7', '8', '9', '4', '5', '6', '1', '2', '3']:
            self.create_number_button(i)
        self.button_zero = BitNumberButton(self, image_file='0.png', label='0')
        self.button_list.append(self.button_zero)
        self.button_point = BitNumberButton(self, image_file='point.png', label='.')
        self.button_list.append(self.button_point)
        self.button_close = BitNumberButton(self, image_file='close.png', label='close', handler=self.event_close)
        self.button_list.append(self.button_close)
        self.button_delete = BitNumberButton(self, image_file='delete.png', label='delete', handler=self.event_delete)
        self.button_list.append(self.button_delete)
        self.button_enter = BitNumberButton(self, image_file='enter.png', label='enter', handler=self.event_enter)
        self.button_list.append(self.button_enter)

        # Layout
        self.zero_point_sizer.AddMany([(self.button_zero, 0, wx.ALIGN_CENTRE | wx.LEFT, 0),
                                       (self.button_point, 0, wx.ALIGN_CENTRE | wx.LEFT, 10)])
        self.button_function_sizer.AddMany([(self.button_close, 0, wx.ALIGN_CENTRE | wx.TOP, 0),
                                            (self.button_delete, 0, wx.ALIGN_CENTRE | wx.TOP, 10),
                                            (self.button_enter, 0, wx.ALIGN_CENTRE | wx.TOP, 10)])
        self.left_vertical_sizer.AddMany([(self.inputText, 0, wx.ALIGN_CENTRE | wx.TOP, 0),
                                          (self.button_number_sizer, 0, wx.ALIGN_CENTRE | wx.TOP, 10),
                                          (self.zero_point_sizer, 0, wx.ALIGN_CENTRE | wx.TOP, 10)])
        self.main_sizer.AddMany([(self.left_vertical_sizer, 0, wx.ALIGN_CENTRE | wx.LEFT, 25),
                                 (self.button_function_sizer, 0, wx.ALIGN_CENTRE | wx.LEFT, 10)])
        self.SetSizer(self.main_sizer)

    def create_number_button(self, label):
        image = label + '.png'
        button = BitNumberButton(self, image_file=image, label=label)
        self.button_list.append(button)
        self.button_number_sizer.Add(button)
        return button

    def buttons_reset(self, event):
        for button in self.button_list:
            button.reset()

    def input(self, elem):
        self.inputText.WriteText(elem)
        self.insertion_pos = self.inputText.GetInsertionPoint()
        self.string = self.inputText.GetValue()

    def event_close(self):
        self.Destroy()

    def event_delete(self):
        self.insertion_pos = self.inputText.GetInsertionPoint()
        self.inputText.Remove(self.insertion_pos-1, self.insertion_pos)
        self.insertion_pos -= 1
        self.string = self.inputText.GetValue()

    def event_enter(self):
        self.Parent.value_raw = self.string
        if self.get_value() == '':
            self.Parent.reset()
            self.Parent.value_OK = False
            self.Destroy()
        elif self.Parent.range_check():
            self.Parent.value_set()
            self.Destroy()
        else:
            MyWidget.MyOKDialog(self, "Please enter a number between " +
                                str(self.Parent.min) + " and " + str(self.Parent.max))
            self.inputText.SetValue(self.string)
            self.inputText.SetInsertionPoint(self.insertion_pos)
            self.Parent.value_OK = False

    def get_value(self):
        return self.inputText.GetValue()

    def null_function(self, event):
        pass


if __name__ == '__main__':
    app = wx.App()
    frame = MyInputer(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
