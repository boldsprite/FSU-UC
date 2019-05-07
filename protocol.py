# -*- coding: UTF-8 -*-
__author__ = 'YMM'
import socket
import common
import time
import logging
import global_variable

class Protocl(object):

    #连接接入服务器
    def socket_Connect(self,host,port,fsu_code):
        logging.info("FSU:%s is connecting server"%fsu_code)
        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #在客户端开启心跳维护
                client.connect((host, port))
                logging.info("FSU:%s connects server" %fsu_code)
                break
            except Exception as e:
                self.close_socket(client)
                logging.info("Fsu:%s, fsuserver unconnect:%s" % (fsu_code, e))
                time.sleep(2) #10s后重新连接
        return client

    #断开socket连接
    def close_socket(self,client):
        if client is not None:
            client.close()

    #注册
    def register(self,client,fsu_code,select_list):
        c = common.GetConfigInfo()
        # fsu_dict = c.get_mete_data()
        # fsu_code = fsu_dict['fsu_code']
        FsuIP = common.get_host_ip()

        # devCode_str = ""
        # xml=("<?xml version='1.0' encoding='utf-8'?>"
        #     "<Request>"
        #       "<PK_Type>"
        #         "<Name>LOGIN</Name>"
        #         "<Code>101</Code>"
        #       "</PK_Type>"
        #       "<Info>"
        #         "<UserName>chinaunicom</UserName>"
        #         "<PassWord>chinaunicom</PassWord>"
        #         "<SUId>04d437057320</SUId>"
        #         "<SURId>04d437057320</SURId>"
        #         "<SUIP>%s</SUIP>"
        #         "<SUPort>8080</SUPort>"
        #         "<SUVendor>znv</SUVendor>"
        #         "<SUModel>IG2000</SUModel>"
        #         "<SUHardVer>1.0.0.0</SUHardVer>"
        #         "<SUConfigTime>2019-04-08 20:02:22</SUConfigTime>"
        #         "<DeviceList>"%(FsuIP))
        #
        # for device in select_list['device']:
        #     device_code = device['device_code']
        #     devCode_str +=("<Device Id='%s' Code='%s' />"%(device_code,device_code))
        xml="&lt;?xml version=\"1.0\" encoding=\"UTF-8\" ?&gt;"
"&#xA;&lt;Request&gt;"
"&#xA;&lt;PK_Type&gt;"
"&#xA;&lt;Name&gt;LOGIN&lt;/Name&gt;"
"&#xA;&lt;Code&gt;101&lt;/Code&gt;"
"&#xA;&lt;/PK_Type&gt;"
"&#xA;&lt;Info&gt;"
"&#xA;&lt;UserName&gt;chinaunicom&lt;/UserName&gt;"
"&#xA;&lt;PassWord&gt;chinaunicom&lt;/PassWord&gt;"
"&#xA;&lt;SUId&gt;04d4370de15e&lt;/SUId&gt;"
"&#xA;&lt;SURId&gt;04d4370de15e&lt;/SURId&gt;"
"&#xA;&lt;SUPort&gt;8080&lt;/SUPort&gt;"
"&#xA;&lt;SUVendor&gt;ZNV&lt;/SUVendor&gt;"
"&#xA;&lt;SUConfigTime&gt;2019-04-08 20:02:22&lt;/SUConfigTime&gt;"
"&#xA;&lt;SUModel&gt;IG2000V3&lt;/SUModel&gt;"
"&#xA;&lt;SUHardVer&gt;1.05&lt;/SUHardVer&gt;"
"&#xA;&lt;SUIP&gt;10.45.148.64&lt;/SUIP&gt;"
"&#xA;&lt;SUVer&gt;1.00.004&lt;/SUVer&gt;"
"&#xA;&lt;DeviceList&gt;"
"&#xA;&lt;Device Id=\"41901\"  RId=\"41901\"/&gt;"
"&#xA;&lt;Device Id=\"91101\"  RId=\"91101\"/&gt;"
"&#xA;&lt;/DeviceList&gt;"
"&#xA;&lt;/Info&gt;"
"&#xA;&lt;/Request&gt;"
"&#xA;"
        try:
            # xml = xml + devCode_str + "</DeviceList><SUVer>1.0</SUVer></Info></Request>"
            # xmlstr=xml.encode("utf8")
            client.send(xml.encode("utf8"))
            login_ack = client.recv(1024)
            root = c.parse_protocol_response(login_ack)
            pkType = root.find("PK_Type")
            code = pkType.find("Code").text
            name = pkType.find("Name").text
            if code == "102" and name == "LOGIN_ACK":
                out_put  = "注册成功"
                logging.info("FSU:%s Successfully registered" %fsu_code)
            else:
                out_put  = "注册失败"
                logging.info("FSU:%s's registration failed" % fsu_code)
        except Exception as e:
            logging.info("FSU:%s's registration failed,%s" % (fsu_code,e))
        return out_put

    #上报变化数据协议，包括告警、遥测量、遥调量等
    #协议号：3001
    #分为两类，告警和其他监控量
    def send_data_request(self,client,fsu_code,device_list,mete_type,current_value,singal):
        mete_str = ""
        xml = (
            "<?xml version='1.0' encoding='utf-8'?>"
            "<Request>"
              "<PK_Type>"
                "<Name>SEND_CHANGED_DATA</Name>"
                "<Code>3001</Code>"
              "</PK_Type>"
              "<Info>"
                "<FsuId>%s</FsuId>"
                "<FsuCode>%s</FsuCode>"
                "<Values>"
                  "<TChangedDataList>"%(fsu_code,fsu_code))
        sy_device_list = global_variable.get_value("mete")
        for device in device_list:
            device_code = device['device_code']
            mete_list = device['mete']
            for sy_device in sy_device_list:
                sy_device_code = sy_device["device_code"]
                if device_code == sy_device_code:
                    sy_mete_list = sy_device['mete']
                    for mete in mete_list:
                        for sy_mete in sy_mete_list:
                            if mete['MeterID'] == sy_mete['mete_id']:
                                MeterType = mete['MeterType']
                                if mete_type == "alarm":
                                    if MeterType == '4':
                                        MeterId = mete['MeterID']
                                        OccurTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                        if singal == 'clear':
                                            CurrentVal = 0
                                            status =  'clear alarm'
                                        else:
                                            CurrentVal = 1
                                            status = 'alarm'
                                        sy_mete['value'] = CurrentVal
                                        mete_str +=("<TChangedData>"
                                              "<MeterType>%s</MeterType>"
                                              "<MeterId>%s</MeterId>"
                                              "<DevId>%s</DevId>"
                                              "<DevCode>%s</DevCode>"
                                              "<CurrentVal>%s</CurrentVal>"
                                              "<Index>%s</Index>"
                                              "<OccurTime>%s</OccurTime>"
                                              "</TChangedData>"%(MeterType,MeterId,device_code,device_code,CurrentVal,MeterId,OccurTime))
                                        # logging.info("fsu send %s data deviceCode:%s, MeterId:%s,MeterType:%s,CurrentVal:%s,OccurTime:%s"%
                                        #              (status,device_code,MeterId,MeterType,CurrentVal,OccurTime))

                                elif mete_type == "telmeter":
                                    if singal == u'遥测量':
                                        if MeterType == '1':
                                            MeterId = mete['MeterID']
                                            OccurTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                            CurrentVal = current_value
                                            sy_mete['value'] = CurrentVal
                                            mete_str +=("<TChangedData>"
                                                      "<MeterType>%s</MeterType>"
                                                      "<MeterId>%s</MeterId>"
                                                      "<DevId>%s</DevId>"
                                                      "<DevCode>%s</DevCode>"
                                                      "<CurrentVal>%s</CurrentVal>"
                                                      "<Index>%s</Index>"
                                                      "<OccurTime>%s</OccurTime>"
                                                      "</TChangedData>"%(MeterType,MeterId,device_code,device_code,CurrentVal,MeterId,OccurTime))
                                            # logging.info("fsu send change data deviceCode:%s, MeterId:%s,MeterType:%s,CurrentVal:%s,OccurTime:%s"%
                                            #              (device_code,MeterId,MeterType,CurrentVal,OccurTime))
                                    elif MeterType == '0':
                                        MeterId = mete['MeterID']
                                        OccurTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                        CurrentVal = current_value
                                        sy_mete['value'] = CurrentVal
                                        mete_str +=("<TChangedData>"
                                                  "<MeterType>%s</MeterType>"
                                                  "<MeterId>%s</MeterId>"
                                                  "<DevId>%s</DevId>"
                                                  "<DevCode>%s</DevCode>"
                                                  "<CurrentVal>%s</CurrentVal>"
                                                  "<Index>%s</Index>"
                                                  "<OccurTime>%s</OccurTime>"
                                                  "</TChangedData>"%(MeterType,MeterId,device_code,device_code,CurrentVal,MeterId,OccurTime))
                                        # logging.info("fsu send change data deviceCode:%s, MeterId:%s,MeterType:%s,CurrentVal:%s,OccurTime:%s"%
                                        #              (device_code,MeterId,MeterType,CurrentVal,OccurTime))
                                    else:
                                        pass
                                else:
                                    pass
        global_variable.set_value("mete",sy_device_list)
        xml = xml + mete_str + "</TChangedDataList></Values></Info></Request>"
        logging.info("fsu send xml request:%s"%xml)
        client.send(xml.encode("utf8"))

    #告警上报，协议号：501
    def send_alarm(self,client,signal=None):
        mete_str = ""
        alarm_xml = (
            "<?xml version='1.0' encoding='UTF-8'?>"
            "<Request>"
                "<PK_Type>"
                    "<Name>SEND_ALARM</Name>"
                    "<Code>501</Code>"
                "</PK_Type>"
                "<Info>"
                    "<Values>"
                        "<TAlarmList>")

        c = common.GetConfigInfo()
        base = common.Database()
        fsu_dict = c.get_mete_data()
        IP,Port,user,password,db = c.get_database_info()

        if signal == 'eliminate':
                AlarmValue = 0
        else:
                AlarmValue = 1

        alarm_no = "0"
        FsuCode = fsu_dict['fsu_code']
        device_list = fsu_dict['device']
        for device in device_list:
            DeviceCode = device['device_code']
            mete_list = device['mete']
            for mete in mete_list:
                if mete['MeterType'] == '4':
                    MeterID = mete['MeterID']
                    AlarmLevel = base.get_alarm_level(IP,Port,user,password,db,MeterID)[0][0]
                    AlarmTime = time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
                    mete_str +=("<TAlarm>"
                                    "<SerialNo>%s</SerialNo>"
                                    "<Type>%s</Type>"
                                    "<Id>%s</Id>"
                                    "<FsuId>%s</FsuId>"
                                    "<FsuCode>%s</FsuCode>"
                                    "<DeviceId>%s</DeviceId>"
                                    "<DeviceCode>%s</DeviceCode>"
                                    "<AlarmTime>%s</AlarmTime>"
                                    "<AlarmLevel>%s</AlarmLevel>"
                                    "<AlarmFlag>%s</AlarmFlag>"
                                    "<AlarmDesc>%s</AlarmDesc>"
                                    "<AlarmValue>%s</AlarmValue>"
                                "</TAlarm>"
                                %(alarm_no,"AI",MeterID,FsuCode,FsuCode,DeviceCode,DeviceCode,AlarmTime,AlarmLevel,"BEGIN","ALARM",AlarmValue))
        alarm_xml = alarm_xml + mete_str + "/TAlarmList></Values></Info></Request>"
        client.send(alarm_xml.encode("utf8"))
        alarm_ack = client.recv(1024)

    #心跳线程
    def heertbeat_thread(self,client,fsu_code):
        while True:
            data = None
            try:
                # TCP连接
                data = client.recv(1024)
            except Exception as e:
                logging.info("Fsu: fsuserver unconnect:%s\n" % e)
                continue

            if data is None:
                continue
            # 解析协议，并返回对应协议
            self.deal_packets(data.decode("utf-8").strip().replace("\n", "").replace("\r", ""),client,fsu_code)

    # 收到的协议包存放到缓存 ,循环处理缓存中协议包
    def deal_packets(self,data,client,fsu_code):
        #logging.info("RECV-ALL: %s" % (data))
        packet_buf = global_variable.get_value("REV_DATA")
        new_data = packet_buf + data
        if len(new_data) < 31457280: #30M
            # 新包和packetBuf加起来没有超过最大缓存
            global_variable.set_value("REV_DATA", new_data)
        else:
            # 超过最大缓存，将原有缓存数据丢掉
            logging.info("data is too large, drop some data!")
            if len(data) > 31457280:
                # 新包数据超过最大缓存，丢掉前面，拷贝后面部分
                start_index = len(data) - 31457280
                global_variable.set_value("REV_DATA", data[start_index:])
            else:
                global_variable.set_value("REV_DATA", data)

        xml_tail_index = 0
        while xml_tail_index >= 0:
            xml_tail_index = self.group_packet(client,fsu_code)
            if xml_tail_index > 0:
                cache_data = global_variable.get_value("REV_DATA")
                s = cache_data[xml_tail_index:]
                global_variable.set_value("REV_DATA", s)

    def group_packet(self,client,fsu_code):
        ''' 处理packet Buf中的数据，找到完整的一包XML进行处理,
            XML样式
            <?xml version=“1.0” encoding=“UTF-8”?>
            <Response> 或 <Request>
            XXX
            </Response> 或 </Request>
        '''
        packet_buf = global_variable.get_value("REV_DATA")
        # 先找xml包标志头
        xml_head_str = "<?xml"
        xml_head_index = packet_buf.find(xml_head_str)
        # 没找到XML头，返回-1
        if xml_head_index < 0:
            return -1

        # 找xml包标志尾
        xml_req_end_str = "</Request>";
        xml_rsp_end_str = "</Response>";
        xml_packet = "";

        # 第二个包头
        xml_head_next = packet_buf.find(xml_head_str, xml_head_index + 1)

        # 没有第二个包头
        if xml_head_next < 0:
            xml_packet = packet_buf[xml_head_index:]
        else:
            xml_packet = packet_buf[xml_head_index:xml_head_next]

        xml_tail = xml_head_next

        end_index = xml_packet.find(xml_req_end_str)
        if end_index < 0:  # 不是请求
            end_index = xml_packet.find(xml_rsp_end_str)
            if end_index < 0:  # 不是完整包
                return xml_tail
            else:  # 响应包
                xml_tail = end_index + len(xml_rsp_end_str)
                xml_packet = xml_packet[0:xml_tail]
        else:  # 请求包
            xml_tail = end_index + len(xml_req_end_str)
            xml_packet = xml_packet[0:xml_tail]

        # 处理完整一包xml协议
        self.deal_single_packet(client,xml_packet,fsu_code)
        return xml_tail

    #处理接入服务器发送的协议
    def deal_single_packet(self,client,data,fsu_code):
        logging.info("RECV: %s" % (data))
        c = common.GetConfigInfo()
        root =c.parse_protocol_response(data)
        if root is None:
            return

        pkType = root.find("PK_Type")
        code = pkType.find("Code").text

        data = None
        # GET_FSUINFO心跳协议
        if code == '1701':
            #logging.info("RECV: %s" % (xmlData))
            infoEt = root.find("Info")
            fsu_code = infoEt.find("FsuCode").text
            #logging.info("FSUINFO:%s" % (fsu_code))

            # 更新心跳时间，用于判断是否需要重连
            # c.modify_time(fsu_code,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            data = self.get_fsuinfo_ack(fsu_code)
        # GET_DATA周期上报协议
        elif code == '401':
            #logging.info("RECV: %s" % (xmlData))
            infoEt = root.find("Info")
            fsu_code = infoEt.find("FsuCode").text
            data =self.get_data_ack(root)
            logging.info("GET_DATA_ACK:%s" % (data))


        if data is None:
            return

        # 发送协议
        try:
            client.send(data.encode("utf8"))
            logging.info("fsu have response to sever's heartbeat:%s" % data)
        except Exception as e:
            logging.info("Fsu:%s, fsuserver unconnect:%s\n" % (fsu_code, e))

    #心跳协议
    def get_fsuinfo_ack(self, fsu_code):
        fsu_info = ("<?xml version='1.0' encoding='utf-8'?>"
                "<Response>"
                    "<PK_Type>"
                        "<Name>GET_FSUINFO_ACK</Name>"
                        "<Code>1702</Code>"
                    "</PK_Type>"
                    "<Info>"
                        "<FsuId>%s</FsuId>"
                        "<FsuCode>%s</FsuCode>"
                        "<TFSUStatus>"
                            "<CPUUsage>10</CPUUsage>"
                            "<MEMUsage>20</MEMUsage>"
                        "</TFSUStatus>"
                        "<Result>1</Result>"
                    "</Info>"
                "</Response>" %
                (fsu_code, fsu_code))
        return fsu_info

    #将fsu下所有设备写入全局变量
    def init_device(self,select_list):
        device_list = []
        count = len(select_list)

        if count>0:
            for i in range(count):
                dev_list = select_list[i]["device"]
                for device in dev_list:
                    device_list.append(device["device_code"])
        global_variable.set_value("DEVICE_IN_FSU", device_list)

    #将所有监控量按类型写入全局变量
    def init_mete(self,select_list):
        dev_dict = {}
        dev_list = []
        count = len(select_list)
        if count>0:
            for i in range(count):
                device_list = select_list[i]["device"]
                for device in device_list:
                    mete_list = []
                    device_code = device["device_code"]
                    for mete in device["mete"]:
                        mete_dict = {"mete_id":mete["MeterID"],"mete_name":mete["mete_name"],"mete_kind":mete["MeterType"],"value":0}
                        mete_list.append(mete_dict)
                    dev_dict = {"device_code":device_code,"mete":mete_list}
                    dev_list.append(dev_dict)
        global_variable.set_value("mete", dev_list)

    #周期上报协议
    def get_data_ack(self, xml_data):
        # 解析接入协议
        xml_info_et = xml_data.find("Info")
        fsu_code = xml_info_et.find("FsuCode").text
        xml_device_list_et = xml_info_et.find("DeviceList")
        xml_device_ets = xml_device_list_et.findall("Device")
        if len(xml_device_ets) == 0:
            logging.info("Fsu:%s, GET_DATA PROTOCOL ERROR" % (fsu_code))
            return

        # get_data返回协议
        data = ("<?xml version='1.0' encoding='utf-8'?>"
                "<Response>"
                    "<PK_Type>"
                        "<Name>%s</Name>"
                        "<Code>%s</Code>"
                    "</PK_Type>"
                    "<Info>"
                        "<FsuId>%s</FsuId>"
                        "<FsuCode>%s</FsuCode>"
                        "<Result>1</Result>"
                        "<Values>"
                            "<DeviceList>" %
                ('GET_DATA_ACK', '402', fsu_code, fsu_code))

        # 获取全局变量
        dev_list = global_variable.get_value("DEVICE_IN_FSU")
        mete_list = global_variable.get_value("mete")
        dev_id = xml_device_ets[0].get("Id")
        if dev_id == "99999999999999": # 获取所有设备数据
            for device_code in dev_list:
                data += ("<Device Id='%s' Code='%s'>" % (device_code, device_code))
                for device in mete_list:
                    if device_code == device["device_code"]:
                        data = self.assembly_mete(data, device['mete']) # 遥测量
                data += "</Device>"
        else:
            for dev_ele in xml_device_ets:
                device_code = dev_ele.get("Id")
                #logging.info("Fsu:%s, GETDATA__DEVICE_ID:%s" % (fsuId, devId))
                data += ("<Device Id='%s' Code='%s'>" % (device_code, device_code))
                for device in mete_list:
                    if device_code == device["device_code"]:
                        data = self.assembly_mete(data, device['mete']) # 遥测量
                data += "</Device>"

        data += "</DeviceList></Values></Info></Response>"
        return data

    # 组装循环上报协议
    def assembly_mete(self, data, mete_dict):
        if  mete_dict is None:
            return
        for mete in mete_dict:
            data += ("<TSemaphore Type='%s' Id='%s' MeasuredVal='%s' SetupVal='%s' Status='0'/>" %
                     (str(mete["mete_kind"]), mete["mete_id"], str(mete["value"]), str(mete["value"])))
        return data


class Reconnet(object):
    def send_heartbeat(self,client):
        #心跳
        xml = (
                "INFO zxvnms SIP/2.0"
                "CSeq: 0"
                "Call-ID: 123"
                "Content-Length: 0"
                "Content-Type: text/xml"
                "From: zxvnms2.0"
                "Max-Forwards: 70"
                "To: zxvnms3.0"
                "Via: longconnect_type"
                )
        client.send(xml.encode("utf8"))

    def reconnect(self,client,host,port):
        p = Protocl()
        while True :
            try :
                self.send_heartbeat(client)
                print('send data')
                print time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
                time.sleep(10) #如果想验证长时间没发数据，SOCKET连接会不会断开，则可以设置时间长一点
            except socket.error :
                print "\r\nsocket error,do reconnect "
                client = p.socket_Connect(host,port)
                p.register(client)
            except :
                print '\r\nother error occur '
                time.sleep(3)

if __name__ == '__main__':
    host = "10.45.152.138"
    port = 8081
    c = common.GetConfigInfo()
    fsu_code,mete_list = c.get_mete_data()
    p = Protocl()
    client = p.socket_Connect(host,port)
    p.register(client,fsu_code,mete_list)


