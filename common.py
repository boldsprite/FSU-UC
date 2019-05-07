# -*- coding: utf-8 -*-
__author__ = 'YMM'
import xml.etree.ElementTree as ET
import sys
import os.path
import socket
from io import StringIO
import pymysql
import logging
from logging.handlers import RotatingFileHandler
from DBUtils.PooledDB import PooledDB

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
def get_host_ip():
    #获取本机ip地址
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


"""
从配置文件BasicConfig.xml中获取数据库和b接口接入服务器信息
"""
class GetConfigInfo(object):

    #解析xml文件
    def parse_xml(self):
        file = "BasicConfig.xml"
        tree = ET.parse(file)
        root = tree.getroot()
        return root

    #从配置文件中获取数据库配置数据，IP、Port、user、password、db
    def get_database_info(self):
        root = self.parse_xml()
        IP = root.find("./Mysql/IP").text
        Port = root.find("./Mysql/Port").text
        user = root.find("./Mysql/user").text
        password = root.find("./Mysql/password").text
        db = root.find("./Mysql/db").text
        return IP,Port,user,password,db

    #从配置文件中获取B接口接入服务器配置数据，IP、Port、device_id
    def get_SC_info(self):
        root = self.parse_xml()
        SCIP = root.find("./SC/SCIP").text
        SCPort = root.find("./SC/SCPort").text
        SCID = root.find("./SC/SCID").text
        return SCIP,SCPort,SCID

    #从配置文件中获取fsucode及fsu的监控量信息，
    # 返回一个字典：
    #      dict = {"fsu_code":fsu_code,"fsu_id":fsu_id,"device":["device_code":device_code,"mete":[{"MeterType":mete_type,"MeterID":mete_id},[.....]]]}
    def get_mete_data(self):
        root = self.parse_xml()
        device_list = []
        fsu_code = root.find("./Fsu").attrib["Code"]
        fsu_id = root.find("./Fsu").attrib["ID"]
        #fsu_name = base.get_fsu_name(string,port,user,passwd,db,fsu_id)[0][0]

        #获取fsu下所挂设备的信息
        device_data = root.findall("./Fsu/Device")
        for device in device_data:
            device_code = device.attrib["code"]
            #device_name = base.get_device_name(string,port,user,passwd,db,fsu_id,device_code)[0][0]
            mete_data = device.findall("MeteId")
            mete_list = []
            for mete in mete_data:
                mete_type = mete.attrib["type"]
                mete_id = mete.text
                mete_dict = {"MeterType":mete_type,"MeterID":mete_id}
                mete_list.append(mete_dict)
            device_dict = {"device_code":device_code,"mete":mete_list}
            device_list.append(device_dict)
        fsu_dict = {"fsu_code":fsu_code,"fsu_id":fsu_id,"device":device_list}
        return fsu_dict

    #解析协议返回的xml字符串
    def parse_protocol_response(self,str):
        str = unicode(str)
        file = StringIO(str)
        root = ET.parse(file)
        return root

    def modify_time(self,fsu_code,beat_time):
        # 往缓存文件中写
        file = "temp/FSU" + fsu_code + "beattime.xml"
        self.folder_exist("temp")
        self.file_exist(file)
        size = os.path.getsize(file)
        if size ==0 :
            f = open(file, 'w')
            f.write("<?xml version='1.0' encoding='utf-8'?>"
                    "<ZXM10><Connect><HeartbeatTime>2018-09-30 10:31:32</HeartbeatTime></Connect></ZXM10>")
            f.close()
            self.write_time(file,beat_time)
        else:
            self.write_time(file,beat_time)

    def write_time(self,file,beat_time):
        if os.path.exists(file):
            tree = ET.parse(file)
            root = tree.getroot()
            conInfo = root.find("Connect")
            beatTIMENode = conInfo.find("HeartbeatTime")
            beatTIMENode.text = beat_time
            tree.write(file, encoding="utf-8",xml_declaration=True)
        else:
            rootEt = ET.Element("ZXM10")
            conEt = ET.SubElement(rootEt, "Connect")
            beatTimeNode = ET.SubElement(conEt, "HeartbeatTime")
            beatTimeNode.text = beat_time
            et = ET.ElementTree(rootEt)
            et.write(file)

    #修改xml文件的节点内容
    def modify_xml_text(self,node_name,value):
        file = "BasicConfig.xml"
        tree = ET.parse(file)
        root = tree.getroot()
        conInfo = root.find(node_name)
        conInfo.text = str(value)
        tree.write("BasicConfig.xml")

    # 打印日志
    def init_log(self,file_name):
        file_path = "log/" + file_name + ".log"
        self.folder_exist("log")
        self.file_exist(file_path)
        self.output_log(file_path)


    def file_exist(self,file_path):#文件是否存在
        if not os.path.exists(file_path):
            f = open(file_path,'w')
            f.close()
        else:
            pass

    def folder_exist(self,path):#判断log文件夹是否存在
        if not os.path.exists(path):
           os.makedirs(path)
        else:
            pass

    def output_log(self,file_path):
        # 文件输出日志
        logger = logging.getLogger('')
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')
        logger.setLevel(logging.INFO)

        # 控制台输出
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)

        # 文件输出
        th =  RotatingFileHandler(filename=file_path, maxBytes=1024*1024*1024*2, backupCount=1,encoding='utf-8')
        # th = logging.FileHandler(filename=file_path, encoding='utf-8')
        th.setFormatter(formatter)

        # 控制台输出
        logger.addHandler(sh) #把对象加到logger里
        logger.addHandler(th)

"""
数据库的行为
"""
class SqlConn():
    def __init__(self):
        self.conn= DBpool.pool.connection()
        self.cur=self.conn.cursor()
    def cur(self):
        return self.cur()
    def commit(self):
        self.conn.commit()
    def execute(self,sql,fetchone=0):
        self.cur.execute(sql)
        return self.cur.fetchone() if fetchone else self.cur.fetchall()
    def last_id(self,table):
        sql='SELECT LAST_INSERT_ID() from %s'%table
        return self.execute(sql,1)[0]
    def close(self):
        self.cur.close()
        self.conn.close()


class Database(object):
    #连接数据库
    def selectSql(self,string,port,user,passwd,db,sql):
        string = str(string)
        port = int(port)
        user = str(user)
        passwd = str(passwd)
        db = str(db)
        try:
            con =pymysql.connect(
                host= string,
                port = port,
                user = user,
                passwd = passwd,
                db = db,
                charset = 'utf8',
                )         #连接数据库
            try:
                #cur = con.cursor(cursor=pymysql.cursors.DictCursor)
                cur = con.cursor()
                cur.execute(sql)
                results = cur.fetchall()
            except Exception as e:
                raise e
            finally:
                cur.close()  #关闭连接
        except Exception as e:
            results = '数据库连接失败'
        finally:
            return results

    #利用device_id获取fsu的名称
    def get_fsu_name(self,string,port,user,passwd,db,id):
        sql = "SELECT device_name from t_cfg_device WHERE device_id = '%s'"%id
        return self.selectSql(string,port,user,passwd,db,sql)

    #利用fsu_device_id和device_code获取fsu下属设备的名称
    def get_device_name(self,string,port,user,passwd,db,id,device_code):
        sql =("SELECT d.device_name "
              "from t_cfg_monitordevice m "
              "join t_cfg_device d ON d.device_id = m.device_id "
              "WHERE m.fsu_device_id = '%s' and d.device_code ='%s'")%(id,device_code)
        return self.selectSql(string,port,user,passwd,db,sql)

    #利用mete_id获取监控量的alarm_level
    def get_alarm_level(self,string,port,user,passwd,db,mete_id):
        sql = "SELECT alarmlevel FROM t_cfg_telesignal WHERE mete_id = '%s'"%mete_id
        return self.selectSql(string,port,user,passwd,db,sql)

    #利用mete_code获取监控量名称
    def get_mete_name(self,string,port,user,passwd,db,mete_code):
        sql = "SELECT mete_name from t_cfg_metemodel_detail WHERE mete_id = '%s'"%mete_code
        return self.selectSql(string,port,user,passwd,db,sql)

    #获取b接口接入服务器下的所有fsu设备的信息
    def get_fsu_info(self,string,port,user,passwd,db,access_device_id):
        sql = ("SELECT d.device_name,d.device_code,d.device_id,p.precinct_name,p1.precinct_name station_name "
                "FROM t_cfg_fsu f "
                "JOIN t_cfg_device d on d.device_id = f.device_id "
                "JOIN t_cfg_precinct p on d.precinct_id = p.precinct_id "
                "JOIN t_cfg_precinct p1 on p.up_precinct_id = p1.precinct_id "
             "WHERE f.access_device_id = '%s'")%access_device_id
        return self.selectSql(string,port,user,passwd,db,sql)

    #获取fsu下所有监控设备的信息
    def get_monitordevice_info(self,string,port,user,passwd,db,fsu_device_id):
        sql = ("SELECT d.device_name,d.device_code,d.device_id FROM t_cfg_monitordevice m "
               "JOIN t_cfg_device d on d.device_id = m.device_id "
               "WHERE m.fsu_device_id = '%s'")%fsu_device_id
        return self.selectSql(string,port,user,passwd,db,sql)

    #获取设备下所有监控量的信息
    def get_device_mete_info(self,string,port,user,passwd,db,device_id):
        sql = ("SELECT me.mete_name,m.mete_id,m.mete_kind FROM t_cfg_device d "
               "JOIN t_cfg_metemodel_detail m ON m.model_id = d.device_model "
               "JOIN t_cfg_mete me on me.mete_code = m.mete_code "
               "WHERE d.device_id = '%s'")% device_id
        return self.selectSql(string,port,user,passwd,db,sql)

if __name__ == '__main__':
    string = "10.45.156.179"
    port = 3306
    user = "root"
    passwd = "zxm10"
    db = "usmsc"
    a = GetConfigInfo()
    b=a.get_mete_data()
    print b