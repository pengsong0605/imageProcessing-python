import cv2
import wx
from filterFunction import *
class picFilterDialog(wx.Dialog): 
    #id 150-160
    def __init__(self, parent, title,pic): 
        super(picFilterDialog, self).__init__(parent, title = title,size = (250,250))
        self.cv_image=pic 
        self.opt={'颜色变换':symphonyOfColors, '浮雕':cameo, '雕刻':carve, '扩张':expand, '挤压':squeeze,'素描':sketch,'毛玻璃':frostedGlass,'怀旧':reminiscence,'连环画':comicBook,'熔铸':casting,'冰冻':frozen,'羽化':eclosion,'二值化':binaryzation}
        self.makePannel()
    
    def makePannel(self):
        panel = wx.Panel(self) 
        self.vbox = wx.BoxSizer(wx.VERTICAL) 
         
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        self.l1 = wx.StaticText(panel, -1, "滤镜:") 
        hbox1.Add(self.l1, 1, wx.EXPAND|wx.TE_CENTRE|wx.ALL,5)  
        self.choice1 = wx.Choice(panel,id=150,choices = list(self.opt))
        hbox1.Add(self.choice1, 1, wx.EXPAND|wx.TE_CENTRE|wx.ALL,5)  
        self.Bind(wx.EVT_CHOICE,self.picFilter,id=150)
        self.vbox.Add(hbox1) 

        hbox3 = wx.BoxSizer(wx.HORIZONTAL) 
        self.picShow = wx.StaticBitmap(panel,-1,pos=(0, 0),size=(self.cv_image[:2]))
        hbox3.Add(self.picShow, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.vbox.Add(hbox3)
        
        panel.SetSizer(self.vbox) 
        self.adaptiveSize(self.cv_image)
        self.Centre() 
        self.Show() 
        self.Fit()  

    def picFilter(self,event):
        x=event.GetString()
        img=self.opt[x](self.cv_image)
        self.adaptiveSize(img)


    def adaptiveSize(self,cv_image):
        height,width = cv_image.shape[:2]
        #pic = wx.Bitmap.FromRGBA(cv_image)
        pic = wx.Bitmap.FromBuffer(width, height, BGR2RGB(cv_image))
        self.picShow.SetClientSize((width, height))
        self.picShow.SetBitmap(pic)
        self.vbox.Layout()
        super(picFilterDialog, self).SetClientSize((width*1.1, height*1.1))
        super(picFilterDialog, self).Layout()

