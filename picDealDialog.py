import cv2
import wx
from filterFunction import BGR2RGB
class picDealDialog(wx.Dialog): 
    #id 140-150
    def __init__(self, parent, title,pic): 
        super(picDealDialog, self).__init__(parent, title = title,size = (250,250))
        self.cv_image=pic
        self.makePannel()
        
    
    def makePannel(self):
        panel = wx.Panel(self) 
        self.vbox = wx.BoxSizer(wx.VERTICAL) 
         
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        self.l1 = wx.TextCtrl(panel,value = "",style = wx.TE_READONLY) 
        hbox1.Add(self.l1, 3, wx.EXPAND|wx.TE_CENTRE|wx.ALL,5)   
        self.t1 = wx.TextCtrl(panel,id=140,style=wx.TE_PROCESS_ENTER) 
        
        hbox1.Add(self.t1,2,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.vbox.Add(hbox1) 

        hbox2 = wx.BoxSizer(wx.HORIZONTAL) 
        self.picShow = wx.StaticBitmap(panel,-1,pos=(0, 0),size=(self.cv_image[:2]))
        hbox2.Add(self.picShow, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.vbox.Add(hbox2) 
        panel.SetSizer(self.vbox) 
        self.adaptiveSize()
        self.Centre() 
        self.Show() 
        self.Fit()  

    def zoomCheck(self,event):
        x=event.GetString()
        if x=="" or x=="0":
            return
        elif x.count('.')==1 :
            if x.split('.')[1]=='':
                return
            elif x.split('.')[1].isdigit():
                pass
            else:
                wx.MessageBox("请输入纯数字！","类型错误")
                return
        elif not x.isdigit():
            wx.MessageBox("请输入纯数字！","类型错误")
            return
        else:
            pass
        x=float(x)
        height,width = self.cv_image.shape[:2]
        self.cv_image=cv2.resize(self.cv_image,(int(height*x),int(width*x)),interpolation=cv2.INTER_CUBIC)
        self.adaptiveSize()
        

    def adaptiveSize(self):
        height,width = self.cv_image.shape[:2]
        pic = wx.Bitmap.FromBuffer(width, height, BGR2RGB(self.cv_image))
        self.picShow.SetClientSize((width, height))
        self.picShow.SetBitmap(pic)
        self.vbox.Layout()
        super(picDealDialog, self).SetClientSize((width*1.1, height*1.2))
        super(picDealDialog, self).Layout()

    def bindZoom(self):
        self.l1.SetValue("缩放比例（0-max）：")
        self.Bind(wx.EVT_TEXT_ENTER,self.zoomCheck,id=140)

    def bindRotate(self):
        self.l1.SetValue("旋转角度（0°-360°）：")
        self.Bind(wx.EVT_TEXT_ENTER,self.rotateCheck,id=140)

    def rotateCheck(self,event):
        x=event.GetString()
        if not x.isdigit():
            wx.MessageBox("请输入纯数字！","类型错误")
            return
        else:
            pass
        x=int(x)
        self.cv_image=self.rotate(self.cv_image,x)
        self.adaptiveSize()

    @staticmethod
    def rotate(image, angle, center=None, scale=1.0):
        # 获取图像尺寸
        (h, w) = image.shape[:2]

        # 若未指定旋转中心，则将图像中心设为旋转中心
        if center is None:
            center = (w / 2, h / 2)

        # 执行旋转
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h))

        # 返回旋转后的图像
        return rotated
   