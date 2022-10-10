# coding=GBK
"""
This script is the prototype of invoice reimbursement automation for everbright trust
"""
import math

from random import randint, sample, choice
from docx import Document
from .models import CompanyReim, ClientReim, FieldReim


class InvoiceReimburse:
    def __init__(self, reim_input):
        self.invoice_info = reim_input
        self.invoice_info['amount'] = float(self.invoice_info['amount'])

        #  set the multiple of average dining fee base based on dining type
        self.base_multiplpe_dict = {
            '�����д�': 1,
            'һ���д�': 2,
            '�����д�': 3,
        }
        self.base_multiplpe = self.base_multiplpe_dict[self.invoice_info['dining_type']]

        #  initialize class attributes
        self.clients_str = ''  # readable clients string
        self.guests = 0  # number of guests
        self.avai_com_objs = []  # a list of CompanyReim objects, the company in which has more clients than self.guests
        self.table = ''  #  the table instance generated using docx.Document.tables in the word attachment


    def attachment_gen(self):
        """
        generate the attachment file required
        """
        file = "C:/Users/13554/OneDrive/pythonproject/Report_Automation/test_words/template����Ʊ������.docx"
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
        doc.save("C:/Users/13554/OneDrive/pythonproject/Report_Automation/test_words/����Ʊ���������.docx")

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
        self.avai_com()

        random_com_obj = choice(self.avai_com_objs)  #  avai_com_objs is a list of objects, thus using choice here
        self.confirmed_company = random_com_obj.company
        client_objs = [client_obj for client_obj in ClientReim.objects.filter(company=random_com_obj)]

        random_client_objs = sample(client_objs, self.guests)
        print(random_client_objs)

        # create a readable client string, for example, "Ͷ�ʲ���+Ͷ�ʾ���+��+�ܣ�"��

        for client_obj in random_client_objs:
            self.clients_str += client_obj.department + client_obj.position + client_obj.client + '��' + '��'
        self.clients_str = self.clients_str[:-1]  # remove the last comma

        last = FieldReim.objects.filter(company=random_com_obj).count() - 1
        idx = randint(0, last)
        random_field_obj = FieldReim.objects.filter(company=random_com_obj)[idx]
        print(random_field_obj)

        #  texts prep for page display and attachment table population
        self.field = "��" + random_field_obj.field + "����Ǣ̸"
        self.ave_amount = self.invoice_info['amount'] / self.diners
        self.amount_str = '{:,.2f}'.format(self.invoice_info['amount']) + "Ԫ"
        self.ave_amount_str = '{:,.2f}'.format(self.ave_amount) + "Ԫ"
        self.hosts_str = str(self.hosts) + "��"
        self.guests_str = str(self.guests) + "��"
        """
        print("________________________")
        print("�д���λ��" + self.confirmed_company)
        print("�д����ˣ�" + self.field)
        print("�д���Ա��" + self.clients_str)
        print("�Ӵ�������" + self.hosts_str + "���д�������" + self.guests_str)
        print("�ܽ�� ��" +  self.amount_str)
        print("�˾���" + self.ave_amount_str)
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
        if self.invoice_info['preset_number']:
            print('�����趨���ò�����')
            self.diners = int(self.invoice_info['preset_number'])
        else:
            min_number = max(2, math.ceil(self.invoice_info['amount'] / (200*self.base_multiplpe)))
            max_number = min(max(2, int(self.invoice_info['amount'] // (140*self.base_multiplpe))), 6)
            self.diners = randint(min_number, max_number)

            print('�������趨���ò��������Զ������ò�����')
            print('��С������' + str(min_number))
            print('���������' + str(max_number))

        # print('��������' + str(self.diners))
        self.hosts = randint(1, int(self.diners / 2))
        self.guests = self.diners - self.hosts
        # print('���нӴ���������Ϊ: ' + str(self.hosts))

    def avai_com(self):
        """
        return available companies (companies that have more clients than guests)
        """
        print('self.avai_com starts')
        coms_objs = CompanyReim.objects.all()
        for com_obj in coms_objs:
            #  what if add a field to CompanyReim to get the client number of the company
            clients_objs = ClientReim.objects.filter(company=com_obj)
            if len(clients_objs) >= self.guests:
                self.avai_com_objs.append(com_obj)
        print(self.avai_com_objs)
        """
        for company, clients_in_a_company in self.clients_dict.items():
            clients_number_in_a_company = len(clients_in_a_company)
            if clients_number_in_a_company >= self.guests:
                avai_com.append(company)
        """

    """
    def clients_dict_gen(self):

        self.clients_dict = {}
        all_companies = CompanyReim.objects.all()

        for row in tuple(self.ws.values)[1:]:
            name, depar, position, *field = row[1:]
            field = list(filter(None, field))
            depar = depar or ''  # only depar could be vacant
            if row[0] not in self.clients_dict.keys():
                self.clients_dict[row[0]] = []
            self.clients_dict[row[0]].append([name, depar, position, field])
    """

if __name__ == '__main__':
    reim_input = {
        'amount': 3000,
        'restaurant': '�óԵĲ���',
        'date': '2022-10-07',
        'preset_number': None,
        'dining_type': '�����д�',
    }
    ir = InvoiceReimburse(reim_input)
    ir.who_to_dine()
    # ir.attachment_gen()




