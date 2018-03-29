# using coding=utf-8
# author = SXL

import numpy as np
import matplotlib.pyplot as plt
import xlrd


class UEPainter(object):
    """
        class for paint ue
    """

    def __init__(self):
        self.total_width = 0.8
        self.colors = ['r', 'y', 'b', 'g', 'm', 'c']
        self.table_list = None
        self.width = None

    def _paint_bar(self, values_dict):
        n = len(values_dict)
        x = np.arange(n)
        x = x.astype('float')
        conditions = sorted(values_dict.keys(), cmp=cmp_delay_loss)
        plt.xticks(x + self.width, conditions)
        for index, table_name in enumerate(self.table_list):
            tb_values = list()
            for condition in conditions:
                tb_values.append(values_dict[condition][index])
            plt.bar(x, tb_values, width=self.width, label=table_name)
            x += self.width

    @staticmethod
    def _paint_legend(title, picture_name, x_label='', y_label=''):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        plt.legend()
        fig.savefig(picture_name)
        plt.show()

    def paint_startup(self, file_name, channel_rate, lf_number, bandwidth, table_list):
        self.table_list = table_list
        self.width = self.total_width / len(self.table_list)
        startup_dict = ue_collector(file_name, 'startup', channel_rate, lf_number, bandwidth, *table_list)
        self._paint_bar(startup_dict)
        self._paint_legend(title='startup time -- %d LF' % lf_number, picture_name='startup_%dlf.png' % lf_number,
                           y_label='time/s')

    def paint_buffering_number(self, file_name, channel_rate, lf_number, bandwidth, table_list):
        self.table_list = table_list
        self.width = self.total_width / len(self.table_list)
        buffering_num_dict = ue_collector(file_name, 'buffering_num', channel_rate, lf_number, bandwidth, *table_list)
        self._paint_bar(buffering_num_dict)
        self._paint_legend(title='buffering number -- %d LF' % lf_number,
                           picture_name='buffering_num_%dlf.png' % lf_number,
                           x_label='delay(ms)&loss',
                           y_label='buffering number')

    def paint_buffering_ratio(self, file_name, channel_rate, lf_number, bandwidth, table_list):
        self.table_list = table_list
        self.width = self.total_width / len(self.table_list)
        buffering_ratio_dict = ue_collector(file_name, 'buffering_ratio', channel_rate, lf_number, bandwidth,
                                            *table_list)
        self._paint_bar(buffering_ratio_dict)
        self._paint_legend(title='buffering ratio -- %d LF' % lf_number,
                           picture_name='buffering_ratio_%dlf.png' % lf_number,
                           x_label='delay(ms)&loss',
                           y_label='buffering total time/play total time')


class UEExcelReader(object):
    """
        class for read ue
    """

    def __init__(self, file_name):
        self.data = xlrd.open_workbook(file_name)
        self.table = None

    def set_table(self, table_name):
        self.table = self.data.sheet_by_name(table_name)

    def _get_row_number(self):
        rows = self.table.nrows
        return rows

    def _get_col_number(self):
        cols = self.table.ncols
        return cols

    def _get_values_by_condition(self, channel_rate, lf_number, bandwidth, col_number):
        """
            find row number and col number by channel_rate & lf_number
        """

        tar_channel_rate_row = []
        tar_lf_row = []
        tar_bandwidth_row = []
        tar_values = {}
        for row_num, value in enumerate(self.get_col(-2)):
            if value == channel_rate:
                tar_channel_rate_row.append(row_num)
        for row_num, value in enumerate(self.get_col(-3)):
            if value == lf_number:
                tar_lf_row.append(row_num)
        for row_num, value in enumerate(self.get_col(-1)):
            if value == bandwidth:
                tar_bandwidth_row.append(row_num)
        tar_row = list(set(tar_channel_rate_row) & set(tar_lf_row) & set(tar_bandwidth_row))
        col_label = self.get_col(0)
        col_values = self.get_col(col_number)
        for row_num in tar_row:
            tar_values[col_label[row_num]] = col_values[row_num]
        return tar_values

    def get_row(self, row_number):
        row_items = list()
        for col_number in xrange(self._get_col_number()):
            row_items.append(self.table.row(row_number)[col_number].value)
        return row_items

    def get_col(self, col_number):
        col_items = list()
        for row_number in xrange(self._get_row_number()):
            col_items.append(self.table.col(col_number)[row_number].value)
        return col_items

    def get_cell(self, row_number, col_number):
        cell_item = self.table.cell(row_number, col_number).value
        return cell_item

    def startup_time_count(self, channel_rate, lf_number, bandwidth):
        """
            table structure row1:
            startup time = col 3
|delay&loss|version|sample num|startup time|buffering num|buffering time|buffering ratio|p2p|lf|channel rate|bandwidth|

        """

        tar_startup = self._get_values_by_condition(channel_rate, lf_number, bandwidth, 3)
        return tar_startup

    def buffering_count(self, channel_rate, lf_number, bandwidth):
        """
            buffering num = col 4
        """

        tar_buffering_num = self._get_values_by_condition(channel_rate, lf_number, bandwidth, 4)
        return tar_buffering_num

    def buffering_ratio_count(self, channel_rate, lf_number, bandwidth):
        """
            buffering ratio = col 6
        """
        tar_buffering_ratio = self._get_values_by_condition(channel_rate, lf_number, bandwidth, 6)
        return tar_buffering_ratio
        pass

    def __str__(self):
        return '[table info]: col_number %d row_number %d' % (self._get_col_number(), self._get_row_number())

    def __call__(self, table_name):
        self.table = self.data.sheet_by_name(table_name)

    def __del__(self):
        del self.data


class NoTypeError(RuntimeError):
    def __init__(self, message):
        self.message = message


def ue_collector(file_name, value_type, channel_rate, lf_number, bandwidth, *table_list):
    values_dict = dict()
    values_temp_list = list()
    temp_list = list()
    ecl_obj = UEExcelReader(file_name)
    for table_name in table_list:
        if table_name == 'tcp':
            lf_num = 0
        else:
            lf_num = lf_number
        ecl_obj(table_name)
        # print '[table name]: ', table_name, '\t',  ecl_obj
        if value_type == 'startup':
            table_dict = ecl_obj.startup_time_count(channel_rate, lf_num, bandwidth)
        elif value_type == 'buffering_num':
            table_dict = ecl_obj.buffering_count(channel_rate, lf_num, bandwidth)
        elif value_type == 'buffering_ratio':
            table_dict = ecl_obj.buffering_ratio_count(channel_rate, lf_num, bandwidth)
        else:
            raise NoTypeError('value type is not support')
        values_temp_list.append(table_dict)
    for table_dict in values_temp_list:
        temp_list += table_dict.keys()
    for key in set(temp_list):
        if key not in values_dict:
            values_dict[key] = list()
        for table_dict in values_temp_list:
            values_dict[key].append(table_dict[key])
    return values_dict


def cmp_delay_loss(c1, c2):
    """
        compare method for delay&loss
        priority: delay first loss second
    """

    c1 = c1.split(u'ms_')
    c2 = c2.split(u'ms_')
    if int(c1[0]) > int(c2[0]):
        return 1
    elif int(c1[0]) == int(c2[0]):
        if int(c1[1].replace(u'%', u'')) > int(c2[1].replace(u'%', u'')):
            return 1
        else:
            return -1
    else:
        return -1


if __name__ == '__main__':
    # t_list = [u'tcp', u'sdk3.20.0+livepush2.8.0_0823', u'sdk3.18.200+livepush2.6.200', u'sdk3.19.0+livepush2.7.0_0815', u'sdk3.18.24+livepush2.6.92', u'sdk3.18.21+livepush2.6.92', u'sdk3.19.0+livepush2.7.0_0811',u'sdk3.18.7+livepush2.6.71']
    t_list = [u'sdk3.19.6+livepush2.7.13', u'sdk3.19.6+livepush2.7.11', u'sdk3.19.4+livepush2.7.9', u'sdk3.19.0+livepush2.7.0_0815', u'sdk3.18.7+livepush2.6.71']
    eg = UEPainter()
    # eg.paint_buffering_ratio('summary_result.xls', '1M', 70, '2M', t_list)
    eg.paint_buffering_number(r'summary_result.xls', '1M', 0, '2M', t_list)
    pass
