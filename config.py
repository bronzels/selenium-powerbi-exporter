import time

db_info = {'user': 'pbeximporter', 'password': 'pbeximporter',
  'host': '127.0.0.1', 'db': 'pbeximporter', 'port': 3306, 'charset': 'utf8',
  'autocommit': True}

sheet_name = 'Sheet1'
tbl_prefix = 'PbEx_'

l_2_simple_eximport = []
'''
    [
    {
        'url': 'http://Test06:s102ywdCwQ_@192.168.0.55:8000/Reports/powerbi/%E9%98%BF%E7%B1%B3%E5%B7%B4%E6%A0%B8%E7%AE%97%E6%8A%A5%E8%A1%A8/TM/TM%E6%88%90%E6%9C%AC%E5%88%86%E6%9E%90%E6%8A%A5%E8%A1%A8',
        'div_classname': 'preTextWithEllipsis',
        'div_cap': '综合外教成本趋势',
        'to_import_db_name': 'AcadsocAMB',
        'to_import_tbl_name': 'teacher_cost_trend',
        'page_loading_secs': 5
    },
    {
        'url': 'http://Test06:s102ywdCwQ_@192.168.0.55:8000/Reports/powerbi/%E9%98%BF%E7%B1%B3%E5%B7%B4%E6%A0%B8%E7%AE%97%E6%8A%A5%E8%A1%A8/TM/TM%E6%88%90%E6%9C%AC%E5%88%86%E6%9E%90%E6%8A%A5%E8%A1%A8',
        'div_class': 'preTextWithEllipsis',
        'div_cap': '综合单位完课成本趋势',
        'to_import_db_name': 'AcadsocAMB',
        'to_import_tbl_name': 'teacher_cost_per_class_trend',
        'page_loading_secs': 5
    }
]
'''

def get_curr_date_input():
    #date_delta4_debug = 9
    str_curr = time.strftime('%Y/%m/%d',time.localtime(time.time()))
    l_curr = str_curr.split('/')
    #l_curr[2] = str(int(l_curr[2]) - date_delta4_debug)
    #return '/'.join(l_curr)
    return '2020/12/8'

l_2_complex_eximport = [
    {
        'url': 'http://LiuAlex:zDKqWx3aQiG@192.168.0.55:8000/reports/powerbi/%E6%95%B0%E6%8D%AE%E6%88%98%E7%95%A5%E9%83%A8/test/%E8%BF%90%E8%90%A5%E5%95%86%E5%8F%B7%E7%A0%81%E5%88%86%E6%9E%90',
        'div_cssfmt': 'div[class=\'visualTitle themableBackgroundColor themableColor\'][title=\'{}\']',
        'div_cap': '各运营商15天移动平均接通率趋势',
        'to_import_db_name': 'AcadsocAMB',
        'to_import_tbl_name': 'line_15days_moving_average_call_through_rate_thread',
        'page_loading_secs': 10,
        'dates': [
            {
                'input_name': '日期-结束',
                'input_prop_value': '结束值输入框。输入范围介于 ',
                'value': get_curr_date_input
            },
            {
                'input_name': '日期-开始',
                'input_prop_value': '起始值输入框。输入范围介于 ',
                'value': get_curr_date_input
            },
        ],
        'dropdowns': [
            {
                'div_class': 'slicer-restatement',
                'div_caption': '非VIP呼出',
                'col_2_select': '呼出类型',
                'drop_items':
                    [
                        '非VIP呼出',
                        '试课呼出'
                    ]
            },
            {
                'div_class': 'slicer-restatement',
                'div_caption': '蜂云-109501',
                'col_2_select': '呼出线路',
                'drop_items':
                    [
                        '北京号外号-600100014',
                        '蜂云-109501',
                        '捷讯-075520200731',
                        '联通-057456888888',
                        '联通-075510101616',
                        '联通-075561988888'
                    ]
            },
        ],
    }
]

