import wx
import sys
import time
import shutil
import wx.lib.sized_controls as sc

try:
    from PageFormat import FindFit
except:
    def FindFit(*args):
        return "not implemented"

bmp_buffer = wx.Bitmap.FromBuffer


class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


class MainFrame(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(1600, 900))
        panel = wx.Panel(self, -1, pos=(0, 0), size=(1600, 300))
        panel.SetBackgroundColour("#DCDCDC")

        bmp = wx.Image('Icon\\open-folder-outline.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.file_button = wx.BitmapButton(panel, -1, bmp, pos=(0, 0), size=(100, 100))
        self.Bind(wx.EVT_BUTTON, self.on_click_file, self.file_button)

        bmp2 = wx.Image('Icon\\verified-text-paper.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.valid_button = wx.BitmapButton(panel, -1, bmp2, pos=(100, 0), size=(100, 100))
        self.Bind(wx.EVT_BUTTON, self.on_click_valid, self.valid_button)

        bmp3 = wx.Image('Icon\\play-button.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.start_button = wx.BitmapButton(panel, -1, bmp3, pos=(200, 0), size=(100, 100))
        self.Bind(wx.EVT_BUTTON, self.on_click_start, self.start_button)

        bmp4 = wx.Image('Icon\\search.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.search_button = wx.BitmapButton(panel, -1, bmp4, pos=(300, 0), size=(100, 100))
        self.Bind(wx.EVT_BUTTON, self.on_click_search, self.search_button)

        bmp5 = wx.Image('Icon\\send.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.send_button = wx.BitmapButton(panel, -1, bmp5, pos=(400, 0), size=(100, 100))
        self.Bind(wx.EVT_BUTTON, self.on_click_send, self.send_button)

        menubar = wx.MenuBar()
        file = wx.Menu()
        edit = wx.Menu()
        help = wx.Menu()

        file.Append(101, '&Open', 'Open New Document')
        file.Append(102, '&Save', 'Save the Document')
        file.AppendSeparator()

        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit Application')
        file.Append(quit)

        menubar.Append(file, '&File')
        menubar.Append(edit, '&Edit')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        self.CreateStatusBar()

        title_text = wx.StaticText(self, -1, 'Document Management System', (600, 0))
        title_font = wx.Font(40, wx.SWISS, wx.NORMAL, wx.BOLD)
        title_text.SetFont(title_font)
        title_text.SetBackgroundColour("#DCDCDC")

        subtitle_text = wx.StaticText(self, -1, 'Powered by Fino-Chain', (600, 60))
        subtitle_font = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
        subtitle_text.SetFont(subtitle_font)
        subtitle_text.SetBackgroundColour("#DCDCDC")


# ===================================================================================================
        self.panel2 = wx.Panel(panel, -1, pos=(0, 120), size=(1600, 800))
        self.panel2.SetBackgroundColour("#AAAAAA")

# ===================================================================================================
#         self.pdfV = pdfViewer(panel2, -1, pos=(0, 0), size=(750, 700), style=wx.HSCROLL| wx.VSCROLL)
#         self.pdfV.LoadFile("C:\Users\park\Documents\TESTFILE.pdf")
        # self.pdfV.OnPaint()



# ===================================================================================================
        log = wx.TextCtrl(self.panel2, wx.ID_ANY, pos=(750, 0), size=(835, 350),
                          style=wx.TE_MULTILINE | wx.TE_READONLY | wx.SUNKEN_BORDER)

        font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        font2 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        log.SetFont(font2)
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(log, 1, wx.ALL | wx.EXPAND, 40)
        panel.SetSizer(sizer)

        redir = RedirectText(log)
        sys.stdout = redir

#===================================================================================================
        self.log2 = wx.TextCtrl(self.panel2, wx.ID_ANY, pos=(750, 350), size=(835, 350),
                          style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.log2.SetFont(font2)
        self.log2.AppendText("Status Display")
        self.log2.AppendText("\n")

    # Click event for File button
    def on_click_file(self, event):
        select_file_frame = wx.Frame(None, -1, 'Select File')
        select_file_frame.SetSize(200, 100)

        open_file_dialog = wx.FileDialog(select_file_frame, "Upload file", "", "",
                                         "PDF files (*.pdf)|*.pdf",
                                         wx.FD_OPEN)
        open_file_dialog.ShowModal()

        self.write_log("File Selecting...")

        selected_file_name = open_file_dialog.GetFilename()
        selected_file_path = open_file_dialog.GetPath()
        open_file_dialog.Destroy()

        dpath = selected_file_path
        spath = "./document"

        shutil.copy(dpath, spath)

        fi_path = ""
        fi_path += spath
        fi_path += "\\"
        fi_path += selected_file_name

        w_file = open("file.txt", 'w')
        w_file.write(fi_path)

        # PDF PREVIEW
        self.matrix = fitz.Matrix(0.9, 0.9)
        self.paperform = wx.StaticText(self.panel2, wx.ID_ANY,
                                       "", pos=(0, 0), size=(750, 700))
        # self.links = wx.CheckBox(self, wx.ID_ANY,
        #                          u"show links",
        #                          pos=(0, 0), size=(750, 700), style= wx.ALIGN_LEFT)
        # self.links.Value = True

        self.doc = fitz.open(fi_path)
        self.PDFimage = wx.StaticBitmap(self.panel2, -1, self.pdf_show(1), pos=(0, 0),
                                        size=(750, 700))

        self.write_log("File Selected")

        open_file_dialog.Destroy()
        # self.pdfV = pdfViewer(self.panel2, -1, pos=(0, 0), size=(750, 700), style=wx.HSCROLL | wx.VSCROLL)
        # self.pdfV.LoadFile(fi_path)
        # self.pdfV.OnPaint()

    def NeuesImage(self, page=1):

        self.last_page = page
        self.link_rects = []
        self.link_texts = []
        self.current_lnks = []
        self.bitmap = self.pdf_show(page)        # read page image
        if self.links.Value:                     # show links?
            self.draw_links(self.bitmap, page)
        self.PDFimage.SetSize(self.bitmap.Size)  # adjust screen to image size
        self.PDFimage.SetBitmap(self.bitmap)     # put it in screen
        return

    def pdf_show(self, pg_nr):
        page = self.doc.loadPage(int(pg_nr) - 1)  # load the page & get Pixmap
        pix = page.getPixmap(matrix=self.matrix)
        bmp = bmp_buffer(pix.w, pix.h, pix.samples)
        paper = FindFit(page.bound().x1, page.bound().y1)
        self.paperform.Label = "Page format: " + paper
        # if self.links.Value:
        #     self.current_lnks = page.getLinks()
        self.pg_ir = page.bound().round()
        page = None
        pix = None
        return bmp

    # Click event for Start Button
    def on_click_start(self, event):
        flag = True
        MainController.get_ip_address()

        if flag is True:
            MainController.initiate_node()
            flag = False

    # Click event for SEND button
    def on_click_send(self, event):
        trx_dialog = wx.Dialog(None, title="SEND TRANSACTION")
        trx_dialog.SetSize((600, 300))

        trx_panel = wx.Panel(trx_dialog)

        trx_dialog_font = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.password = wx.StaticText(trx_panel, 1, 'Password Code: ', (5, 5), style=wx.LEFT)
        self.password.SetFont(trx_dialog_font)
        self.input_pwd = wx.TextCtrl(trx_panel, pos=(230, 5), size=(180, 30))
        self.input_pwd.SetFont(trx_dialog_font)

        purpose_list = ['Loan', 'Mortgage', 'Lease']
        self.purpose = wx.StaticText(trx_panel, 1, 'Purpose: ', (5, 55), style=wx.LEFT)
        self.purpose.SetFont(trx_dialog_font)
        self.input_purpose = wx.ComboBox(trx_panel, pos=(230, 55), size=(180, 30), choices=purpose_list)
        self.input_purpose.SetFont(trx_dialog_font)

        confirm_button = wx.Button(trx_panel, 3, "SEND", (5, 200))
        confirm_button.SetFont(trx_dialog_font)
        confirm_button.Bind(wx.EVT_BUTTON, self.on_click_confirm)
        confirm_button.SetSize((100, 60))

        trx_dialog.ShowModal()

        # FunctionAPIs.test_tx()

    # INSIDE SEND BUTTON
    def on_click_confirm(self, event):
        import hashlib
        password = self.input_pwd.GetValue()
        purpose = self.input_purpose.GetValue()

        fi_file = open('file.txt', 'r')
        file_location = fi_file.readline()
        fi_file.close()

        # pdf file hash
        pdf_file = open(file_location, 'r')
        read_file = pdf_file.read()
        file_hash = hashlib.sha224(read_file)
        file_hash_hex = file_hash.hexdigest()

        # file hash + additional information(pwd + purpose)
        combined_info = file_hash_hex + purpose + password
        combined_info_hash = hashlib.sha224(combined_info).hexdigest()

        # Send tx
        FunctionAPIs.send_tx('ALL', combined_info_hash)
        self.write_log("Send Transactions")

    def on_click_search(self, event):
        search_dialog = wx.Dialog(None, title="SEARCH")
        search_dialog.SetSize((600, 300))

        search_panel = wx.Panel(search_dialog)

        search_panel_font = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        search_panel_font2 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.search_id = wx.StaticText(search_panel, 1, 'Search ID: ', (5, 5), style=wx.LEFT)
        self.search_id.SetFont(search_panel_font)
        self.input_id = wx.TextCtrl(search_panel, pos=(230, 5), size=(300, 30))
        self.input_id.SetFont(search_panel_font)

        find_button = wx.Button(search_panel, 1, "SEARCH", (5, 200))
        find_button.SetFont(search_panel_font2)
        find_button.Bind(wx.EVT_BUTTON, self.on_click_find)
        find_button.SetSize((100, 60))

        search_dialog.ShowModal()

        return True

    def on_click_find(self, event):
        block_id = self.input_id.GetValue()

        obj_json = FunctionAPIs.search_block_info(block_id)

        if obj_json is False:
            self.log2.AppendText("Search Failed")

        else:
            self.log2.AppendText("TYPE: "+obj_json['type'])
            self.log2.AppendText("\n")
            self.log2.AppendText("Block ID: " + obj_json['block_id'])
            self.log2.AppendText("\n")
            self.log2.AppendText("Time Stamp: " + obj_json['time_stamp'])
            self.log2.AppendText("\n")
            self.log2.AppendText("Block Miner: " + str(obj_json['block_miner']))
            self.log2.AppendText("\n")
            self.log2.AppendText("Previous Block ID: " + obj_json['prev_block_id'])
            self.log2.AppendText("\n")
            self.log2.AppendText("Merkle Root: " + obj_json['merkle_root'])
            self.log2.AppendText("\n")
            self.log2.AppendText("Transactions: " + str(obj_json['tx_list']))
            self.log2.AppendText("\n")
            self.log2.AppendText("Previous Block Hash: " + obj_json['prev_block_hash'])
            self.log2.AppendText("\n")
            self.log2.AppendText("Block Hash: " + obj_json['block_hash'])
            self.log2.AppendText("\n")
            self.log2.AppendText("Nonce: " + str(obj_json['nonce']))
            self.log2.AppendText("\n")
            self.log2.AppendText("---------------------------------------")

    def on_click_valid(self, event):
        valid_dialog = wx.Dialog(None, title="Check Tampering")
        valid_dialog.SetSize((600, 300))

        valid_panel = wx.Panel(valid_dialog)
        valid_panel_font = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        valid_panel_font2 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.valid_pwd = wx.StaticText(valid_panel, 1, 'Input password: ', (5, 5), style=wx.LEFT)
        self.valid_pwd.SetFont(valid_panel_font)
        self.valid_pwd_text = wx.TextCtrl(valid_panel, pos=(230, 5), size=(300, 30))
        self.valid_pwd_text.SetFont(valid_panel_font)

        purpose_list = ['Loan', 'Mortgage', 'Lease']
        self.valid_purpose = wx.StaticText(valid_panel, 1, 'Purpose: ', (5, 55), style=wx.LEFT)
        self.valid_purpose.SetFont(valid_panel_font)
        self.input_purpose = wx.ComboBox(valid_panel, pos=(230, 55), size=(180, 30), choices=purpose_list)
        self.input_purpose.SetFont(valid_panel_font2)

        select_button = wx.Button(valid_panel, 1, "Select File", (5, 200))
        select_button.SetFont(valid_panel_font2)
        select_button.Bind(wx.EVT_BUTTON, self.on_click_file)
        select_button.SetSize((200, 60))

        valid_button = wx.Button(valid_panel, 1, "Check", (300, 200))
        valid_button.SetFont(valid_panel_font2)
        valid_button.Bind(wx.EVT_BUTTON, self.on_click_check)
        valid_button.SetSize((200, 60))

        valid_dialog.ShowModal()

        valid_dialog.Destroy()

    def on_click_check(self, event):
        import hashlib
        password = self.valid_pwd_text.GetValue()
        purpose = self.input_purpose.GetValue()

        fi_file = open('file.txt', 'r')
        file_location = fi_file.readline()
        fi_file.close()

        # pdf file hash
        pdf_file = open(file_location, 'r')
        read_file = pdf_file.read()
        file_hash = hashlib.sha224(read_file)
        file_hash_hex = file_hash.hexdigest()

        # file hash + additional information(pwd + purpose)
        combined_info = file_hash_hex + purpose + password
        combined_info_hash = hashlib.sha224(combined_info).hexdigest()

        # CHECK TAMPERING FunctionAPIs.search_block(combined_info_hash)
        check_result = FunctionAPIs.search_block(combined_info_hash)

        if check_result is True:
            self.write_log("CHECK")
            self.write_log("SUCCESS!")
        else:
            self.write_log("FAIL!")


    # Write to console window
    def write_log(self, message):
        print(time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime()) + ": " + message)


class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, -1, 'Document Management')
        frame.SetIcon(wx.Icon('Icon\\sgsebig.ico', wx.BITMAP_TYPE_ICO))
        frame.Center()
        frame.Show(True)
        Property.ui_frame = frame
        return True


# Start application

if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()