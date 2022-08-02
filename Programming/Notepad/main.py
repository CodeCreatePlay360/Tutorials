import wx
from wx import stc
from TextEditor import TextEditorPanel


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dir_name = ''  # hold the current directory
        self.filename = ''  # hold the file name
        self.leftMarginWidth = 25

        # toggle line numbers in preferences menu
        self.line_numbers_enabled = True

        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        # control + = to zoom in
        self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)

        # control - = to zoom out
        self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        # not show white space
        self.control.SetViewWhiteSpace(False)

        # line numbers
        self.control.SetMargins(5, 0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)

        # status  bar
        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220, 220, 220))

        # Menubar
        file_menu = wx.Menu()
        menu_new = file_menu.Append(wx.ID_NEW, "&New", "Create a new Document")
        menu_open = file_menu.Append(wx.ID_OPEN, "&Open", "Open a existing document")
        menu_save = file_menu.Append(wx.ID_SAVE, "&Save", "save the current Document")
        menu_save_as = file_menu.Append(wx.ID_SAVEAS, "Save &As", "Save a new Document")
        file_menu.AppendSeparator()
        menu_close = file_menu.Append(wx.ID_EXIT, "&Close", "Close the Application")

        edit_menu = wx.Menu()
        menu_undo = edit_menu.Append(wx.ID_UNDO, "&Undo", "Undo last action")
        menu_redo = edit_menu.Append(wx.ID_REDO, "&Redo", "Redo last action")

        edit_menu.AppendSeparator()

        menu_select_all = edit_menu.Append(wx.ID_SELECTALL, "&Select ALl", "Select the entire Document")
        menu_copy = edit_menu.Append(wx.ID_COPY, "&Copy", "Copy Selected text")
        menu_cut = edit_menu.Append(wx.ID_CUT, "&Cut", "Cut the selected text")
        menu_paste = edit_menu.Append(wx.ID_PASTE, "&Paste", "Paste text from the clipboard")

        preferences_menu = wx.Menu()
        menu_line_number = preferences_menu.Append(wx.ID_ANY, "Toggle &Line Numbers", "Show/Hide line numbers colum")

        help_menu = wx.Menu()
        menu_about = help_menu.Append(wx.ID_ABOUT, "&About", "Read about the editor and its making")

        # menu bar creating
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(edit_menu, "&Edit")
        menu_bar.Append(preferences_menu, "&Preferences")
        menu_bar.Append(help_menu, "&Help")
        self.SetMenuBar(menu_bar)

        # calling the functions
        self.Bind(wx.EVT_MENU, self.on_new, menu_new)
        self.Bind(wx.EVT_MENU, self.on_open, menu_open)
        self.Bind(wx.EVT_MENU, self.on_save, menu_save)
        self.Bind(wx.EVT_MENU, self.on_save_as, menu_save_as)
        self.Bind(wx.EVT_MENU, self.on_close, menu_close)

        self.Bind(wx.EVT_MENU, self.on_undo, menu_undo)
        self.Bind(wx.EVT_MENU, self.on_redo, menu_redo)
        self.Bind(wx.EVT_MENU, self.on_select_all, menu_select_all)
        self.Bind(wx.EVT_MENU, self.on_copy, menu_copy)
        self.Bind(wx.EVT_MENU, self.on_cut, menu_cut)
        self.Bind(wx.EVT_MENU, self.on_paste, menu_paste)

        self.Bind(wx.EVT_MENU, self.on_toggle_line_number, menu_line_number)

        self.Bind(wx.EVT_MENU, self.on_about, menu_about)

        self.control.Bind(wx.EVT_KEY_UP, self.update_line_col)
        # key bind
        self.control.Bind(wx.EVT_CHAR, self.on_char_event)

        self.Show()
        self.update_line_col(self)

    def on_new(self, e):
        self.filename = ''
        self.control.SetValue("")

    def on_open(self, e):
        try:
            dlg = wx.FileDialog(self, "Choose a file", self.dir_name, "", "*.*", wx.FD_OPEN)
            # title, directory, type, id
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dir_name = dlg.GetDirectory()
                f = open(os.path.join(self.dir_name, self.filename), 'r')
                self.control.SetValue(f.read())
                f.close()
            dlg.Destroy()
        except:
            dlg = wx.MessageDialog(self, "Couldn't open the file", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def on_save(self, e):
        try:
            f = open(os.path.join(self.dir_name, self.filename), 'w')
            f.write(self.control.GetValue())
        except:
            try:
                dlg = wx.FileDialog(self, "Save file as", self.dir_name, "Untitled", "*.*",
                                    wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if dlg.ShowModal() == wx.ID_OK:
                    self.filename = dlg.GetFilename()
                    self.dir_name = dlg.GetDirectory()
                    f = open(os.path.join(self.dir_name, self.filename), 'w')
                    f.write(self.control.GetValue())
                    f.close()
                dlg.Destroy()
            except:
                pass

    def on_save_as(self, e):
        try:
            dlg = wx.FileDialog(self, "Save file as", self.dir_name, "Untitled", "*.*",
                                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dir_name = dlg.GetDirectory()
                f = open(os.path.join(self.dir_name, self.filename), 'w')
                f.write(self.control.GetValue())
                f.close()
            dlg.Destroy()

        except:
            pass

    def on_close(self, e):
        self.Close(True)

    def on_undo(self, e):
        self.control.Undo()

    def on_redo(self, e):
        self.control.Redo()

    def on_select_all(self, e):
        self.control.SelectAll()

    def on_copy(self, e):
        self.control.Copy()

    def on_cut(self, e):
        self.control.Cut()

    def on_paste(self, e):
        self.control.Paste()

    def on_toggle_line_number(self, e):
        if self.line_numbers_enabled:
            self.control.SetMarginWidth(1, 0)
            self.line_numbers_enabled = False
        else:
            self.control.SetMarginWidth(1, self.leftMarginWidth)
            self.line_numbers_enabled = True

    def on_how_to(self, e):
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, "this is how to.", "how to", size=(400, 400))
        dlg.ShowModal()
        dlg.Destroy()

    def on_about(self, e):
        dlg = wx.MessageDialog(self, "My advance text editor i made with python and wx", " ABout", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def update_line_col(self, e):
        line = self.control.GetCurrentLine() + 1
        col = self.control.GetColumn(self.control.GetCurrentPos())
        stat = "Line %s, Column %s" % (line, col)
        self.StatusBar.SetStatusText(stat, 0)

    def on_char_event(self, e):
        key_code = e.GetKeyCode()
        alt_down = e.AltDown()

        # print(keyCode)

        if key_code == 14:  # Ctrl + N
            self.on_new(self)

        elif key_code == 15:  # Ctrl + o
            self.on_open(self)

        elif key_code == 19:  # Ctrl + s
            self.on_save(self)

        elif alt_down and (key_code == 115):  # Alt + s
            self.on_save_as(self)

        elif key_code == 23:  # Ctrl + w
            self.on_close(self)

        elif key_code == 340:  # F1
            self.on_how_to(self)

        elif key_code == 341:  # F2
            self.on_about(self)

        else:
            e.Skip()


class WxFrame(wx.Frame):
    def __init__(self, parent, title, min_size):
        wx.Frame.__init__(self, parent, title=title)
        self.min_size = min_size

        self.text_ed_panel = TextEditorPanel(self)

        self.SetMinSize(self.min_size)
        self.SetSize(self.min_size)
        self.Center()
        self.Show()


class TestObj:
    def __init__(self):
        pass

    def foo(self):
        print("foo")


def main():
    test_obj = TestObj()
    x = lambda: test_obj.foo()

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
