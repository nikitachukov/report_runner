#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ChukovNA'
import logging
import logging.handlers
import traceback
import sys
import os
import cx_Oracle
import json

from pprint import pprint


def init_logger():
    global logger
    LOG_FILENAME = 'report_export.txt'
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(funcName)s:%(lineno)d - %(message)s")
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logfile_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024 * 1024 * 1, backupCount=7)
    logfile_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(logfile_handler)
    logger.addHandler(console_handler)


def load_template(template_file):
    template = json.loads(open(template_file).read())
    return template


def do_exit(abnormal=False):
    if abnormal:
        logger.critical('Работа завершена некорректно')
        sys.exit(1)
    else:
        logger.critical('Работа завершена')
        sys.exit(0)


def do_report(template):
    # host=template['connection']['host']
    # port=template['connection'].get('port')
    # if (not port):
    # port=1521
    # sid=template['connection']['sid']
    # user=template['connection']['user']
    # password=template['connection']['password']


    try:
        dsn_tns = cx_Oracle.makedsn(template['connection']['host'], template['connection'].get('port'), template['connection']['sid'])
        connection = cx_Oracle.connect(template['connection']['user'], template['connection']['password'], dsn_tns)
        logger.info('Соедиенение с базой данных установленно')

        cursor = connection.cursor()
        # result = cursor.var(cx_Oracle.STRING)
        cursor.prepare(template['db']['stored_procedure']['sql'])
        # cursor.execute(template['db']['stored_procedure']['sql'],
        #
        # {'result': result, 'ppolicyno': 30005017}
        #
        # )

        # result = result.getvalue()
        bindparams = cursor.bindnames()
        print(bindparams)
        # # print(template['db']['stored_procedure']['args'])
        #
        # # print(
        # #     [
        #
        args = {}
        for arg in template['db']['stored_procedure']['args']:
            if arg.get('value'):

                args[arg['name'].upper()] = arg['value']
            else:
                args[arg['name'].upper()] = cursor.var(cx_Oracle.STRING)

        # in_arg = [arg['name'].upper() for arg in template['db']['stored_procedure']['args'] if (arg['name'].upper() in bindparams) and arg.get('value')]
        in_arg = [{arg['name'].upper()}for arg in template['db']['stored_procedure']['args'] if (arg['name'].upper() in bindparams) and arg.get('value')]

        out_arg = [{arg['name'].upper() }for arg in template['db']['stored_procedure']['args'] if (arg['name'].upper() in bindparams) and not arg.get('value')]

        # [user['name'] for user in users if user['age'] > 30]

        print(in_arg)
        print(out_arg)
        # print(out_arg.extend(in_arg))
        print(args)
        # print(in_arg+out_arg)
        # cursor.execute(template['db']['stored_procedure']['sql'],args)

        # print(args)
        # print(out_arg)



        # print(args)
        # cursor.execute(template['db']['stored_procedure']['sql'],{})


        # print(args)
        # print(in_arg.extend(out_arg))





        # for bindarg in cursor.bindnames():

        # return dict(zip([x[0] for x in cursor.description], row))





    except cx_Oracle.DatabaseError as e:
        logger.critical(('Database error: %s' % (e.args[0].message)).strip())
        do_exit(abnormal=True)
    except:
        logger.critical(traceback.format_exc())
        do_exit(abnormal=True)





        # dsn_tns = cx_Oracle.makedsn(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'], settings.DATABASES['default']['NAME'])


# cursor = con.cursor()
# cursor.execute("set role lisaro identified by lisaro")
# cursor.execute("SELECT username,lastname,firstname,middlename,phone,email,job FROM lisa.usr_django_auth WHERE username=user")


def main():
    init_logger()

    try:
        logger.info('Начато выполнение скрипта')
        template = load_template('test.json')
        logger.info('Настройки загружены')
        do_report(template)


    except:
        pass
        # logger.critical(traceback.format_exc())
        # do_exit(abnormal=True)


if __name__ == '__main__':
    main()

