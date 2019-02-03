#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad

from table import FTableWidget, TotalsWidget
from PyQt4.QtCore import QDate, Qt

from export_pdf import pdf_view
from PyQt4.QtGui import (
    QVBoxLayout, QComboBox, QIcon, QGridLayout, QPushButton, QMenu)
from util import date_to_datetime, formatted_number, is_int, uopen_file, check_is_empty
from common import (
    FWidget, IntLineEdit, LineEdit, FLabel, FormatDate)

# from configuration import Config


class InvoiceViewWidget(FWidget):

    def __init__(self, product="", parent=0, *args, **kwargs):
        super(InvoiceViewWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parentWidget().setWindowTitle("Facturation")
        self.parent = parent

        vbox = QVBoxLayout()
        # hbox = QHBoxLayout(self)
        editbox = QGridLayout()
        self.num_invoice = IntLineEdit()
        self.num_invoice.setMinimumSize(130, 40)
        self.num_invoice.setPlaceholderText("Le numéro")
        self.num_invoice.setMaximumSize(
            80, self.num_invoice.maximumSize().height())
        self.invoice_date = FormatDate(QDate.currentDate())
        self.name_client_field = LineEdit()
        self.name_client_field.setMinimumSize(130, 40)
        self.name_client_field.setPlaceholderText("Nom compléte du client")

        self.string_list = [""]
        # Combobox widget for add store
        self.liste_type_invoice = ["Facture", "Bon"]

        bicon = QIcon.fromTheme('', QIcon("img/pdf.png"))
        self.pdf_bn = QPushButton(bicon, "")
        self.pdf_bn.released.connect(self.printer_pdf)
        self.pdf_bn.setEnabled(False)
        self.pdf_bn.setShortcut("Alt+P")
        self.box_type_inv = QComboBox()
        for index in range(0, len(self.liste_type_invoice)):
            op = self.liste_type_invoice[index]
            sentence = "%(name)s" % {'name': op}
            self.box_type_inv.addItem(sentence, op)

        self.table_invoice = InvoiceTableWidget(parent=self)

        self.name_client_field.textChanged.connect(
            self.table_invoice.changed_value)
        editbox.addWidget(self.box_type_inv, 0, 0)
        editbox.addWidget(self.num_invoice, 0, 1)
        editbox.addWidget(FLabel("Doit :"), 1, 0)
        editbox.addWidget(self.name_client_field, 1, 1, 1, 3)
        editbox.addWidget(FLabel("Date :"), 0, 2)
        editbox.addWidget(self.invoice_date, 0, 3)
        editbox.addWidget(self.pdf_bn, 0, 8)
        editbox.setColumnStretch(4, 3)

        vbox.addLayout(editbox)
        vbox.addWidget(self.table_invoice)
        self.setLayout(vbox)

    def refresh_(self):
        pass

    def printer_pdf(self):
        pdf = pdf_view(self.data_export())
        uopen_file(pdf)

    def data_export(self):
        return {
            "title": "eee",
            "file_name": "facture.pdf",
            "invoice_date": date_to_datetime(self.invoice_date.text()).strftime("%d %B %Y"),
            "name_client": self.name_client_field.text(),
            "number": self.num_invoice.text(),
            "invoice_type": self.liste_type_invoice[
                self.box_type_inv.currentIndex()],
            "data": self.table_invoice.get_table_items()
        }


class InvoiceTableWidget(FTableWidget):

    def __init__(self, parent, *args, **kwargs):
        FTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.parent = parent
        self.pparent = parent.parent
        self.hheaders = ["Modeles", "Quantité", "Prix Unitaire", "Montant"]

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popup)

        # self.stretch_columns = [0, 1, 2, 3]
        # self.align_map = {3: 'r'}
        self.display_vheaders = False
        # self.display_fixed = True

        self.refresh_()

    def refresh_(self, choix=None):
        self.row = ["", "", "", ""]
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self._reset()
        self.data.extend([self.row])
        self.refresh()

    # def del_row(self):
    #     row = self.rowCount() - 2
    #     print(row, len(self.data))
    #     # if (len(self.data) - 1) < row:
    #     #     return False
    #     try:
    #         self.data.pop(row)
    #     except IndexError:
    #         pass

    def popup(self, pos):
        row = self.selectionModel().selection().indexes()[0].row()
        if (len(self.data) - 1) < row:
            return False
        menu = QMenu()
        quit_action = menu.addAction("Supprimer cette ligne")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == quit_action:
            try:
                self.data.pop(row)
            except IndexError:
                pass
            self.refresh()

    def extend_rows(self):
        nb_rows = self.rowCount()
        self.setRowCount(nb_rows + 2)
        monttc = TotalsWidget(formatted_number("%d" % 0))
        self.add_bn = QPushButton("+")
        self.add_bn.setShortcut("Alt+A")
        self.add_bn.released.connect(self.add_row)
        self.setCellWidget(nb_rows, 3, self.add_bn)
        # self.del_bn = QPushButton("-")
        # self.del_bn.setShortcut("Alt+D")
        # self.del_bn.released.connect(self.del_row)
        # self.setCellWidget(nb_rows, 2, self.del_bn)
        nb_rows += 1
        self.setItem(nb_rows, 2, TotalsWidget("Montant"))
        self.setItem(nb_rows, 3, monttc)
        # self.button.setEnabled(False)
        self.setSpan(nb_rows - 1, 0, 2, 2)

        pw = self.width() / 5
        self.setColumnWidth(0, pw * 2)
        self.setColumnWidth(1, pw)
        self.setColumnWidth(2, pw)

    def add_row(self):
        if len(self.data) <= 20:
            self._reset()
            self.data.extend([self.row])
            self.refresh()

    def _update_data(self, row_num, new_data):
        self.data[row_num] = (new_data[0], new_data[1], new_data[2],
                              new_data[3])

    def _item_for_data(self, row, column, data, context=None):
        if column == 0:
            self.line_edit = LineEdit("%s" % data)
            return self.line_edit
        if column == 1 or column == 2:
            self.line_edit = IntLineEdit("%s" % data)
            self.line_edit.textChanged.connect(self.changed_value)
            self.line_edit.setAlignment(Qt.AlignRight)
            return self.line_edit
        return super(InvoiceTableWidget, self)._item_for_data(row, column,
                                                              data, context)

    def get_table_items(self):
        """ Recupère les elements du tableau """

        list_invoice = []
        for i in range(self.rowCount() - 2):
            liste_item = []
            row_data = self.data[i]
            try:
                liste_item.append(str(row_data[0]))
                liste_item.append(is_int(row_data[1]))
                liste_item.append(is_int(row_data[2]))
                list_invoice.append(liste_item)
            except AttributeError:
                raise
                liste_item.append("")

        return list_invoice

    def changed_value(self, refresh=False):
        """ Calcule les Resultat """
        self.mtt_ht = 0
        self.parent.pdf_bn.setEnabled(True)
        for row_num in range(0, self.data.__len__()):
            designation = str(self.cellWidget(row_num, 0).text())
            qtsaisi = is_int(self.cellWidget(row_num, 1).text())
            pusaisi = is_int(self.cellWidget(row_num, 2).text())
            if check_is_empty(self.parent.num_invoice):
                return
            if check_is_empty(self.parent.name_client_field):
                return
            if (pusaisi and check_is_empty(self.cellWidget(row_num, 1))):
                return
            if (pusaisi and check_is_empty(self.cellWidget(row_num, 2))):
                return
            montant = (qtsaisi * pusaisi)
            self.mtt_ht += montant
            self.setItem(row_num, 3, TotalsWidget(formatted_number(montant)))
            self._update_data(
                row_num, [designation, qtsaisi, pusaisi, self.mtt_ht])
        self.setItem(
            row_num + 2, 3, TotalsWidget(formatted_number(self.mtt_ht)))
