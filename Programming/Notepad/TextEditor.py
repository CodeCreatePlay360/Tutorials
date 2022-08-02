import wx
import os
from wx import stc


class TextEditorPanel(wx.Panel):
    id_new = wx.NewId()
    id_open = wx.NewId()
    id_save = wx.NewId()
    id_save_as = wx.NewId()
    id_close = wx.NewId()

    id_undo = wx.NewId()
    id_redo = wx.NewId()
    id_select_all = wx.NewId()
    id_copy = wx.NewId()
    id_cut = wx.NewId()
    id_paste = wx.NewId()

    id_toggle_line_numbers = wx.NewId()

    id_help = wx.NewId()

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent)
        self.frame = parent

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)

        self.save_file_dir = ""
        self.save_file_name = ""
        self.line_numbers_enabled = True

        self.left_margin_width = 25
        self.text_editor_ctrl = None
        self.menu_bar = None

        # map events to their respective function calls
        self.event_map = {
            self.id_new: self.on_file_new,
            self.id_open: self.on_file_open,
            self.id_save: self.on_file_save,
            self.id_save_as: self.on_file_save_as,
            self.id_close: self.on_close,

            self.id_undo: lambda: self.text_editor_ctrl.Undo(),
            self.id_redo: lambda: self.text_editor_ctrl.Redo(),
            self.id_select_all: lambda: self.text_editor_ctrl.SelectAll(),
            self.id_copy: lambda: self.text_editor_ctrl.Copy(),
            self.id_cut: lambda: self.text_editor_ctrl.Cut(),
            self.id_paste: lambda: self.text_editor_ctrl.Paste(),

            self.id_toggle_line_numbers: self.on_toggle_line_numbers_display,

            self.id_help: self.show_about_dialog,
        }

        self.create_text_editor()
        self.create_menu_bar()

        # create status bar
        self.frame.CreateStatusBar()
        self.frame.StatusBar.SetBackgroundColour((220, 220, 220))

        self.main_sizer.Add(self.text_editor_ctrl, proportion=1, flag=wx.EXPAND, border=0)
        self.main_sizer.Layout()

        self.update_status_bar_text()

    def create_text_editor(self):
        self.text_editor_ctrl = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        # control + = to zoom in
        self.text_editor_ctrl.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)

        # control - = to zoom out
        self.text_editor_ctrl.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        # not show white space
        self.text_editor_ctrl.SetViewWhiteSpace(False)

        # line numbers
        self.text_editor_ctrl.SetMargins(5, 0)
        self.text_editor_ctrl.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.text_editor_ctrl.SetMarginWidth(1, self.left_margin_width)

    def create_menu_bar(self):
        self.menu_bar = wx.MenuBar()
        self.frame.SetMenuBar(self.menu_bar)

        # Menubar
        # ----------------------
        # create file menus
        file_menu = wx.Menu()
        file_menu.Append(self.id_new, "&New")
        file_menu.Append(self.id_open, "&Open")
        file_menu.Append(self.id_save, "&Save")
        file_menu.Append(self.id_save_as, "Save &As")
        file_menu.AppendSeparator()
        file_menu.Append(self.id_close, "&Close")
        # -------------------------------------------------

        # create edit menus
        edit_menu = wx.Menu()
        edit_menu.Append(self.id_undo, "&Undo")
        edit_menu.Append(self.id_redo, "&Redo")

        edit_menu.AppendSeparator()

        edit_menu.Append(self.id_select_all, "&Select All")
        edit_menu.Append(self.id_copy, "&Copy")
        edit_menu.Append(self.id_cut, "&Cut")
        edit_menu.Append(self.id_paste, "&Paste")
        # ----------------------------------------------------

        # create preferences menus
        preferences_menu = wx.Menu()
        preferences_menu.Append(self.id_toggle_line_numbers, "&Toggle Line Numbers")
        # ----------------------------------------------------

        # create help and about menus
        about_menu = wx.Menu()
        about_menu.Append(self.id_help, "&About", "Read about the editor and its making")

        self.menu_bar.Append(file_menu, "&File")
        self.menu_bar.Append(edit_menu, "&Edit")
        self.menu_bar.Append(preferences_menu, "&Preferences")
        self.menu_bar.Append(about_menu, "&Help")

        self.frame.Bind(wx.EVT_MENU, self.on_event)

    def on_file_new(self):
        self.save_file_dir = ""
        self.save_file_name = ""
        self.text_editor_ctrl.SetValue("")

    def on_file_open(self):
        # first check if the directory of last save already exists,
        # if yes than set browse directory to that
        if os.path.isdir(self.save_file_dir):
            browse_dir = self.save_file_dir
        # else set browse directory to current working directory
        else:
            browse_dir = os.getcwd()

        try:
            dlg = wx.FileDialog(self, "Choose a file", browse_dir, "", "*.txt*", wx.FD_OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.save_file_name = dlg.GetFilename()
                self.save_file_dir = dlg.GetDirectory()
                f = open(os.path.join(self.save_file_dir, self.save_file_name), 'r')
                self.text_editor_ctrl.SetValue(f.read())
                f.close()
            dlg.Destroy()

        except:
            dlg = wx.MessageDialog(self, "Couldn't open the file", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def on_file_save(self):
        if os.path.isdir(self.save_file_dir) and os.path.isfile(self.save_file_name):
            with open(os.path.join(self.save_file_dir, self.save_file_name), 'w') as f:
                f.write(self.text_editor_ctrl.GetValue())
                f.close()
        else:
            self.on_file_save_as()

    def on_file_save_as(self):
        # first check if the directory of last save already exists,
        # if yes than set browse directory to that
        if os.path.isdir(self.save_file_dir):
            browse_dir = self.save_file_dir
        # else set browse directory to current working directory
        else:
            browse_dir = os.getcwd()

        flags = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        dlg = wx.FileDialog(self, "Save file as", browse_dir, "Untitled", "*.txt*", flags)
        if dlg.ShowModal() == wx.ID_OK:
            self.save_file_name = dlg.GetFilename()
            self.save_file_dir = dlg.GetDirectory()
            f = open(os.path.join(self.save_file_dir, self.save_file_name), 'w')
            f.write(self.text_editor_ctrl.GetValue())
            f.close()

        dlg.Destroy()

    def on_close(self):
        self.frame.Close()

    def on_toggle_line_numbers_display(self):
        if self.line_numbers_enabled:
            self.text_editor_ctrl.SetMarginWidth(1, 0)
            self.line_numbers_enabled = False
        else:
            self.text_editor_ctrl.SetMarginWidth(1, self.left_margin_width)
            self.line_numbers_enabled = True

        self.update_status_bar_text()

    def show_about_dialog(self):
        dlg = wx.MessageDialog(None, "WxPython text editor tutorial by CodeCreatePlay...!", "About", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def update_status_bar_text(self):
        line = self.text_editor_ctrl.GetCurrentLine() + 1
        col = self.text_editor_ctrl.GetColumn(self.text_editor_ctrl.GetCurrentPos())
        stat = "[Info] Line %s, Column %s" % (line, col)
        self.frame.StatusBar.SetStatusText(stat, 0)

    def on_event(self, event):
        evt_id = event.GetId()

        if evt_id in self.event_map.keys():
            function = self.event_map[evt_id]
            function()

        event.Skip()
