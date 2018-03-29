# coding=utf-8
# control sdk
# author = 'dh'
import xlrd
import xlwt
from xlutils.copy import copy

from lib.control.ue_analyze_controller import *
import csv
import codecs
import sys


# @print_trace
# @log_func_args
# def get_result_csv(sdk_version, live_push_version, play_duration, lf=0, mode_type=MODE_UDP, start_time=None,
#                    end_time=None, bandwidth='2M'):
#     db_object = MysqlDB(MYSQL_HOST, MYSQL_UE_USER, MYSQL_PASSWORD, MYSQL_DB_NAME)
#     csv_file = codecs.open(CSV_FILE, "wb", "utf_8_sig")
#     writer = csv.writer(csv_file)
#     data = [
#         CSV_DATABASE_HEADER
#     ]
#
#     for record in condition_select(db_object, sdk_version=sdk_version, live_push_version=live_push_version,
#                                    mode=mode_type, play_duration=play_duration, lf=lf, band_width=bandwidth,
#                                    start_time=start_time, end_time=end_time):
#         data.append(record)
#
#     # print data
#     # new_data = generate_format(data)
#     reload(sys)
#     sys.setdefaultencoding("utf-8")
#     writer.writerows(data)
#     csv_file.close()


def get_result_xls(sdk_version, live_push_version, play_duration, lf=0, mode_type=MODE_UDP, start_time=None,
                   end_time=None, bandwidth='2M'):
    """
        create a excel file of ue test results
    """
    db_obj = MysqlDB(MYSQL_HOST, MYSQL_UE_USER, MYSQL_PASSWORD, MYSQL_DB_NAME)
    file_name = EXCEL_PATH + 'result_' + sdk_version + '_' + live_push_version + '.xls'
    summary_file_name = EXCEL_PATH + 'summary_result.xls'
    table_name = 'sdk' + sdk_version + '+livepush' + live_push_version
    results = condition_select_v2(db_obj, sdk_version=sdk_version, live_push_version=live_push_version, mode=mode_type,
                                  play_duration=play_duration, lf_number=lf, band_width=bandwidth,
                                  start_time=start_time, end_time=end_time)
    data = [EXCEL_ROW0]
    data += results
    if os.path.isfile(file_name):
        append_data2xls(file_name, table_name, results)
    else:
        new_excel = xlwt.Workbook()
        table = new_excel.add_sheet(table_name)
        write_xls(table, data)
        new_excel.save(file_name)

    copy_sheet_to_other_file(file_name, summary_file_name, table_name)


def write_xls(obj, data):
    """
        method for write
    """
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            obj.write(i, j, value)


def append_data2xls(filename, table_name, data):
    """
        append data to exist xls
    """
    r_xls = xlrd.open_workbook(filename)
    r_sheet = r_xls.sheet_by_name(table_name)
    end_row_number = r_sheet.nrows
    w_xls = copy(r_xls)
    sheet_write = w_xls.get_sheet(0)

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            sheet_write.write(end_row_number + i, j, value)
    w_xls.save(filename)


def copy_sheet_to_other_file(o_filename, d_filename, sheet_name):
    """
        copy sheet from one file to other file 
    """
    of = xlrd.open_workbook(o_filename)
    of_sheet = of.sheet_by_name(sheet_name)
    row_number = of_sheet.nrows
    data = list()
    for i in xrange(row_number):
        data.append(of_sheet.row_values(i))

    delete_sheet(d_filename, sheet_name)
    o_df = xlrd.open_workbook(d_filename)
    df = copy(o_df)
    df_sheet = df.add_sheet(sheet_name)
    write_xls(df_sheet, data)
    df.save(d_filename)


def delete_sheet(file_name, sheet_name):
    """
        delete a sheet
    """
    o_df = xlrd.open_workbook(file_name)
    df = copy(o_df)
    df._Workbook__worksheets = [worksheet for worksheet in df._Workbook__worksheets if worksheet.name != sheet_name]
    df.save(file_name)


if __name__ == "__main__":
    # mode http not depend on sdk_version, no mater what you write.
    # get_result_csv(sdk_version='3.17.22', live_push_version='2.6.63', play_duration=3600, mode_type='udp',
    #                lf=0, start_time='20170718171800', bandwidth='2M')

    get_result_xls(sdk_version='3.19.7', live_push_version='pushdev-201709141746', play_duration=3600, mode_type='udp',
                   lf=0, start_time='20170830090000', bandwidth='2M')
    get_result_xls(sdk_version='3.19.7', live_push_version='pushdev-201709141746', play_duration=3600, mode_type='udp',
                   lf=70, start_time='20170830090000', bandwidth='2M')
