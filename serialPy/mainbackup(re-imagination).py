from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QByteArray, QItemSelectionModel, QModelIndex, QThread
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QFileDialog, QWidget, QLineEdit, QLCDNumber, QSpinBox, QDial,QAbstractItemView, QCheckBox

app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("SerialGUI")


f = open(r"C:\Users\vsask\Documents\Arduino\serialPy\10.04.22.txt", "rt")
mylist = f.read()
mylist = mylist.split('\n')
#def filebrowse():
#    filename=QFileDialog.getOpenFileName(self, "Open file", "C:\Users\vsask\Documents\Arduino\serialPy", "Text files (*.txt)")
#ui.browse.clicked.connect(ui.filebrowse)


class QLineEdit(QWidget):
    def __init__(self):
        super().__init__()
        ui.browse.clicked.connect(self.get_text_file)
    def get_text_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', r'C:\Users\vsask\Documents\Arduino\serialPy', 'Text files (*.txt)')
        if(file_name[0]!=''):
            ui.filename.setText(file_name[0])
            f = open(file_name[0], "rt")
            mylist = f.read()
            mylist = mylist.split('\n')
            name = []
            azimuth = []
            elevation = []
            date = []
            # так как основная информация о пролете спутника в орбитроне начинается с 12 строки,
            # пишем цикл
            for sat in range(12, len(mylist) - 2):
                temp = list(mylist[sat])  # разделяем строку на символы
                temp = temp[:51]  # удаляем ненужную информацию
                temp = ''.join(temp)
                temp = temp.replace("              ", ' ')
                if (temp != ''):
                    # парсим время пролета спутника
                    date_object = datetime.strptime(temp[:19], "%Y-%m-%d %H:%M:%S")
                    date.append(date_object)
                    # парсим название спутника
                    name.append(temp[20:27])
                    # парсим азимут
                    azimuth.append(float(temp[28:33]))
                    # парсим высоту
                    elevation.append(float(temp[34:38]))

            # выставляем количество столбцов и строк tablewidget'a
            #ui.tableSattels.setColumnCount(4)
            ui.tableSattels.setRowCount(len(name))
            # наименования столбцов
            ui.tableSattels.setHorizontalHeaderLabels(["Name", "Time", "Azimuth", "Elevation"])
            # инициализируем списки одноименных обьектов
            itemName = []
            itemDate = []
            itemAzimuth = []
            itemElevation = []
            #ui.tableSattels.closePersistentEditor(ui.tableSattels.item(0, 0))
            for index in range(len(name)):
                itemName.append(QTableWidgetItem(name[index]))
                itemDate.append(QTableWidgetItem(str(date[index])))
                itemAzimuth.append(QTableWidgetItem(str(azimuth[index])))
                itemElevation.append(QTableWidgetItem(str(elevation[index])))
                ui.tableSattels.setItem(index, 0, itemName[index])
                ui.tableSattels.setItem(index, 1, itemDate[index])
                ui.tableSattels.setItem(index, 2, itemAzimuth[index])
                ui.tableSattels.setItem(index, 3, itemElevation[index])

filename=QLineEdit()



# name=[]
# azimuth=[]
# elevation=[]
# date=[]
# #так как основная информация о пролете спутника в орбитроне начинается с 12 строки,
# #пишем цикл
# for sat in range(12, len(mylist)-2):
#     temp=list(mylist[sat]) #разделяем строку на символы
#     temp=temp[:51]         #удаляем ненужную информацию
#     temp = ''.join(temp)
#     temp=temp.replace("              ", ' ')
#     if(temp!=''):
#         # парсим время пролета спутника
#         date_object=datetime.strptime(temp[:19],"%Y-%m-%d %H:%M:%S")
#         date.append(date_object)
#         # парсим название спутника
#         name.append(temp[20:27])
#         # парсим азимут
#         azimuth.append(float(temp[28:33]))
#         #парсим высоту
#         elevation.append(float(temp[34:38]))
#
# #выставляем количество столбцов и строк tablewidget'a
# ui.tableSattels.setColumnCount(4)
# ui.tableSattels.setRowCount(len(name))
# #наименования столбцов
# ui.tableSattels.setHorizontalHeaderLabels(["Name","Time","Azimuth","Elevation"])
# #инициализируем списки одноименных обьектов
# itemName=[]
# itemDate=[]
# itemAzimuth=[]
# itemElevation=[]
# ui.tableSattels.closePersistentEditor(ui.tableSattels.item(0,0))
# for index in range(len(name)):
#     itemName.append(QTableWidgetItem(name[index]))
#     itemDate.append(QTableWidgetItem(str(date[index])))
#     itemAzimuth.append(QTableWidgetItem(str(azimuth[index])))
#     itemElevation.append(QTableWidgetItem(str(elevation[index])))
#     ui.tableSattels.setItem(index,0,itemName[index])
#     ui.tableSattels.setItem(index,1,itemDate[index])
#     ui.tableSattels.setItem(index,2,itemAzimuth[index])
#     ui.tableSattels.setItem(index,3,itemElevation[index])






serial = QSerialPort()
serial.setBaudRate(115200)#9600
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.comL.addItems(portList)



def onOpen():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)
def onClose():
    serial.close()

def onRead():
     coord = serial.readLine()
     coord=str(coord, "utf-8")
     coord = coord.split(";")
     ui.lcdNumber.display(coord[0])
     ui.lcdNumber_2.display(coord[1])

def elevIncr():
    serial.write('elevincr {}'.format(ui.spinBox.value()).encode())
def elevDecr():
    serial.write('elevdecr {}'.format(ui.spinBox.value()).encode())
def rotIncr():
    serial.write('rotaincr {}'.format(ui.spinBox.value()).encode())
def rotDecr():
    serial.write('rotadecr {}'.format(ui.spinBox.value()).encode())

serial.readyRead.connect(onRead)
model = QItemSelectionModel
model = ui.tableSattels.selectionModel()
def selRows():
    selectedrows=model.selectedRows()
    ui.tableSelectedSattels.setRowCount(len(selectedrows))
    if (bool(selectedrows)==True):
        for row in range(len(selectedrows)):
            #Третьим параметром приводим к типу QTableWidgetItem
            #Перекидываем все выделенные спутники во второй tableWidget
            ui.tableSelectedSattels.setItem(row, 0, QTableWidgetItem(ui.tableSattels.item(selectedrows[row].row(), 0).text()))
            ui.tableSelectedSattels.setItem(row, 1, QTableWidgetItem(ui.tableSattels.item(selectedrows[row].row(), 1).text()))
            ui.tableSelectedSattels.setItem(row, 2, QTableWidgetItem(ui.tableSattels.item(selectedrows[row].row(), 2).text()))
            ui.tableSelectedSattels.setItem(row, 3, QTableWidgetItem(ui.tableSattels.item(selectedrows[row].row(), 3).text()))
#from threading import Timer
from threading import Thread
import time

list_azimIncrement = []
list_azimIterations = []
list_elevIncrement = []
list_elevIterations = []
list_timeDelta = []

# def zero():
#     serial.write('elevdecr {}'.format(int(ui.lcdNumber_2.value())).encode())
#     time.sleep(5)
#     serial.write('rotadecr {}'.format(int(ui.lcdNumber.value())).encode())
currentSatell = 0
def Tracking():
    print(serial.bytesToWrite())
    rowcount = ui.tableSelectedSattels.rowCount()
    temp = []
    for j1 in range(rowcount):
            temp.append(datetime.strptime(ui.tableSelectedSattels.item(j1, 1).text(), "%Y-%m-%d %H:%M:%S"))
    while (ui.checkBox.isChecked() == True):  # пока нажата кнопка начать отслеживание,
        for currentSatell in range(rowcount):
            date_object = datetime.strptime(ui.tableSelectedSattels.item(currentSatell, 1).text(), "%Y-%m-%d %H:%M:%S")
            datenow = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            if(date_object==datenow):
                print(True)
                TrackMove(currentSatell)

                #print('in Tracking',serial.bytesToWrite())
                #th2 = Thread(target=TrackMove, daemon=True)
                #th2.start()
                #serial.write('elevincr {}'.format(int(float(ui.tableSelectedSattels.item(0,2).text()))).encode())
                #time.sleep(10)
                #serial.write('rotaincr {}'.format(int(float(ui.tableSelectedSattels.item(0,3).text()))).encode())
        time.sleep(1)
        print("check")
    return


# def Tracking():
#     #выставляем антенну на ноль, т.к возможна ситуация, когда мы повторно начинаем отслеживание
#     serial.write('elevdecr {}'.format(int(ui.lcdNumber_2.value())).encode())
#     #time.sleep(5)
#     #serial.write('rotadecr {}'.format(int(ui.lcdNumber.value())).encode())
#
#     rowcount = ui.tableSelectedSattels.rowCount()
#     temp = []
#     for j1 in range(rowcount):
#         temp.append(datetime.strptime(ui.tableSelectedSattels.item(j1, 1).text(), "%Y-%m-%d %H:%M:%S"))
#     list_azimIncrement = []
#     list_azimIterations = []
#     list_elevIncrement = []
#     list_elevIterations = []
#     list_timeDelta = []
#     for j1 in range(rowcount-1):
#         timeDelta = int(abs((temp[j1+1] - temp[j1]).total_seconds()))
#         azimDelta = abs(int(float(ui.tableSelectedSattels.item(j1+1,2).text()))-int(float(ui.tableSelectedSattels.item(j1,2).text())))
#         elevDelta = abs(int(float(ui.tableSelectedSattels.item(j1+1,3).text()))-int(float(ui.tableSelectedSattels.item(j1,3).text())))
#         if(azimDelta==0 or azimDelta<timeDelta):
#             azimIterations = 1
#             azimIncrement = azimDelta
#         else:
#             azimIterations = int(int(azimDelta)/int(azimDelta/timeDelta))
#             azimIncrement = int(azimDelta/timeDelta)
#         if(elevDelta==0 or elevDelta<timeDelta):
#             elevIterations = 1
#             elevIncrement = elevDelta
#         else:
#             elevIterations = int(int(elevDelta)/int(elevDelta/timeDelta))
#             elevIncrement = int(elevDelta/timeDelta)
#
#         list_azimIncrement.append(azimIncrement)
#         list_azimIterations.append(azimIterations)
#         list_elevIncrement.append(elevIncrement)
#         list_elevIterations.append(elevIterations)
#         list_timeDelta.append(timeDelta)
#     #print(list_elevIncrement, list_elevIterations, list_azimIncrement, list_azimIterations, list_timeDelta)
#     #двигаем антенну на первое прохождение
#     while(ui.checkBox.isChecked()==True):             #пока нажата кнопка начать отслеживание,
#         date_object = datetime.strptime(ui.tableSelectedSattels.item(0, 1).text(), "%Y-%m-%d %H:%M:%S")
#         datenow = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
#         if(date_object==datenow):
#             serial.write('elevincr {}'.format(int(float(ui.tableSelectedSattels.item(0,2).text()))).encode())
#             time.sleep(10)
#             serial.write('rotaincr {}'.format(int(float(ui.tableSelectedSattels.item(0,3).text()))).encode())
#             break
#         time.sleep(1)
#     return
# def TrackingElev():
#     time.sleep(10)
#     while (ui.checkBox.isChecked() == True):
#         for t1 in range(len(list_timeDelta)):
#             for t2 in range(list_elevIterations[t1]):
#                 time.sleep(int(list_timeDelta[t1]/list_elevIterations[t2]))
#                 if(int(ui.lcdNumber_2.value())<int(float(ui.tableSelectedSattels.item(t1+1,3).text()))):
#                     serial.write('elevincr {}'.format(list_elevIncrement[t1]).encode())
#                     ui.lcdNumber_2.display(int(ui.lcdNumber_2.value())+list_elevIncrement[t1])
#                 else:
#                     serial.write('elevdecr {}'.format(list_elevIncrement[t1]).encode())
#                     ui.lcdNumber_2.display(int(ui.lcdNumber_2.value()) - list_elevIncrement[t1])
#
#     return
# def TrackingRot():
#     time.sleep(10)
#     while (ui.checkBox.isChecked() == True):
#         for t1 in range(len(list_timeDelta)):
#             for t2 in range(list_azimIterations[t1]):
#                 time.sleep(int(list_timeDelta[t1]/list_azimIterations[t2]))
#                 if(int(ui.lcdNumber.value())<int(float(ui.tableSelectedSattels.item(t1+1,2).text()))):
#                     serial.write('rotaincr {}'.format(list_azimIncrement[t1]).encode())
#                     ui.lcdNumber.display(int(ui.lcdNumber.value())+list_azimIncrement[t1])
#                 else:
#                     serial.write('rotadecr {}'.format(list_azimIncrement[t1]).encode())
#                     ui.lcdNumber.display(int(ui.lcdNumber.value()) - list_azimIncrement[t1])
#     return

def TrackMove(par):
    azim = int(float(ui.tableSelectedSattels.item(par, 2).text()))
    elev = int(float(ui.tableSelectedSattels.item(par, 3).text()))

    if(ui.lcdNumber.value()< azim):
        serial.write('rotaincr {}'.format(azim-ui.lcdNumber.value()).encode())
        serial.flush()
        time.sleep((azim-ui.lcdNumber.value())/3.6)
        ui.lcdNumber.display(azim)
    elif(ui.lcdNumber.value() > azim):
        serial.write('rotadecr {}'.format(ui.lcdNumber.value()-azim).encode())
        serial.flush()
        time.sleep((ui.lcdNumber.value()-azim)/3.6)
        ui.lcdNumber.display(azim)
    #serial.flush()
    #time.sleep()
    serial.close()
    time.sleep(3)
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)
    time.sleep(3)
    if (ui.lcdNumber_2.value() < elev):
        serial.write('elevincr {}'.format(elev-ui.lcdNumber_2.value()).encode())
        serial.flush()
        time.sleep((elev-ui.lcdNumber_2.value())/1.8)
        ui.lcdNumber_2.display(elev)
    elif (ui.lcdNumber_2.value() > elev):
        serial.write('elevdecr {}'.format(ui.lcdNumber_2.value()-elev).encode())
        serial.flush()
        time.sleep((ui.lcdNumber_2.value()-elev)/1.8)
        ui.lcdNumber_2.display(elev)
    serial.flush()
    time.sleep(2)
    serial.close()
    time.sleep(2)
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)






def startTracking():
    if(ui.checkBox.isChecked()==True):
        th1 = Thread(target=Tracking, daemon=True)
        #th2 = Thread(target=TrackMove, daemon=True)
        #th3 = Thread(target=TrackingRot, daemon=True)
        th1.start()

        #th3.start()


    #temp = datetime.strptime(ui.tableSelectedSattels.item(0,1).text(), "%Y-%m-%d %H:%M:%S")
    #if ui.checkBox.checkState()==2:
        #(temp - datetime.today() < datetime.strptime("00:00:03", "%H:%M:%S")
    #schedule.every(5).seconds.do(print(True))







ui.tableSattels.setColumnCount(4)
ui.tableSattels.setHorizontalHeaderLabels(["Name", "Time", "Azimuth", "Elevation"])
ui.tableSelectedSattels.setColumnCount(4)
ui.tableSelectedSattels.setHorizontalHeaderLabels(["Name", "Time", "Azimuth", "Elevation"])





#ui.setZero.clicked.connect(zero)
ui.checkBox.stateChanged.connect(startTracking)
ui.pushButton.clicked.connect(selRows)
ui.elevIncrease.clicked.connect(elevIncr)
ui.elevDecrease.clicked.connect(elevDecr)
ui.rotIncrease.clicked.connect(rotIncr)
ui.rotDecrease.clicked.connect(rotDecr)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)


ui.show()
app.exec()