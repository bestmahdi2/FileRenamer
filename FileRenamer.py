import time
from functools import partial
from sys import argv, exit
from os import sep, getcwd, chdir, walk, path, rename
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

        self.checkBox_paste_beg.setChecked(True)
        self.comboBox.setCurrentText(getcwd())

        # region Original Hiding
        self.progressBar.setVisible(False)
        self.Label_Progress_text.setVisible(False)
        self.Label_Progress_Done_text.setVisible(False)

        self.Label_Number.setVisible(False)
        self.Label_Number_2.setVisible(False)
        self.Label_Number_text.setVisible(False)
        # endregion

        # region icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("." + sep + "edit.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        # endregion

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)
        # _translate = QtCore.QCoreApplication.translate

    def First(self):
        self.ExceptFiles = []
        self.cancel = False  # for clicking on the cancel button

    # region Buttons
    def ButtonOpen(self):
        file_path = ""
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = filedialog.askdirectory(title="Select Directory", initialdir="./")
        self.comboBox.setStyleSheet("color:yellow;")
        self.comboBox.setCurrentText(file_path.replace("/", sep).replace("\\", sep))
        self.comboBox.addItem(file_path.replace("/", sep).replace("\\", sep))

    def ButtonRename(self):
        self.filetype = ""
        self.Error.setText("")
        self.cancel = False
        FileLoc = self.comboBox.currentText()
        Files = []

        # region Except Files
        Except = self.lineEdit_Except.displayText().replace(" , ", ",").replace(" ,", ",").replace(", ", ",").replace(
            "\"", "").replace("\'", "")
        # endregion

        if "," not in Except:
            Except += ","
        ExceptList = Except.split(",")
        print(ExceptList)

        try:
            self.comboBox.setStyleSheet("color:yellow;")
            chdir(FileLoc)
            DirExist = True
        except OSError:
            self.comboBox.setStyleSheet("color:red")
            self.comboBox.setCurrentText("There is no such a directory")
            DirExist = False

        # region Shows
        self.Label_Number.setVisible(True)
        self.Label_Number_2.setVisible(True)
        self.Label_Number_text.setVisible(True)
        self.Label_Progress_text.setVisible(True)
        self.progressBar.setVisible(True)
        self.Label_Progress_Done_text.setVisible(False)
        # endregion

        # region Files:
        counter = 0
        for (dirpath, dirnames, filenames) in walk(FileLoc):
            for filename in filenames:
                QApplication.processEvents()
                if filename not in ExceptList:
                    absulpathR = path.abspath(sep.join([dirpath, filename]))
                    Files.append(absulpathR)
                counter += 1
                self.Label_Number.setText(str(counter))
        # endregion

        # region common pattern:
        if self.lineEdit_Common.displayText() == "":
            FilesR = Files
        else:
            if self.checkBox_Ex.isChecked():
                FilesR = [i for i in Files if
                          "." + self.lineEdit_Common.displayText() in i[i.rfind(sep):].replace(sep, "")]
            else:
                FilesR = [i for i in Files if self.lineEdit_Common.displayText() in i[i.rfind(sep):].replace(sep, "")]
            # endregion

        self.progressBar.setMaximum(len(FilesR))

        # region tabs
        if DirExist:
            self.Label_Number_2.setText(str(len(FilesR)))

            if FilesR:
                if self.tabWidget.currentIndex() == 0:  # tab_Delete
                    name = FilesR[0][FilesR[0].rfind(sep):].replace(sep, "")

                    if self.checkBox_Select.isChecked():
                        From = self.lineEdit_From.displayText() if self.lineEdit_From.displayText() != "" else name[0]
                        To = self.lineEdit_To.displayText() if self.lineEdit_To.displayText() != "" else name[-1]

                        if self.checkBox_From.isChecked():
                            if self.checkBox_To.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)] + To
                            else:
                                delete = name[name.rfind(From):name.rfind(To)]
                        else:
                            if self.checkBox_To.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "") + (To)
                            else:
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "")

                    else:
                        delete = self.lineEdit_Delete.displayText()

                    progress = 0
                    for file in FilesR:
                        QtWidgets.QApplication.processEvents()
                        nameOld = file[file.rfind(sep):].replace(sep, "")
                        nameNew = nameOld.replace(delete, "")
                        progress += 1
                        # print(nameOld +"  "+ nameNew)
                        if not self.cancel:
                            try:
                                rename(file, file.replace(nameOld, nameNew))
                            except FileExistsError:
                                self.Error.setText("Be sure about the files not being used by another program")
                            except OSError:
                                self.Error.setText("Be sure about the files not being used by another program")

                            self.progressBar.setProperty("value", progress)
                        else:
                            break

                        time.sleep(0.5)

                    self.Label_Progress_Done_text.setVisible(True)

                if self.tabWidget.currentIndex() == 1:  # tab_rename

                    if self.checkBox_Select_2.isChecked():
                        name = FilesR[0][FilesR[0].rfind(sep):].replace(sep, "")

                        From = self.lineEdit_From_2.displayText() if self.lineEdit_From_2.displayText() != "" else name[
                            0]
                        To = self.lineEdit_To_2.displayText() if self.lineEdit_To_2.displayText() != "" else name[-1]

                        if self.checkBox_From_2.isChecked():
                            if self.checkBox_To_2.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)] + To
                            else:
                                delete = name[name.rfind(From):name.rfind(To)]
                        else:
                            if self.checkBox_To_2.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "") + To
                            else:
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "")

                        re_from = delete

                    else:
                        re_from = self.lineEdit_Rename_From.displayText()

                    re_to = self.lineEdit_Rename_To.displayText()

                    progress = 0
                    for file in FilesR:
                        QtWidgets.QApplication.processEvents()
                        name = file[file.rfind(sep):].replace(sep, "")
                        delete = name.replace(re_from, re_to)
                        progress += 1

                        if not self.cancel:
                            try:
                                rename(file, file.replace(name, delete))
                            except FileExistsError:
                                self.Error.setText("Be sure about patterns and files.")
                            except OSError:
                                self.Error.setText("Be sure about the files not being used by another program")
                            # except :
                            #     self.Error.setText("Be sure about patterns and files.")

                            self.progressBar.setProperty("value", progress)
                        else:
                            break

                        time.sleep(0.5)

                    self.Label_Progress_Done_text.setVisible(True)

                if self.tabWidget.currentIndex() == 2:  # tab_sufix

                    prefix = self.lineEdit_addPre.displayText()
                    suffix = self.lineEdit_addSuf.displayText()

                    progress = 0
                    for file in FilesR:
                        QtWidgets.QApplication.processEvents()
                        progress += 1

                        name = file[file.rfind(sep):].replace(sep, "")

                        if self.filetype == "":
                            typename = "." + name[name.rfind(".", len(name) - 5):].replace(".", "")
                        else:
                            typename = self.filetype

                        to_name = prefix + name[:name.rfind(typename)].replace(".", "") + suffix + typename
                        if not self.cancel:
                            try:
                                rename(file, file.replace(name, "") + to_name)
                            except FileExistsError:
                                self.Error.setText("Be sure about patterns and files.")
                            except OSError:
                                self.Error.setText("Be sure about the files not being used by another program")
                            self.progressBar.setProperty("value", progress)
                        else:
                            break

                        time.sleep(0.5)

                    self.Label_Progress_Done_text.setVisible(True)

                if self.tabWidget.currentIndex() == 3:  # tab_mixed

                    # region Pre-Suffix
                    prefix = self.lineEdit_addPre_2.displayText()
                    suffix = self.lineEdit_addSuf_2.displayText()
                    # endregion

                    # print(FilesR)

                    progress = 0
                    for file in FilesR:
                        QtWidgets.QApplication.processEvents()
                        name = file[file.rfind(sep):].replace(sep, "")
                        if self.filetype == "":
                            typename = "." + name[name.rfind(".", len(name) - 5):].replace(".", "")
                        else:
                            typename = self.filetype
                        progress += 1

                        # region Rename
                        if self.checkBox_Select_3.isChecked():
                            From = self.lineEdit_From_3.displayText() if self.lineEdit_From_3.displayText() != "" else \
                                name[0]
                            To = self.lineEdit_To_3.displayText() if self.lineEdit_To_3.displayText() != "" else \
                                name[-1]

                            if self.checkBox_From_3.isChecked():
                                if self.checkBox_To_3.isChecked():
                                    delete = name[name.rfind(From):name.rfind(To)] + To
                                else:
                                    delete = name[name.rfind(From):name.rfind(To)]
                            else:
                                if self.checkBox_To_3.isChecked():
                                    delete = name[name.rfind(From):name.rfind(To)].replace(From, "") + (To)
                                else:
                                    delete = name[name.rfind(From):name.rfind(To)].replace(From, "")

                            re_from = delete

                        else:
                            re_from = self.lineEdit_Rename_From_2.displayText()
                        re_to = self.lineEdit_Rename_To_2.displayText()
                        # endregion

                        if not self.cancel:
                            try:
                                to_name = prefix + name[:name.rfind(typename)].replace(".", "").replace(re_from,
                                                                                                        re_to).replace(
                                    sep, "") + suffix + typename

                                rename(file, file.replace(name, "") + to_name)
                            except FileExistsError:
                                self.Error.setText("Be sure about patterns and files.")
                            except OSError:
                                self.Error.setText("Be sure about the files not being used by another program")
                            except:
                                self.Error.setText("Be sure about using both Rename and Prefix/Suffix together.")

                            self.progressBar.setProperty("value", progress)
                        else:
                            break
                        time.sleep(0.5)

                    self.Label_Progress_Done_text.setVisible(True)

                if self.tabWidget.currentIndex() == 4:  # tab_advanced

                    continue_1 = True
                    continue_2 = True
                    prefix = self.lineEdit_addPre_3.displayText()
                    suffix = self.lineEdit_addSuf_3.displayText()

                    progress = 0
                    for file in FilesR:
                        QtWidgets.QApplication.processEvents()
                        name = file[file.rfind(sep):].replace(sep, "")
                        if self.filetype == "":
                            typename = "." + name[name.rfind(".", len(name) - 5):].replace(".", "")
                        else:
                            typename = self.filetype
                        progress += 1

                        From = self.lineEdit_From_4.displayText() if self.lineEdit_From_4.displayText() != "" else name[
                            0]
                        To = self.lineEdit_To_4.displayText() if self.lineEdit_To_4.displayText() != "" else name[-1]

                        if From not in file:
                            self.Error.setText("\"From\" part is incorrect")
                            continue_1 = False
                        if To not in file:
                            self.Error.setText("\"To\" part is incorrect")
                            continue_1 = False

                        if self.checkBox_From_4.isChecked():
                            if self.checkBox_To_4.isChecked():
                                select = name[name.rfind(From):name.rfind(To)] + To
                            else:
                                select = name[name.rfind(From):name.rfind(To)]
                        else:
                            if self.checkBox_To_4.isChecked():
                                select = name[name.rfind(From):name.rfind(To)].replace(From, "") + (To)
                            else:
                                select = name[name.rfind(From):name.rfind(To)].replace(From, "")

                        name_ = name.replace(select, "")

                        delete = self.lineEdit_Del_char_From_Sel.displayText()

                        if delete in select:
                            continue_2 = True

                        else:
                            continue_2 = False
                            self.Error.setText("The \"Delete\" part is not in the \"Selected\" part.")

                        if continue_1 is True and continue_2 is True:

                            select = select.replace(delete, "")

                            FinSelect = str(prefix + select + suffix)

                            # print(suffix , prefix , From , To , select , name , name_ , delete, FinSelect , sep=", " )

                            if self.cancel != True:
                                try:
                                    if self.checkBox_paste_beg.isChecked():
                                        rename(file, file.replace(name, "") + FinSelect + name_)

                                    else:
                                        to_name = name_[:name_.rfind(typename)].replace(".", "") + FinSelect + typename
                                        rename(file, file.replace(name, "") + to_name)

                                except FileExistsError:
                                    self.Error.setText("Be sure about patterns and files.")

                                except OSError:
                                    self.Error.setText("Be sure about the files not being used by another program")

                                self.progressBar.setProperty("value", progress)

                            else:
                                break
                            time.sleep(0.5)
                            self.Label_Progress_Done_text.setVisible(True)

                        else:
                            break

            else:
                self.Error.setText("There is no file with this pattern.")
                self.lineEdit_Preview_R.setText("")

            if FilesR:
                self.lineEdit_Preview_O.setText(FilesR[0][FilesR[0].rfind(sep):].replace(sep, ""))

        # endregion

    def ButtonCancel(self):
        self.progressBar.setProperty("value", 0)
        self.Error.setText("The Operation Canceled")
        self.cancel = True

    def ButtonReset(self):
        self.lineEdit_Preview_R.setText("")
        self.lineEdit_Preview_O.setText("")
        self.lineEdit_Except.setText("")
        self.lineEdit_Common.setText("")
        self.lineEdit_Delete.setText("")
        self.lineEdit_Del_char_From_Sel.setText("")
        self.lineEdit_To.setText("")
        self.lineEdit_To_2.setText("")
        self.lineEdit_To_3.setText("")
        self.lineEdit_To_4.setText("")
        self.lineEdit_From.setText("")
        self.lineEdit_From_2.setText("")
        self.lineEdit_From_3.setText("")
        self.lineEdit_From_4.setText("")
        self.lineEdit_addPre.setText("")
        self.lineEdit_addPre_2.setText("")
        self.lineEdit_addPre_3.setText("")
        self.lineEdit_addSuf.setText("")
        self.lineEdit_addSuf_2.setText("")
        self.lineEdit_addSuf_3.setText("")
        self.lineEdit_Rename_To.setText("")
        self.lineEdit_Rename_To_2.setText("")
        self.lineEdit_Rename_From.setText("")
        self.lineEdit_Rename_From_2.setText("")

        self.Label_Number.setText("")
        self.Label_Number_2.setText("")
        self.Label_Number_text.setVisible(False)
        self.Label_Progress_Done_text.setVisible(False)
        self.Label_Progress_text.setVisible(False)
        self.Error.setText("")

        self.progressBar.setVisible(False)

        self.checkBox_Select.setChecked(False)
        self.checkBox_Select_2.setChecked(False)
        self.checkBox_Select_3.setChecked(False)
        self.checkBox_From.setChecked(False)
        self.checkBox_From_2.setChecked(False)
        self.checkBox_From_3.setChecked(False)
        self.checkBox_From_4.setChecked(False)
        self.checkBox_To.setChecked(False)
        self.checkBox_To_2.setChecked(False)
        self.checkBox_To_3.setChecked(False)
        self.checkBox_To_4.setChecked(False)
        self.checkBox_Ex.setChecked(False)
        self.checkBox_paste_beg.setChecked(True)

        self.Checker("deleter")
        self.Checker("renamer")
        self.Checker("mixed")
        self.Checker("advanceB")



    def ButtonPreview(self):
        self.filetype = ""
        self.Error.setText("")
        FileLoc = self.comboBox.currentText()
        Files = []

        # region Except Files
        Except = self.lineEdit_Except.displayText().replace(" , ", ",").replace(" ,", ",").replace(", ", "").replace(
            "\"", "").replace("\'", "")
        # endregion

        if "," not in Except:
            Except += ","
        ExceptList = Except.split(",")

        try:
            self.comboBox.setStyleSheet("color:yellow;")
            chdir(FileLoc)
            DirExist = True
        except OSError:
            self.comboBox.setStyleSheet("color:red")
            self.comboBox.setCurrentText("There is no such a directory")
            DirExist = False

        # region Shows
        self.Label_Number.setVisible(True)
        self.Label_Number_2.setVisible(True)
        self.Label_Number_text.setVisible(True)
        # endregion

        # region Files:
        counter = 0
        for (dirpath, dirnames, filenames) in walk(FileLoc):
            for filename in filenames:
                QApplication.processEvents()
                if filename not in ExceptList:
                    absulpathR = path.abspath(sep.join([dirpath, filename]))
                    Files.append(absulpathR)
                counter += 1
                self.Label_Number.setText(str(counter))
        # endregion

        # region common pattern:
        if self.lineEdit_Common.displayText() == "":
            FilesR = Files
        else:
            if self.checkBox_Ex.isChecked():
                self.filetype = "." + (self.lineEdit_Common.displayText()).replace(".", "")
                FilesR = [i for i in Files if self.filetype in i[i.rfind(sep):].replace(sep, "")]
            else:
                FilesR = [i for i in Files if self.lineEdit_Common.displayText() in i[i.rfind(sep):].replace(sep, "")]
        # endregionS

        if DirExist:
            self.Label_Number_2.setText(str(len(FilesR)))
            if FilesR:

                if self.tabWidget.currentIndex() == 0:  # tab_Delete
                    name = FilesR[0][FilesR[0].rfind(sep):].replace(sep, "")
                    if self.checkBox_Select.isChecked():

                        From = self.lineEdit_From.displayText() if self.lineEdit_From.displayText() != "" else name[0]
                        To = self.lineEdit_To.displayText() if self.lineEdit_To.displayText() != "" else name[-1]

                        if self.checkBox_From.isChecked():
                            if self.checkBox_To.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)] + To
                            else:
                                delete = name[name.rfind(From):name.rfind(To)]
                        else:
                            if self.checkBox_To.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "") + (To)
                            else:
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "")

                        self.lineEdit_Preview_R.setText(
                            FilesR[0][FilesR[0].rfind(sep):].replace(delete, "").replace(sep, ""))

                    else:
                        delete = self.lineEdit_Delete.displayText()
                        self.lineEdit_Preview_R.setText(
                            FilesR[0][FilesR[0].rfind(sep):].replace(delete, "").replace(sep, ""))

                if self.tabWidget.currentIndex() == 1:  # tab_rename

                    if self.checkBox_Select_2.isChecked():
                        name = FilesR[0][FilesR[0].rfind(sep):].replace(sep, "")

                        From = self.lineEdit_From_2.displayText() if self.lineEdit_From_2.displayText() != "" else name[
                            0]
                        To = self.lineEdit_To_2.displayText() if self.lineEdit_To_2.displayText() != "" else name[-1]

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
                    self.lineEdit_Preview_R.setText(
                        FilesR[0][FilesR[0].rfind(sep):].replace(re_from, re_to).replace(sep, ""))

                if self.tabWidget.currentIndex() == 2:  # tab_sufix

                    name = FilesR[0][FilesR[0].rfind(sep):].replace(sep, "")
                    if self.filetype == "":
                        typename = "." + name[name.rfind(".", len(name) - 5):].replace(".", "")
                    else:
                        typename = self.filetype

                    prefix = self.lineEdit_addPre.displayText()
                    suffix = self.lineEdit_addSuf.displayText()

                    self.lineEdit_Preview_R.setText(prefix + name[:name.rfind(typename)].replace(".", "") +
                                                    suffix + typename)

                if self.tabWidget.currentIndex() == 3:  # tab_mixed
                    # region Pre-Suffix
                    prefix = self.lineEdit_addPre_2.displayText()
                    suffix = self.lineEdit_addSuf_2.displayText()
                    # endregion

                    name = FilesR[0][FilesR[0].rfind(sep):].replace(sep, "")
                    if self.filetype == "":
                        typename = "." + name[name.rfind(".", len(name) - 5):].replace(".", "")
                    else:
                        typename = self.filetype

                    # region Rename
                    if self.checkBox_Select_3.isChecked():
                        From = self.lineEdit_From_3.displayText() if self.lineEdit_From_3.displayText() != "" else name[
                            0]
                        To = self.lineEdit_To_3.displayText() if self.lineEdit_To_3.displayText() != "" else name[-1]

                        if self.checkBox_From_3.isChecked():
                            if self.checkBox_To_3.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)] + To
                            else:
                                delete = name[name.rfind(From):name.rfind(To)]
                        else:
                            if self.checkBox_To_3.isChecked():
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "") + (To)
                            else:
                                delete = name[name.rfind(From):name.rfind(To)].replace(From, "")

                        re_from = delete

                    else:
                        re_from = self.lineEdit_Rename_From_2.displayText()

                    re_to = self.lineEdit_Rename_To_2.displayText()
                    # endregion

                    try:
                        self.lineEdit_Preview_R.setText(
                            prefix + name[:name.rfind(typename)].replace(".", "").replace(re_from, re_to).replace(sep,
                                                                                                                  "")
                            + suffix + typename)
                    except:
                        self.Error.setText("Be sure about using both Rename and Prefix/Suffix together.")

                if self.tabWidget.currentIndex() == 4:  # tab_advanced

                    name = FilesR[0][FilesR[0].rfind(sep):].replace(sep, "")

                    if self.filetype == "":
                        typename = "." + name[name.rfind(".", len(name) - 5):].replace(".", "")
                    else:
                        typename = self.filetype

                    continue_1 = True
                    continue_2 = True
                    prefix = self.lineEdit_addPre_3.displayText()
                    suffix = self.lineEdit_addSuf_3.displayText()

                    From = self.lineEdit_From_4.displayText() if self.lineEdit_From_4.displayText() != "" else name[0]
                    To = self.lineEdit_To_4.displayText() if self.lineEdit_To_4.displayText() != "" else name[-1]

                    if From not in name:
                        self.Error.setText("\"From\" part is incorect")
                        continue_1 = False
                    if To not in name:
                        self.Error.setText("\"To\" part is incorect")
                        continue_1 = False

                    if self.checkBox_From_4.isChecked():
                        if self.checkBox_To_4.isChecked():
                            select = name[name.rfind(From):name.rfind(To)] + To
                        else:
                            select = name[name.rfind(From):name.rfind(To)]
                    else:
                        if self.checkBox_To_4.isChecked():
                            select = name[name.rfind(From):name.rfind(To)].replace(From, "") + To
                        else:
                            select = name[name.rfind(From):name.rfind(To)].replace(From, "")

                    name = name.replace(select, "")

                    delete = self.lineEdit_Del_char_From_Sel.displayText()

                    if delete in select:
                        continue_2 = True

                    else:
                        continue_2 = False
                        self.Error.setText("The \"Delete\" part is not in the \"Selected\" part.")

                    if continue_1 is True and continue_2 is True:

                        select = select.replace(delete, "")

                        FinSelect = str(prefix + select + suffix)

                        if self.checkBox_paste_beg.isChecked():
                            self.lineEdit_Preview_R.setText(FinSelect + name)

                        else:
                            self.lineEdit_Preview_R.setText(
                                name[:name.rfind(typename)].replace(".", "") + FinSelect + typename)

            else:
                self.Error.setText("There is no file with this pattern.")
                self.lineEdit_Preview_R.setText("")

            if FilesR:
                self.lineEdit_Preview_O.setText(FilesR[0][FilesR[0].rfind(sep):].replace(sep, ""))

    def ButtonHelp(self):
        self.Error.setText("No Help yet :/")

    # endregion

    def SelectFiles(self):
        FileLoc = self.comboBox.currentText()
        chdir(FileLoc)
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = list(filedialog.askopenfilenames(initialdir="./", title="Select except files"))
        file = [i[i.rfind("/"):].replace("/", "") for i in file_path]

        self.lineEdit_Except.setText(str(file).replace("\"", "").replace("[", "").replace("]", ""))

    # region Select Character - Checkbox
    def Checker(self, mode):
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

        if mode == "advanceB":
            self.checkBox_paste_end.setChecked(False)

        if mode == "advanceE":
            self.checkBox_paste_beg.setChecked(False)
    # endregion


if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    MainWindow = QtWidgets.QMainWindow()

    ui = FileRenamer()
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

    # region Button
    ui.Button_open_EX.clicked.connect(ui.SelectFiles)
    # endregion

    # region CheckBoxes
    ui.checkBox_Select.clicked.connect(partial(ui.Checker, "deleter"))
    ui.checkBox_Select_2.clicked.connect(partial(ui.Checker, "renamer"))
    ui.checkBox_Select_3.clicked.connect(partial(ui.Checker, "mixed"))
    ui.checkBox_paste_beg.clicked.connect(partial(ui.Checker, "advanceB"))
    ui.checkBox_paste_end.clicked.connect(partial(ui.Checker, "advanceE"))
    # endregion

    MainWindow.show()
    exit(app.exec_())
