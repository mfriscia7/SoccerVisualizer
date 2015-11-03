import wx

class MainWindow(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'EPL Stats', size=(780,600))

        status = self.CreateStatusBar()
        menubar = wx.MenuBar()

        first = wx.Menu()
        second = wx.Menu()

        first.Append(wx.NewId(), "New Window", "This is a new window")
        menubar.Append(first, "File")
        menubar.Append(second, "Second")
        self.SetMenuBar(menubar)
        panel = wx.Panel(self)


        x1_label = wx.StaticText(panel, -1, "x axis", (25,10))
        x2_label = wx.StaticText(panel, -1, "x axis", (155,10))
        y1_label = wx.StaticText(panel, -1, "y axis", (305,10))
        y2_label = wx.StaticText(panel, -1, "y axis", (435,10))

        list_box_size = (120,60)

        attr_list = ['Points', 'Home Wins', 'Goals Scored', 'Goals Conceded', 'Shots', 'Shots Against']
        attr_list_with_none = ['None'] + attr_list

        x_attr1 = wx.ListBox(panel, -1, (20,30), list_box_size, attr_list, wx.LB_SINGLE)
        x_attr2 = wx.ListBox(panel, -1, (150,30), list_box_size, attr_list_with_none, wx.LB_SINGLE)
        y_attr1 = wx.ListBox(panel, -1, (300,30), list_box_size, attr_list, wx.LB_SINGLE)
        y_attr2 = wx.ListBox(panel, -1, (430,30), list_box_size, attr_list_with_none, wx.LB_SINGLE)
        x_attr1.SetSelection(0)
        x_attr2.SetSelection(0)
        y_attr1.SetSelection(0)
        y_attr2.SetSelection(0)

        x_checkbox = wx.CheckBox(panel, -1, "per game", (25,95), (70,-1))
        y_checkbox = wx.CheckBox(panel, -1, "per game", (305,95), (70,-1))


        go_button = wx.Button(panel, label='Go', pos=(600,50), size=(62,22))
        #self.Bind(wx.EVT_BUTTON, self.run_parameters)
        self.Bind(wx.EVT_CLOSE, self.closewindow)

    #def run_parameters:
    #    a

    def closewindow(self, event):
        self.Destroy()

if __name__=='__main__':
    app = wx.App(False)
    frame = MainWindow(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
