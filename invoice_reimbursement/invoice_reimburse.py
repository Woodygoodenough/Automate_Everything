# coding=GBK
"""
This script is the prototype of invoice reimbursement automation for everbright trust
"""
import math

from openpyxl import workbook, load_workbook
from random import randint, sample
from docx import Document


class InvoiceReimburse():
    def __init__(self, reim_input):
        self.wb = load_workbook("C:/Users/13554/OneDrive/pythonproject/Report_Automation/test_excel/联系人名单.xlsx")
        self.ws = self.wb.active
        self.invoice_info = reim_input
        self.invoice_info['amount'] = float(self.invoice_info['amount'])
        self.invoice_info['preset_number'] = int(self.invoice_info['preset_number'])

        self.unpack_excel()


    def attachment_gen(self):
        """
        generate the attachment file required
        """
        file = "C:/Users/13554/OneDrive/pythonproject/Report_Automation/test_words/template【发票报销】.docx"
        doc = Document(file)
        #  use docx to open an attachment template. There is a table inside. Populate the table with generated info.
        self.table = doc.tables[0]
        self.cell_manuver(0, 1, self.field)
        self.cell_manuver(1, 1, self.invoice_info['date'])
        self.cell_manuver(1, 3, self.confirmed_company)
        self.cell_manuver(2, 1, self.invoice_info['restaurant'])
        self.cell_manuver(3, 3, self.clients_str)
        self.cell_manuver(4, 1, self.guests_str)
        self.cell_manuver(4, 3, self.hosts_str)
        self.cell_manuver(5, 1, self.amount_str)
        self.cell_manuver(5, 3, self.ave_amount_str)
        doc.save("C:/Users/13554/OneDrive/pythonproject/Report_Automation/test_words/【发票报销】输出.docx")

    def cell_manuver(self, x, y, txt):
        """
        populate the cell with coordinates of (x,y) with text of txt
        """
        cell = self.table.cell(x, y)
        runs = cell.paragraphs[0].runs
        runs[0].clear()
        cell.paragraphs[0].add_run(text=txt)

    def who_to_dine(self):
        """
        automatically select the guests and generate other relevant info for reimbusement
        return a dict for page display of reimbursement info
        """
        self.diners_num()
        self.clients_str = ''
        avai_com = self.avai_com()
        avai_num = len(avai_com)
        idx = randint(1, avai_num)
        self.confirmed_company = avai_com[idx - 1]
        clients = sample(self.clients_dict[self.confirmed_company], self.guests)

        for client in clients:
            self.clients_str += client[1] + client[2] + client[0][0] + '总' +'，'
        self.clients_str = self.clients_str[:-1]

        field = clients[0][-1]
        idx = randint(1, len(field))
        #  texts prep for page display and attachment table population
        self.field = "就" + field[idx - 1] + "进行洽谈"
        self.ave_amount = self.invoice_info['amount'] / self.diners
        self.amount_str = '{:,.2f}'.format(self.invoice_info['amount']) + "元"
        self.ave_amount_str = '{:,.2f}'.format(self.ave_amount) + "元"
        self.hosts_str = str(self.hosts) + "人"
        self.guests_str = str(self.guests) + "人"
        """
        print("________________________")
        print("招待单位：" + self.confirmed_company)
        print("招待事宜：" + self.field)
        print("招待人员：" + self.clients_str)
        print("接待人数：" + self.hosts_str + "；招待人数：" + self.guests_str)
        print("总金额 ：" +  self.amount_str)
        print("人均金额：" + self.ave_amount_str)
        print("________________________")
        """
        return {
            'confirmed_company': self.confirmed_company,
            'field': self.field,
            'clients': self.clients_str,
            'hosts': self.hosts_str,
            'guests': self.guests_str,
            'amount': self.amount_str,
            'ave_amount': self.ave_amount_str,
        }


    def diners_num(self):
        """
        take in preset number of diners_num if there is any, and generate the number of diners for the hosts and guests
        """
        if self.invoice_info['preset_flag']:
            print('存在设定的用餐人数')
            self.diners = self.invoice_info['preset_number']
        else:
            min_number = max(2, math.ceil(self.invoice_info['amount'] / 200))
            max_number = min(max(2, int(self.invoice_info['amount'] // 135)), 6)
            self.diners = randint(min_number, max_number)
            """
            print('不存在设定的用餐人数，自动产生用餐人数')
            print('最小人数：' + str(min_number))
            print('最大人数：' + str(max_number))
            """
        # print('总人数：' + str(self.diners))
        self.hosts = randint(1, int(self.diners / 2))
        self.guests = self.diners - self.hosts
        # print('其中接待人数设置为: ' + str(self.hosts))


    def avai_com(self):
        """
        return available companies (companies that have more clients than guests)
        """
        avai_com = []
        for company, clients_in_a_company in self.clients_dict.items():
            clients_number_in_a_company = len(clients_in_a_company)
            if clients_number_in_a_company >= self.guests:
                avai_com.append(company)
        return avai_com

    def unpack_excel(self):
        """
        create a clients dict from the standardised excel file, keys are companies, values are lists of clients,
        with each item representing a client as a nested list, in which the items are names(str), department(str),
        position(str) and field(list).
        """
        self.clients_dict = {}
        for row in tuple(self.ws.values)[1:]:
            name, depar, position, *field = row[1:]
            field = list(filter(None, field))
            depar = depar or ''  # only depar could be vacant
            if row[0] not in self.clients_dict.keys():
                self.clients_dict[row[0]] = []
            self.clients_dict[row[0]].append([name, depar, position, field])

if __name__ == '__main__':
    ir = InvoiceReimburse()
    ir.who_to_dine()
    ir.attachment_gen()




