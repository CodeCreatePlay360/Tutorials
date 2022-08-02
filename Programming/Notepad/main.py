import wx
from wx import stc
from TextEditor import TextEditorPanel


class WxFrame(wx.Frame):
    def __init__(self, parent, title, min_size):
        wx.Frame.__init__(self, parent, title=title)
        self.min_size = min_size

        self.text_ed_panel = TextEditorPanel(self)

        self.SetMinSize(self.min_size)
        self.SetSize(self.min_size)
        self.Center()
        self.Show()


def main():
    # create the wx app object
    wx_app = wx.App()

    # the input arguments to wxFrame are (parent, name and size)
    frame = WxFrame(None, "WxTextEditor", wx.Size(800, 600))

    # load and set the icon
    icon_file = "Resources/notepad.ico"
    icon = wx.Icon(icon_file, wx.BITMAP_TYPE_ICO)
    frame.SetIcon(icon)

    # start the application's main loop
    wx_app.MainLoop()


if __name__ == '__main__':
    main()
