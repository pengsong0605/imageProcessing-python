#encoding=utf-8
import wx
import os
import cv2
import time
import numpy  
from pixelCheckDialog import pixelCheckDialog 
from picDealDialog import picDealDialog
from picLightenessDialog import picLightenessDialog
from picFilterDialog import picFilterDialog
from filterFunction import BGR2RGB


class dmFrame(wx.Frame):
    """
    A Frame that Jingdong tool include login 、seckill and so on.
    """
    #初始化
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(dmFrame, self).__init__(*args, **kw)
        self.makePanel()
        self.makeMenu()
       # self.makeTool()
        self.makeIco()
        self.Centre()
        self.welcome()

    #欢迎界面
    def welcome(self):
        image = wx.Image('ico\welcome.PNG', wx.BITMAP_TYPE_PNG)
        temp = image.ConvertToBitmap() 
        self.picShowFrame.SetClientSize((310, 220))
        self.picShowFrame.SetBitmap(temp)
        self.sizer.Layout()
        super(dmFrame, self).SetClientSize((310, 220))
        super(dmFrame, self).Layout()

        
    # 初始化面板
    def makePanel(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panelTop = wx.Panel(self)
        self.picShowFrame = wx.StaticBitmap(self.panelTop,-1,pos=(0, 0),size=(0,0))  
        self.sizer.Add(self.panelTop, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

    #加载图标
    def makeIco(self):
        icon = wx.Icon()
        icon.LoadFile(r"ico\48.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

    #菜单栏(100-120)
    def makeMenu(self):
        menubar = wx.MenuBar()

        #菜单选项-
        fileMenu=wx.Menu()
        aboutMenu=wx.Menu()
        picInfoMenu=wx.Menu()
        picDealMenu=wx.Menu()
        grayLevelMenu=wx.Menu()


        #文件菜单
        openItem=wx.MenuItem(fileMenu,100,text="打开图片\tCtrl+Q",helpString="打开需要处理的图片")
        self.Bind(wx.EVT_MENU,self.openPicDeal,id=100)
        fileMenu.Append(openItem)
        fileMenu.AppendSeparator()#分隔符

        exitItem=wx.MenuItem(fileMenu,101,text="退出\tCtrl+X",helpString="退出该软件")
        self.Bind(wx.EVT_MENU,self.exitDeal,id=101)
        fileMenu.Append(exitItem)
        #loginMenu.AppendSeparator()#分隔符

        #关于
        aboutItem = wx.MenuItem(aboutMenu, 102, text="关于软件\tCtrl+A")
        self.Bind(wx.EVT_MENU,self.aboutDeal,id=102)
        aboutMenu.Append(aboutItem)

        #图片信息
        pixelItem=wx.MenuItem(picInfoMenu,103,text="像素介绍\tCtrl+P")
        self.Bind(wx.EVT_MENU,self.pixelDeal,id=103)
        picInfoMenu.Append(pixelItem)
        picInfoMenu.AppendSeparator()#分隔符

        pixelChackItem=wx.MenuItem(picInfoMenu,104,text="像素查看\tCtrl+O")
        self.Bind(wx.EVT_MENU,self.pixelCheckDeal,id=104)
        picInfoMenu.Append(pixelChackItem)
        picInfoMenu.AppendSeparator()#分隔符

        picGetWHItem=wx.MenuItem(picInfoMenu,105,text="图像宽高\tCtrl+W")
        self.Bind(wx.EVT_MENU,self.picGetWH,id=105)
        picInfoMenu.Append(picGetWHItem)

        #图像变换-放大、缩小、旋转、二值化、灰度化、加亮变暗
        picZoomItem=wx.MenuItem(picDealMenu,106,text="图片缩放\tCtrl+Z")
        self.Bind(wx.EVT_MENU,self.picZoom,id=106)
        picDealMenu.Append(picZoomItem)
        picDealMenu.AppendSeparator()

        picRotateItem=wx.MenuItem(picDealMenu,107,text="图片旋转\tCtrl+R")
        self.Bind(wx.EVT_MENU,self.picRotate,id=107)
        picDealMenu.Append(picRotateItem)
        picDealMenu.AppendSeparator()

        picLightenessItem=wx.MenuItem(picDealMenu,108,text="亮度和对比度\tCtrl+L")
        self.Bind(wx.EVT_MENU,self.picLighteness,id=108)
        picDealMenu.Append(picLightenessItem)
        picDealMenu.AppendSeparator()

        picFilterItem=wx.MenuItem(picDealMenu,109,text="滤镜\tCtrl+F")
        self.Bind(wx.EVT_MENU,self.picFilter,id=109)
        picDealMenu.Append(picFilterItem)
        

        #绑定到菜单栏
        menubar.Append(fileMenu, '&文件')
        menubar.Append(picInfoMenu,'&图片信息')
        menubar.Append(picDealMenu,'&图片处理')
        menubar.Append(aboutMenu, '&关于')
        self.SetMenuBar(menubar)


    #点击处理函数
    def picFilter(self,event):
        try:
            dialog = picFilterDialog(self.panelTop,title="滤镜",pic=self.cv_image)
            dialog.ShowModal()
        #except AttributeError as e:
        #    wx.MessageBox("请先选择所要需要查看的图片" ,"error")
        except Exception as e:  
                wx.MessageBox("something is error\n%s" %e)  

    def picLighteness(self,event):
        try:
            dialog = picLightenessDialog(self.panelTop,title="亮度和对比度",pic=self.cv_image)
            dialog.ShowModal()
        #except AttributeError as e:
        #    wx.MessageBox("请先选择所要需要查看的图片" ,"error")
        except Exception as e:  
                wx.MessageBox("something is error\n%s" %e)  

    def picRotate(self,event):
        try:
            dialog = picDealDialog(self.panelTop,title="图片旋转",pic=self.cv_image)
            dialog.bindRotate()
            dialog.ShowModal()
        #except AttributeError as e:
        #    wx.MessageBox("请先选择所要需要查看的图片" ,"error")
        except Exception as e:  
                wx.MessageBox("something is error\n%s" %e)  

    def picZoom(self,event):
        try:
            dialog = picDealDialog(self.panelTop,title="图片缩放",pic=self.cv_image)
            dialog.bindZoom()
            dialog.ShowModal()
        #except AttributeError as e:
        #    wx.MessageBox("请先选择所要需要查看的图片" ,"error")
        except Exception as e:  
                wx.MessageBox("something is error\n%s" %e)  

    def picGetWH(self,event):
        wx.MessageBox("该图片的宽为：{0[1]}\n该图片的高为：{0[0]}".format(self.cv_image.shape[:2]),"查看图像宽高")

    def openPicDeal(self,event):
        #创建文件框
        dialog = wx.FileDialog(self,"Open file...",os.getcwd(),style=wx.FD_OPEN,wildcard="*.png;*.jpg;*.bmp")
        #这里有个概念：模态对话框和非模态对话框. 它们主要的差别在于模态对话框会阻塞其它事件的响应,
        #而非模态对话框显示时,还可以进行其它的操作. 此处是模态对话框显示. 其返回值有wx.ID_OK,wx.ID_CANEL;
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
            try:                
                self.cv_image=cv2.imread(filename)
                self.showPic(self.cv_image)
            except Exception as e:  
                wx.MessageBox("open pic failed\n%s" %e)  
        #销毁对话框,释放资源.
        dialog.Destroy()
        

    def showPic(self,cvImage):
        height,width = cvImage.shape[:2]
        pic = wx.Bitmap.FromBuffer(width, height, BGR2RGB(cvImage))
        self.picShowFrame.SetClientSize((width, height))
        self.picShowFrame.SetBitmap(pic)
        self.sizer.Layout()
        super(dmFrame, self).SetClientSize((width, height))
        super(dmFrame, self).Layout()

    def exitDeal(self,e):
        exit(0)

    def aboutDeal(self,event):
        wx.MessageBox(
            "该软件主要实现一些图像处理的常见功能。\n该软件仅用于学术讨论，版权归松裘所有。",
            caption="关于"
            )

    def pixelDeal(self,event):
        wx.MessageBox('''
        像素是指由图像的小方格即所谓的像素(pixel)组成的，
        这些小方块都有一个明确的位置和被分配的色彩数值，
        而这些一小方格的颜色和位置就决定该图像所呈现出来
        的样子。可以将像素视为整个图像中不可分割的单位或
        者是元素，不可分割的意思是它不能够再切割成更小单
        位抑或是元素，它是以一个单一颜色的小格存在。每一
        个点阵图像包含了一定量的像素，这些像素决定图像在
        屏幕上所呈现的大小
        '''
        ,"像素介绍") 

    def pixelCheckDeal(self,event):
        try:
            dialog = pixelCheckDialog(self.panelTop,title="像素查看",pic=self.cv_image)
            dialog.ShowModal()
        except AttributeError as e:
            wx.MessageBox("请先选择所要需要查看的图片" ,"error")
        except Exception as e:  
                wx.MessageBox("something is error\n%s" %e)  


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = dmFrame(None, title='dmTool',style=wx.DEFAULT_FRAME_STYLE^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX ),size=(550,550))
    frm.Show()
    app.MainLoop()



