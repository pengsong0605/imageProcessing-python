import wx
from filterFunction import BGR2RGB
class pixelCheckDialog(wx.Dialog): 
    #id 130-140
    def __init__(self, parent, title,pic): 
        super(pixelCheckDialog, self).__init__(parent, title = title,size = (250,250))
        self.cv_image=pic
        self.makePannel()
        self.x=-1
        self.y=-1
        
    
    def makePannel(self):
        panel = wx.Panel(self) 
        vbox = wx.BoxSizer(wx.VERTICAL) 
         
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        l1 = wx.StaticText(panel, -1, "请输入需查看像素X坐标:") 
        hbox1.Add(l1, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)   
        self.t1 = wx.TextCtrl(panel,id=130) 
        self.Bind(wx.EVT_TEXT,self.checkX,id=130)
        hbox1.Add(self.t1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        vbox.Add(hbox1) 

        hbox2 = wx.BoxSizer(wx.HORIZONTAL) 
        l2 = wx.StaticText(panel, -1, "请输入需查看像素Y坐标:") 
        hbox2.Add(l2, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)    
        self.t2 = wx.TextCtrl(panel,id=131)
        #self.Bind(wx.EVT_TEXT,self.checkY,id=131)
        self.Bind(wx.EVT_TEXT,self.getPixelValue,id=131)
        hbox2.Add(self.t2,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        vbox.Add(hbox2) 



        hbox4 = wx.BoxSizer(wx.HORIZONTAL) 
        l4 = wx.StaticText(panel, -1, "像素值为：") 

        hbox4.Add(l4, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.t4 = wx.TextCtrl(panel, id=132,value = "",style = wx.TE_READONLY|wx.TE_CENTER) 

        hbox4.Add(self.t4,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        vbox.Add(hbox4) 
        panel.SetSizer(vbox) 
        
        self.Centre() 
        self.Show() 
        self.Fit()  

    def checkX(self,event): 
        x=event.GetString()
        if x=="":
            pass
        elif not x.isdigit():
            wx.MessageBox("X：请输入纯数字！","X类型错误")
        else:
            self.x=int(x)


    def checkY(self,event): 
        y=event.GetString()
        if y=="":
            return -1
        elif not y.isdigit():
            wx.MessageBox("Y：请输入纯数字！","Y类型错误")
        else:
            self.y=int(y)

    def getPixelValue(self,event):
        if self.checkY(event)==-1:
            pass
        elif (self.x>=0 & self.y>=0):
            try:
                rgb=self.cv_image[self.x,self.y,:]
                if self.cv_image.shape[2]==3:
                    self.t4.SetValue("r:%s g:%s b:%s"%(rgb[2],rgb[1],rgb[0]))
                else:
                    self.t4.SetValue(rgb[0])
            except IndexError as e:
                wx.MessageBox("超出索引，请修改X和Y的值","索引出错")
        else:
            wx.MessageBox("请输入需要查看的像素坐标！","信息提醒")
