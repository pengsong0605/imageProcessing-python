import cv2
import wx
import numpy
from filterFunction import BGR2RGB
class picLightenessDialog(wx.Dialog): 
    #id 140-150
    def __init__(self, parent, title,pic): 
        super(picLightenessDialog, self).__init__(parent, title = title,size = (250,250))
        self.cv_image=pic
        self.makePannel()
        
    
    def makePannel(self):
        panel = wx.Panel(self) 
        self.vbox = wx.BoxSizer(wx.VERTICAL) 
         
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        self.l1 = wx.StaticText(panel, -1, "请移动滑动条来调节亮度:") 
        hbox1.Add(self.l1, 1, wx.EXPAND|wx.TE_CENTRE|wx.ALL,5)   
        self.sld1 = wx.Slider(panel,id=140 ,value = 0, minValue = -125, maxValue = 125,style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.Bind(wx.EVT_SLIDER,self.lightenessChange,id=140)
        hbox1.Add(self.sld1, 3, wx.EXPAND|wx.TE_CENTRE|wx.ALL,5)  
        self.vbox.Add(hbox1) 

        hbox2 = wx.BoxSizer(wx.HORIZONTAL) 
        self.l2 = wx.StaticText(panel, -1, "请移动滑动条来调节对比度x%:") 
        hbox2.Add(self.l2, 1, wx.EXPAND|wx.TE_CENTRE|wx.ALL,5)   
        self.sld2 = wx.Slider(panel,id=141 ,value = 100, minValue = 0, maxValue = 200,style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.Bind(wx.EVT_SLIDER,self.lightenessChange,id=141)
        hbox2.Add(self.sld2, 3, wx.EXPAND|wx.TE_CENTRE|wx.ALL,5)  
        self.vbox.Add(hbox2) 

        hbox3 = wx.BoxSizer(wx.HORIZONTAL) 
        self.picShow = wx.StaticBitmap(panel,-1,pos=(0, 0),size=(self.cv_image[:2]))
        hbox3.Add(self.picShow, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.vbox.Add(hbox3)
        
        panel.SetSizer(self.vbox) 
        self.adaptiveSize(self.cv_image)
        self.Centre() 
        self.Show() 
        self.Fit()  

    def lightenessChange(self,event):
        x=self.sld1.GetValue()
        y=self.sld2.GetValue()

        temp=self.cv_image.copy()  
        (B,G,R) = cv2.split(temp.astype(numpy.int16))
        nB=B*y/100.+x
        nG=G*y/100.+x
        nR=R*y/100.+x
        img=cv2.merge([nB,nG,nR])
        img[img>255]=255
        img[img<0]=0
        img=img.astype(numpy.uint8)
        self.adaptiveSize(img)
        

    def adaptiveSize(self,cv_image):
        height,width = cv_image.shape[:2]
        pic = wx.Bitmap.FromBuffer(width, height, BGR2RGB(cv_image))
        self.picShow.SetClientSize((width, height))
        self.picShow.SetBitmap(pic)
        self.vbox.Layout()
        super(picLightenessDialog, self).SetClientSize((width*1.1, height*1.3))
        super(picLightenessDialog, self).Layout()
