from functools import partial
from sys import argv,exit
from os import sep, getcwd, chdir, listdir, walk, path
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication

from ProgramFile.FileRenamerQT import Ui_MainWindow

# Handle high resolution displays:
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class FileRenamer(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.comboBox.setCurrentText(getcwd())

        # region Original Hiding
        self.progressBar.setVisible(False)
        self.Label_Progress_text.setVisible(False)
        self.Label_Progress_Done_text.setVisible(False)

        self.Label_Number.setVisible(False)
        self.Label_Number_text.setVisible(False)

        # endregion

        # region Icon
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("." + sep + "film.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        # MainWindow.setWindowIcon(icon)
        # endregion

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)
        # _translate = QtCore.QCoreApplication.translate

    def First(self):
        self.ExceptFiles = []

    # region Buttons
    def ButtonOpen(self):
        file_path = ""
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = filedialog.askdirectory(title="Select Directory",initialdir="./")
        self.comboBox.setStyleSheet("color:yellow;")
        self.comboBox.setCurrentText(file_path.replace("/",sep).replace("\\",sep))
        self.comboBox.addItem(file_path.replace("/",sep).replace("\\",sep))

    def ButtonRename(self):
        pass

    def ButtonCancel(self):
        pass

    def ButtonReset(self):
        pass

    def ButtonPreview(self):
        FileLoc = self.comboBox.currentText()
        Files = []

        Except = self.lineEdit_Except.displayText().replace(" , ",",").replace(" ,",",").replace(", ","")
        if "," not in Except:
            Except += ","
        ExceptList = Except.split(",")

        try:
            self.comboBox.setStyleSheet("color:yellow;")
            chdir(FileLoc)
            countnew = True
        except OSError:
            self.comboBox.setStyleSheet("color:red")
            self.comboBox.setCurrentText("There is no such a directory")
            countnew = False

        # region Shows
        self.Label_Number.setVisible(True)
        self.Label_Number_text.setVisible(True)
        # endregion

        # Files:
        counter = 0
        for (dirpath, dirnames, filenames) in walk(FileLoc):
            for filename in filenames:
                QApplication.processEvents()
                if filename not in Except:
                    absulpathR = path.abspath(sep.join([dirpath, filename]))
                    Files.append(absulpathR)
                    counter += 1
                    self.Label_Number.setText(str(counter))

        if countnew:

            if self.tab_Delete.isActiveWindow():
                # common pattern:
                if self.lineEdit_Common.displayText() == "":
                    FilesR = Files
                else:
                    if self.checkBox_Ex.isChecked():
                        FilesR = [i for i in Files if "."+self.lineEdit_Common.displayText() in i[i.rfind(sep):].replace(sep,"")]
                    else:
                        FilesR = [i for i in Files if self.lineEdit_Common.displayText() in i[i.rfind(sep):].replace(sep,"")]

                if FilesR != []:
                    if self.checkBox_Select.isChecked():
                        From = self.lineEdit_From.displayText() if self.lineEdit_From.displayText() != "" else ""
                        To = self.lineEdit_To.displayText() if self.lineEdit_To.displayText() != "" else ""

                        name = FilesR[0][FilesR[0].rfind(sep):].replace(sep,"")

                        if self.checkBox_From.isChecked():
                            if self.checkBox_To.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)]+To
                            else:
                                delete = name[name.rfind(From):name.rfind(To)]
                        else:
                            if self.checkBox_To.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "")+(To)
                            else:
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "")

                        self.lineEdit_Preview_R.setText(FilesR[0][FilesR[0].rfind(sep):].replace(delete,"").replace(sep,""))

                    else:
                        delete = self.lineEdit_Delete.displayText()
                        self.lineEdit_Preview_R.setText(FilesR[0][FilesR[0].rfind(sep):].replace(delete,"").replace(sep,""))

                else:
                    self.lineEdit_Preview_O.setText("There is no file with this pattern.")
                    self.lineEdit_Preview_R.setText("")

            if self.tab_rename.isActiveWindow():
                # common pattern:
                if self.lineEdit_Common_2.displayText() == "":
                    FilesR = Files
                else:
                    if self.checkBox_Ex_2.isChecked():
                        FilesR = [i for i in Files if
                                  "." + self.lineEdit_Common_2.displayText() in i[i.rfind(sep):].replace(sep, "")]
                    else:
                        FilesR = [i for i in Files if self.lineEdit_Common_2.displayText() in i[i.rfind(sep):].replace(sep, "")]

                if FilesR != []:
                    if self.checkBox_Select_2.isChecked():
                        From = self.lineEdit_From_2.displayText() if self.lineEdit_From_2.displayText() != "" else ""
                        To = self.lineEdit_To_2.displayText() if self.lineEdit_To_2.displayText() != "" else ""

                        name = FilesR[0][FilesR[0].rfind(sep):].replace(sep, "")

                        if self.checkBox_From_2.isChecked():
                            if self.checkBox_To_2.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)] + To
                            else:
                                delete = name[name.rfind(From):name.rfind(To)]
                        else:
                            if self.checkBox_To_2.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "") + (To)
                            else:
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "")

                        re_from = delete

                    else:
                        re_from = self.lineEdit_Rename_From.displayText()
                    re_to = self.lineEdit_Rename_To.displayText()
                    self.lineEdit_Preview_R.setText(FilesR[0][FilesR[0].rfind(sep):].replace(re_from, re_to).replace(sep, ""))

                else:
                    self.lineEdit_Preview_O.setText("There is no file with this pattern.")
                    self.lineEdit_Preview_R.setText("")

            if self.tab_sufix.isActiveWindow():
                # common pattern:
                if self.lineEdit_Common_3.displayText() == "":
                    FilesR = Files
                else:
                    if self.checkBox_Ex_3.isChecked():
                        FilesR = [i for i in Files if "." + self.lineEdit_Common_3.displayText() in i[i.rfind(sep):].replace(sep, "")]
                    else:
                        FilesR = [i for i in Files if self.lineEdit_Common_3.displayText() in i[i.rfind(sep):].replace(sep, "")]

                if FilesR != []:
                    name = FilesR[0][FilesR[0].rfind(sep):].replace(sep, "")
                    typename = name[name.rfind("." ,len(name ) -5):].replace("." ,"")

                    prefix = self.lineEdit_addPre.displayText()
                    suffix = self.lineEdit_addSuf.displayText()

                    self.lineEdit_Preview_R.setText(prefix + name[:name.rfind(".",len(name)-5)].replace(".","") +
                                                suffix +"."+ typename)
                else:
                    self.lineEdit_Preview_O.setText("There is no file with this pattern.")
                    self.lineEdit_Preview_R.setText("")


            if self.tab_mixed.isActiveWindow():
                pass
            if self.tab_advanced.isActiveWindow():
                pass

            if FilesR != []:
                self.lineEdit_Preview_O.setText(FilesR[0][FilesR[0].rfind(sep):].replace(sep, ""))
    def ButtonHelp(self):
        pass

    # endregion

    def SelectFiles(self,mode):
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = list(filedialog.askopenfilenames(initialdir="./", title="Select except files"))
        file = [i[i.rfind("/"):].replace("/","") for i in file_path]

        if mode == "deleter":
            self.lineEdit_Except.setText(str(file).replace("\"","").replace("[","").replace("]",""))

        if mode == "renamer":
            self.lineEdit_Except_2.setText(str(file).replace("\"","").replace("[","").replace("]",""))

        if mode == "suffix":
            self.lineEdit_Except_3.setText(str(file).replace("\"", "").replace("[", "").replace("]", ""))

        if mode == "mixed":
            self.lineEdit_Except_4.setText(str(file).replace("\"", "").replace("[", "").replace("]", ""))

        if mode == "advance":
            self.lineEdit_Except_5.setText(str(file).replace("\"", "").replace("[", "").replace("]", ""))

    # region Select Character - Checkbox
    def Checker(self,mode):
        if mode == "deleter":
            if self.checkBox_Select.isChecked():
                self.lineEdit_Delete.setEnabled(False)
                self.lineEdit_Delete.setStyleSheet("background-color:#3C3F41")
                self.Label_Delete.setStyleSheet("color:#9D7C47")

                self.lineEdit_From.setDisabled(False)
                self.lineEdit_From.setStyleSheet("background-color:#606365")
                self.lineEdit_To.setDisabled(False)
                self.lineEdit_To.setStyleSheet("background-color:#606365")
                self.checkBox_From.setDisabled(False)
                self.checkBox_To.setDisabled(False)

                self.Label_From.setStyleSheet("color:#D9AC63")
                self.Label_To.setStyleSheet("color:#D9AC63")

            else:
                self.lineEdit_Delete.setEnabled(True)
                self.lineEdit_Delete.setStyleSheet("background-color:#606365")
                self.Label_Delete.setStyleSheet("color:#D9AC63")

                self.lineEdit_From.setDisabled(True)
                self.lineEdit_From.setStyleSheet("background-color:#3C3F41")
                self.lineEdit_To.setDisabled(True)
                self.lineEdit_To.setStyleSheet("background-color:#3C3F41")
                self.checkBox_From.setDisabled(True)
                self.checkBox_To.setDisabled(True)

                self.Label_From.setStyleSheet("color:#9D7C47")
                self.Label_To.setStyleSheet("color:#9D7C47")

        if mode == "renamer":
            if self.checkBox_Select_2.isChecked():
                self.lineEdit_Rename_From.setEnabled(False)
                self.lineEdit_Rename_From.setStyleSheet("background-color:#3C3F41")

                self.lineEdit_From_2.setDisabled(False)
                self.lineEdit_From_2.setStyleSheet("background-color:#606365")
                self.lineEdit_To_2.setDisabled(False)
                self.lineEdit_To_2.setStyleSheet("background-color:#606365")
                self.checkBox_From_2.setDisabled(False)
                self.checkBox_To_2.setDisabled(False)

                self.Label_From_2.setStyleSheet("color:#D9AC63")
                self.Label_To2.setStyleSheet("color:#D9AC63")

            else:
                self.lineEdit_Rename_From.setEnabled(True)
                self.lineEdit_Rename_From.setStyleSheet("background-color:#606365")

                self.lineEdit_From_2.setDisabled(True)
                self.lineEdit_From_2.setStyleSheet("background-color:#3C3F41")
                self.lineEdit_To_2.setDisabled(True)
                self.lineEdit_To_2.setStyleSheet("background-color:#3C3F41")
                self.checkBox_From_2.setDisabled(True)
                self.checkBox_To_2.setDisabled(True)

                self.Label_From_2.setStyleSheet("color:#9D7C47")
                self.Label_To2.setStyleSheet("color:#9D7C47")

        if mode == "mixed":
            if self.checkBox_Select_3.isChecked():
                self.lineEdit_Rename_From_2.setEnabled(False)
                self.lineEdit_Rename_From_2.setStyleSheet("background-color:#3C3F41")

                self.lineEdit_From_3.setDisabled(False)
                self.lineEdit_From_3.setStyleSheet("background-color:#606365")
                self.lineEdit_To_3.setDisabled(False)
                self.lineEdit_To_3.setStyleSheet("background-color:#606365")
                self.checkBox_From_3.setDisabled(False)
                self.checkBox_To_3.setDisabled(False)

                self.Label_From_3.setStyleSheet("color:#D9AC63")
                self.Label_To3.setStyleSheet("color:#D9AC63")

            else:
                self.lineEdit_Rename_From_2.setEnabled(True)
                self.lineEdit_Rename_From_2.setStyleSheet("background-color:#606365")

                self.lineEdit_From_3.setDisabled(True)
                self.lineEdit_From_3.setStyleSheet("background-color:#3C3F41")
                self.lineEdit_To_3.setDisabled(True)
                self.lineEdit_To_3.setStyleSheet("background-color:#3C3F41")
                self.checkBox_From_3.setDisabled(True)
                self.checkBox_To_3.setDisabled(True)

                self.Label_From_3.setStyleSheet("color:#9D7C47")
                self.Label_To3.setStyleSheet("color:#9D7C47")
    # endregion

if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    MainWindow = QtWidgets.QMainWindow()


    ui =FileRenamer()
    ui.setupUi(MainWindow)
    ui.First()

    # region Main Buttons
    ui.Button_open.clicked.connect(ui.ButtonOpen)
    ui.Button_Rename.clicked.connect(ui.ButtonRename)
    ui.Button_preview.clicked.connect(ui.ButtonPreview)
    ui.Button_reset.clicked.connect(ui.ButtonReset)
    ui.Button_stop.clicked.connect(ui.ButtonCancel)
    ui.Button_help.clicked.connect(ui.ButtonHelp)
    # endregion
    # region Buttons
    ui.Button_open_EX.clicked.connect(partial(ui.SelectFiles,"deleter"))
    ui.Button_open_EX_2.clicked.connect(partial(ui.SelectFiles,"renamer"))
    ui.Button_open_EX_3.clicked.connect(partial(ui.SelectFiles,"suffix"))
    ui.Button_open_EX_4.clicked.connect(partial(ui.SelectFiles,"mixed"))
    ui.Button_open_EX_5.clicked.connect(partial(ui.SelectFiles,"advance"))
    # endregion
    #region CheckBoxes
    ui.checkBox_Select.clicked.connect(partial(ui.Checker,"deleter"))
    ui.checkBox_Select_2.clicked.connect(partial(ui.Checker,"renamer"))
    ui.checkBox_Select_3.clicked.connect(partial(ui.Checker,"mixed"))
    # endregion


    MainWindow.show()
    exit(app.exec_())

