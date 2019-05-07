# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Fri Oct 26 11:01:43 2018
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from protocol import *
from PyQt4.QtCore import Qt
from common import *
import threading
import random
import global_variable

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

round_data_flag = False

"""
UI界面类
"""
class Ui_Form(object):
    def __init__(self):
        self.value = ''
        self.t_senddata = threading.Thread()  #循环上报线程

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(562, 520)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("file/timg.gif")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)

        #数据库配置模块
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 501, 80))
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(22, 23, 31, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(60, 20, 101, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(200, 23, 31, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(230, 20, 91, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 41, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_3 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(60, 50, 101, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(200, 50, 31, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit_4 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(230, 50, 91, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(350, 50, 41, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_5 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_5.setGeometry(QtCore.QRect(390, 50, 91, 20))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))

        #B接口接入服务器配置模块
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 110, 341, 80))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(22, 23, 31, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEdit_6 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(60, 20, 101, 20))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(200, 23, 31, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.lineEdit_7 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_7.setGeometry(QtCore.QRect(230, 20, 91, 20))
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(20, 50, 41, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.lineEdit_8 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_8.setGeometry(QtCore.QRect(60, 50, 261, 20))
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))

        #展示fsu树按钮
        self.pushButton_6 = QtGui.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(390, 120, 75, 23))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton"))

        #注册按钮
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(390, 150, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        #提示框
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(340, 170, 180, 40))
        self.label_9.setStyleSheet("color:red;font-size:15px")
        self.label_9.setAlignment(Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))

        #设备树模块：
             #一级树: fsu设备名称：fsu设备编码
             #二级树：fsu设备下级设备名称：下级设备编码
             #三级树：MeterId：下级设备所拥有的监控量mete_id
        self.tree = QtGui.QTreeWidget(Form) #建立树
        self.tree.setGeometry(QtCore.QRect(30, 210, 280, 291))
        self.tree.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels([_fromUtf8('FSU树')])

        #上报告警按钮
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 220, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        #消除告警按钮
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(360, 260, 75, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        #上报数据模块
        self.groupBox_3 = QtGui.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(330, 300, 210, 200))
        self.groupBox_3.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))

        self.combo = QtGui.QComboBox(self.groupBox_3)#单次上报
        self.combo.setGeometry(QtCore.QRect(15, 26, 70, 20))
        self.combo.addItem(_fromUtf8("遥测量"))
        self.combo.addItem(_fromUtf8("遥信量"))

        self.label_14 = QtGui.QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(105, 28, 70, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.lineEdit_11 = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_11.setGeometry(QtCore.QRect(145, 25, 40, 20))
        self.lineEdit_11.setObjectName(_fromUtf8("lineEdit_11"))
        self.pushButton_4 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(60, 70, 70, 20))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))

        self.label_15 = QtGui.QLabel(self.groupBox_3)#分割线
        self.label_15.setGeometry(QtCore.QRect(5, 96, 205, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_15.setStyleSheet("color:white")


        self.label_10 = QtGui.QLabel(self.groupBox_3)#循环上报
        self.label_10.setGeometry(QtCore.QRect(10, 118, 31, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.lineEdit_9 = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_9.setGeometry(QtCore.QRect(40, 115, 40, 20))
        self.lineEdit_9.setObjectName(_fromUtf8("lineEdit_9"))
        self.label_11 = QtGui.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(100, 118, 31, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.lineEdit_10 = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_10.setGeometry(QtCore.QRect(130, 115, 40, 20))
        self.lineEdit_10.setObjectName(_fromUtf8("lineEdit_10"))
        self.label_16 = QtGui.QLabel(self.groupBox_3)
        self.label_16.setGeometry(QtCore.QRect(180, 118, 40, 16))
        self.label_16.setObjectName(_fromUtf8("label_16"))

        self.label_12 = QtGui.QLabel(self.groupBox_3)
        self.label_12.setGeometry(QtCore.QRect(10, 145, 60, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.lineEdit_12 = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_12.setGeometry(QtCore.QRect(70, 141, 70, 20))
        self.lineEdit_12.setObjectName(_fromUtf8("lineEdit_10"))
        self.label_13 = QtGui.QLabel(self.groupBox_3)
        self.label_13.setGeometry(QtCore.QRect(140, 145, 80, 16))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_13.setStyleSheet("font-size:11px")

        self.label_16 = QtGui.QLabel(self.groupBox_3)
        self.label_16.setGeometry(QtCore.QRect(140, 170, 40, 16))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_16.setStyleSheet("color:red")
        self.label_16.setAlignment(Qt.AlignCenter)

        self.pushButton_5 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_5.setGeometry(QtCore.QRect(60, 170, 70, 20))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.register)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.send_changed_data)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.send_eliminate_alarm)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.send_single_data)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), self.send_data)
        QtCore.QObject.connect(self.pushButton_6, QtCore.SIGNAL(_fromUtf8("clicked()")), self.show_tree)

        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL('textChanged(QString)'), self.change_mysql_ip)
        QtCore.QObject.connect(self.lineEdit_2, QtCore.SIGNAL('textChanged(QString)'), self.change_mysql_port)
        QtCore.QObject.connect(self.lineEdit_3, QtCore.SIGNAL('textChanged(QString)'), self.change_mysql_user)
        QtCore.QObject.connect(self.lineEdit_4, QtCore.SIGNAL('textChanged(QString)'), self.change_mysql_password)
        QtCore.QObject.connect(self.lineEdit_5, QtCore.SIGNAL('textChanged(QString)'), self.change_mysql_db)
        QtCore.QObject.connect(self.lineEdit_6, QtCore.SIGNAL('textChanged(QString)'), self.change_sc_ip)
        QtCore.QObject.connect(self.lineEdit_7, QtCore.SIGNAL('textChanged(QString)'), self.change_sc_port)
        QtCore.QObject.connect(self.lineEdit_8, QtCore.SIGNAL('textChanged(QString)'), self.change_sc_id)

        self.retranslateUi(Form)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "FSU模拟器", None))
        self.groupBox.setTitle(_translate("Form", "数据库", None))
        self.label.setText(_translate("Form", "地址", None))
        self.label_2.setText(_translate("Form", "端口", None))
        self.label_3.setText(_translate("Form", "用户名", None))
        self.label_4.setText(_translate("Form", "密码", None))
        self.label_5.setText(_translate("Form", "数据库", None))
        self.groupBox_2.setTitle(_translate("Form", "B接口接入服务器", None))
        self.label_6.setText(_translate("Form", "地址", None))
        self.label_7.setText(_translate("Form", "端口", None))
        self.label_8.setText(_translate("Form", "设备ID", None))
        self.pushButton.setText(_translate("Form", "注册", None))
        self.pushButton_2.setText(_translate("Form", "上报告警", None))
        self.pushButton_3.setText(_translate("Form", "消除告警", None))
        self.groupBox_3.setTitle(_translate("Form", "上报数据", None))
        self.label_9.setText(_translate("Form", '请先展示fsu设备树', None))
        self.label_10.setText(_translate("Form", "下限", None))
        self.label_11.setText(_translate("Form", "上限", None))
        self.label_12.setText(_translate("Form", "循环频率：", None))
        self.label_13.setText(_translate("Form", "(单位为秒)", None))
        self.label_14.setText(_translate("Form", "上报值", None))
        self.label_15.setText(_translate("Form", "-"*33, None))
        # self.label_16.setText(_translate("Form", "1", None))
        self.pushButton_4.setText(_translate("Form", "单次上报", None))
        self.pushButton_5.setText(_translate("Form", "循环上报", None))
        self.pushButton_6.setText(_translate("Form", "展示FSU树", None))

        # 从配置文件读取数据，呈现在UI界面
        s = common.GetConfigInfo()
        IP,Port,user,password,db = s.get_database_info()
        SCIP,SCPort,SCID = s.get_SC_info()

        self.lineEdit.setText(_translate("Form", IP, None))
        self.lineEdit_2.setText(_translate("Form", Port, None))
        self.lineEdit_3.setText(_translate("Form", user, None))
        self.lineEdit_4.setText(_translate("Form", password, None))
        self.lineEdit_5.setText(_translate("Form", db, None))
        self.lineEdit_6.setText(_translate("Form", SCIP, None))
        self.lineEdit_7.setText(_translate("Form", SCPort, None))
        self.lineEdit_8.setText(_translate("Form", SCID, None))

    def register(self):
        '''
           fsu注册，有两个操作：
              1.注册行为，fsu发送协议给B接口接入服务器注册
              2.开启守护线程，回复B接口接入服务器的心跳协议
        '''
        SCIP = self.lineEdit_6.text()#B接口接入服务器IP
        SCPort = int(self.lineEdit_7.text())#B接口接入服务器IP
        p = Protocl()

        select_list= self.ifchecked()#选中的二级树设备设备编码list
        count = len(select_list)
        global_variable._init()
        global_variable.set_value("REV_DATA", "")
        p.init_device(select_list)
        p.init_mete(select_list)

        self.label_9.setText(_translate("Form", '正在注册，请等待', None))#将注册结果呈现在UI界面
        register_count = 0

        if count>0:
            for i in range(count):
                QtGui.QApplication.processEvents()
                fsu_code = select_list[i]['fsu_code']

                c = common.GetConfigInfo()

                self.client = p.socket_Connect(SCIP,SCPort,fsu_code) #建立socket连接

                c.init_log("fsu_"+ str(fsu_code))
                out_put = p.register(self.client,fsu_code,select_list[i])#注册行为
                if out_put !="注册成功":
                    break
                else:
                    register_count +=1

                self.label_9.setText(_translate("Form", str(register_count), None))#将注册结果呈现在UI界面
                QtGui.QApplication.processEvents()

                # 开启线程，判断是否按时收到心跳协议，若没收到，则断开连接，重新注册
                self.t_reconnect = threading.Thread(target=p.heertbeat_thread, args=(self.client,fsu_code))
                self.t_reconnect.setDaemon(True)
                self.t_reconnect.start()
            self.label_9.setText(_translate("Form", '注册成功FSU数：%s'%str(register_count), None))
        else:
            self.label_9.setText(_translate("Form", '注册失败，无fsu可注册\n请从fsu树中选择设备', None))

    #发送变化数据，协议号为3001
    def send_changed_data(self,mete_type='alarm',current_value=1,singal='',text ='上报告警成功'):
        new_device_list = []

        select_list= self.ifchecked()#选中的二级树设备设备编码list
        c = common.GetConfigInfo()
        count = len(select_list)
        if count>0:
            for i in range(count):
                fsu_code = select_list[i]['fsu_code']
                device_list = select_list[i]['device']
                if device_list:
                    try:
                        p = Protocl()
                        p.send_data_request(self.client,fsu_code,device_list,mete_type,current_value,singal)
                        self.label_9.setText(_translate("Form",text , None))
                    except Exception as e:
                        logging.info("Fsu: fsuserver unconnect:%s\n" % e)
                else:
                    # logging.info(_fromUtf8("请选择要上报数据的设备"))
                    self.label_9.setText(_translate("Form", "请选择要上报数据的\n设备或监控量", None))

    #消除告警
    def send_eliminate_alarm(self):
        singal = 'clear'
        self.send_changed_data(singal=singal,text ="消除告警成功")

    #上报单条数据
    def send_single_data(self):
        single = self.combo.currentText()
        string = unicode(single)
        current_value = int(self.lineEdit_11.text())
        text = string + u"上报成功"
        self.send_changed_data(mete_type ='telmeter',current_value = current_value,singal=string,text =text)

    #循环上报数据
    def send_round_data(self):
        down_num = int(self.lineEdit_9.text())
        up_num = int(self.lineEdit_10.text())
        frequency = int(self.lineEdit_12.text())
        single = self.combo.currentText()
        string = unicode(single)
        while round_data_flag == True:
            current_value = random.randint(down_num,up_num)
            self.label_16.setText(_translate("Form",str(current_value), None))
            QtGui.QApplication.processEvents()
            self.send_changed_data(mete_type ='telmeter',current_value = current_value,singal=string,text ="正在循环上报数据")
            time.sleep(frequency)

    def wait_round_data_send_terminate(self,th):
        while(th.isAlive()):
            # print   "round data send thread state: "+str(th.isAlive())
            time.sleep(1)

    def send_data(self):
        global round_data_flag
        if  round_data_flag== False:
            round_data_flag = True
            self.pushButton_5.setText(_translate("Form", "结束上报", None))
            self.pushButton_5.setStyleSheet("color:blue")
            self.t_senddata = threading.Thread(target=self.send_round_data)
            self.t_senddata.setDaemon(True)
            self.t_senddata.start()
        else:
            round_data_flag = False
            self.label_9.setText(_translate("Form", "结束循环上报", None))
            self.pushButton_5.setText(_translate("Form", "循环上报", None))
            self.pushButton_5.setStyleSheet("color:black")
            self.wait_round_data_send_terminate(self.t_senddata)

    #二级树-设备树的选中情况：先判断二级树是否被选中，如果选中，将其device_code加入select_list
    def ifchecked(self):
        select_list = []
        child_count = self.tree.topLevelItemCount()
        for m in range(child_count):
            root = self.tree.topLevelItem(m)
            count = root.childCount()
            if root.checkState(0) == QtCore.Qt.Checked or root.checkState(0) == QtCore.Qt.PartiallyChecked:
                fsu_device_code  =  root.text(0).split(':')[1]
                fsu_code = unicode(fsu_device_code).encode("utf-8")
                device_list = []
                for i in range(count):
                    item = root.child(i)
                    sub_childCount  = item.childCount()
                    if item.checkState(0) == QtCore.Qt.Checked or item.checkState(0) == QtCore.Qt.PartiallyChecked:
                        device_code  =  item.text(0).split(':')[1]
                        string = unicode(device_code).encode("utf-8")
                        mete_list = []
                        for j in range(sub_childCount):
                            mete_dict = {}
                            item_1 = item.child(j)
                            if item_1.checkState(0) == QtCore.Qt.Checked or item_1.checkState(0) == QtCore.Qt.PartiallyChecked:
                                mete_id  =  item_1.text(0).split(':')[1]
                                mete_id = unicode(mete_id).encode("utf-8")
                                mete_type = item_1.text(0).split(':')[2]
                                mete_type = unicode(mete_type).encode("utf-8")
                                mete_name = item_1.text(0).split(':')[0]
                                mete_name = unicode(mete_name).encode("utf-8")
                                mete_dict  = {"mete_name":mete_name,"MeterType":mete_type,"MeterID":mete_id}
                                mete_list.append(mete_dict)
                        device_dict = {"device_code":string,"mete":mete_list}
                        if device_dict['mete']:
                            device_list.append(device_dict)
                select_dict =  {"fsu_code":fsu_code,"device":device_list}
                if select_dict['device']:
                    select_list.append(select_dict)
        return select_list

    #展示FSU设备树
    def show_tree(self):
        self.tree.clear()
        base = common.Database()
        IP = self.lineEdit.text()
        Port = self.lineEdit_2.text()
        user = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        db = self.lineEdit_5.text()

        SCID = self.lineEdit_8.text()
        fsu_tuple  = base.get_fsu_info(IP,Port,user,password,db,SCID)
        if fsu_tuple != '数据库连接失败' and fsu_tuple:
            text = '设备树加载成功'
            self.label_9.setText(_translate("Form",text , None))
            for fsu in fsu_tuple:
                fsu_name = fsu[0]
                fsu_code = fsu[1]
                fsu_id = fsu[2]
                precinct_name = fsu[3]
                staion_name = fsu[4]
                self.root= QtGui.QTreeWidgetItem(self.tree)#一级树
                self.root.setText(0,'%s:%s:%s:%s'%(_fromUtf8(fsu_name),fsu_code,_fromUtf8(staion_name),_fromUtf8(precinct_name)))
                self.root.setToolTip(0,'%s:%s:%s:%s'%(_fromUtf8(fsu_name),fsu_code,_fromUtf8(staion_name),_fromUtf8(precinct_name)))
                self.root.setCheckState(0,Qt.Unchecked)

                device_tuple = base.get_monitordevice_info(IP,Port,user,password,db,fsu_id)
                for device in device_tuple:
                    device_name = _fromUtf8(device[0])
                    device_code = device[1]
                    device_id = device[2]
                    self.child = QtGui.QTreeWidgetItem(self.root) #二级树
                    self.child.setText(0,'%s:%s'%(device_name,device_code))
                    self.child.setToolTip(0,'%s:%s'%(device_name,device_code))
                    self.child.setCheckState(0,Qt.Unchecked)

                    mete_tuple = base.get_device_mete_info(IP,Port,user,password,db,device_id)
                    for mete in mete_tuple:
                        mete_name = _fromUtf8(mete[0])
                        MeterCode = mete[1]
                        MeterType = mete[2]
                        child1 = QtGui.QTreeWidgetItem(self.child) #三级树
                        child1.setText(0,'%s:%s:%s'%(mete_name,MeterCode,MeterType))
                        child1.setToolTip(0,'%s:%s:%s'%(mete_name,MeterCode,MeterType))
                        child1.setCheckState(0,Qt.Unchecked)
            self.tree.itemClicked.connect(self.handleChanged)

        elif fsu_tuple == '数据库连接失败':
            text = '数据库连接失败'
            self.label_9.setText(_translate("Form",text , None))
        else:
            text = '设备树加载失败，请检查'
            self.label_9.setText(_translate("Form",text , None))

    #控制设备树的选择状态
    def handleChanged(self,item):
        #选中时
        if item.checkState(0) == Qt.Checked :
            parent = item.parent()
            count = item.childCount()
            if count > 0 and parent == None:
                # 是父节点
                for  i in range(count):
                    #子节点也选中
                    item.child(i).setCheckState(0, Qt.Checked)
                    childcount = item.child(i).childCount()
                    for j in range(childcount):
                        item.child(i).child(j).setCheckState(0, Qt.Checked)
            elif count > 0 and parent != None:
                # 既是子节点又是父节点
                for  i in range(count):
                    #子节点也选中
                    item.child(i).setCheckState(0, Qt.Checked)
                self.updateParentItem(item)
            else:
                # 是子节点
                self.updateParentItem(item)
        elif item.checkState(0) == Qt.Unchecked:
            parent = item.parent()
            count = item.childCount()
            if count > 0 and parent == None:
                for  i in range(count):
                    #子节点也选中
                    item.child(i).setCheckState(0, Qt.Unchecked)
                    childcount = item.child(i).childCount()
                    for j in range(childcount):
                        item.child(i).child(j).setCheckState(0, Qt.Unchecked)
            elif count > 0 and parent != None:
                # 既是子节点又是父节点
                for  i in range(count):
                    #子节点也选中
                    item.child(i).setCheckState(0, Qt.Unchecked)
                self.updateParentItem(item)
            else:
                # 是子节点
                self.updateParentItem(item)
        else:
            self.updateParentItem(item)

    #子节点的状态控制父节点的选择状态
    def updateParentItem(self,item):
        parent = item.parent()
        if parent == None:
             return
        selectedCount = 0
        partiallyCount = 0
        childCount = parent.childCount()
        for i in range(childCount):
            childItem = parent.child(i)
            if childItem.checkState(0) == Qt.Checked:
                selectedCount += 1
            if childItem.checkState(0) == Qt.PartiallyChecked:
                partiallyCount += 1
        if selectedCount <=0 :
            #选中状态
            # if partiallyCount > 0:
            #     parent.setCheckState(0, Qt.PartiallyChecked)
            # else:
                parent.setCheckState(0, Qt.Unchecked)
        elif selectedCount > 0 and selectedCount < childCount:
            #部分选中状态
            parent.setCheckState(0, Qt.PartiallyChecked)
        elif selectedCount == childCount:
            # 未选中状态
            if partiallyCount>0:
                parent.setCheckState(0, Qt.PartiallyChecked)
            else:
                parent.setCheckState(0, Qt.Checked)

        top_parent = parent.parent()
        if top_parent != None:
            selectedCount = 0
            partiallyCount = 0
            childCount = top_parent.childCount()
            for i in range(childCount):
                childItem = top_parent.child(i)
                if childItem.checkState(0) == Qt.Checked:
                    selectedCount += 1
                if childItem.checkState(0) == Qt.PartiallyChecked:
                    partiallyCount += 1
            if selectedCount <=0 :
                #选中状态
                if partiallyCount > 0:
                    top_parent.setCheckState(0, Qt.PartiallyChecked)
                else:
                    top_parent.setCheckState(0, Qt.Unchecked)
            elif selectedCount > 0 and selectedCount < childCount:
                #部分选中状态
                top_parent.setCheckState(0, Qt.PartiallyChecked)
            elif selectedCount == childCount:
                # 未选中状态
                if partiallyCount>0:
                    top_parent.setCheckState(0, Qt.PartiallyChecked)
                else:
                    top_parent.setCheckState(0, Qt.Checked)

    def change_mysql_ip(self):
        value = self.lineEdit.text()
        s = common.GetConfigInfo()
        s.modify_xml_text("./Mysql/IP",value)

    def change_mysql_port(self):
        value = self.lineEdit_2.text()
        s = common.GetConfigInfo()
        s.modify_xml_text("./Mysql/Port",value)

    def change_mysql_user(self):
        value = self.lineEdit_3.text()
        s = common.GetConfigInfo()
        s.modify_xml_text("./Mysql/user",value)

    def change_mysql_password(self):
        value = self.lineEdit_4.text()
        s = common.GetConfigInfo()
        s.modify_xml_text("./Mysql/password",value)

    def change_mysql_db(self):
        value = self.lineEdit_5.text()
        s = common.GetConfigInfo()
        s.modify_xml_text("./Mysql/db",value)

    def change_sc_ip(self):
        value = self.lineEdit_6.text()
        s = common.GetConfigInfo()
        s.modify_xml_text("./SC/SCIP",value)

    def change_sc_port(self):
        value = self.lineEdit_7.text()
        s = common.GetConfigInfo()
        s.modify_xml_text("./SC/SCPort",value)

    def change_sc_id(self):
        value = self.lineEdit_8.text()
        s = common.GetConfigInfo()
        s.modify_xml_text("./SC/SCID",value)