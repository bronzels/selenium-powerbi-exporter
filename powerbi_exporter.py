from selenium import webdriver
from time import sleep
import pandas as pd
import sqlalchemy
import os
import itertools

import config
import env_config

def find_iframe(driver):
    iframes = driver.find_elements_by_tag_name('iframe')
    return iframes[0]

def find_element_by_classname_cap(driver, classname, cap):
    elements = driver.find_elements_by_class_name(classname)
    ret = None
    for element in elements:
        if element.text == cap:
            ret = element
            break
    return ret

def find_element_by_cssfmt_cap(driver, css_fmt, cap):
    ret = driver.find_element_by_css_selector(css_fmt.format(cap))
    return ret

def find_element_by_class_id(driver, classname, id):
    elements = driver.find_elements_by_class_name(classname)
    ret = None
    for element in elements:
        if element.id == id:
            ret = element
            break
    return ret

def wait_until(is_none_or_bool, prompt, func_2wait, *params):
    if is_none_or_bool:
        func = lambda _func_2wait, *_params: _func_2wait(*_params) is None
    else:
        func = lambda _func_2wait, *_params: not _func_2wait(*_params)
    print(prompt, end='')
    while func(func_2wait, *params):
        sleep(1)
        print('.', end='')
    print('/n')
    return func_2wait(*params)

def init(d_config, driver):
    print('url loading...')
    driver.get(d_config['url'])
    sleep(d_config['page_loading_secs'])
    # driver.refresh()

    iframe = wait_until(True, 'iframe to find', find_iframe, driver)

    driver.switch_to.frame(iframe)


def download(driver, diagram_classname_cssfmt, if_classname, diagram_cap, to_import_tbl_name, if_replace = True, d_col_2_append = None):
    common_context_menu_class_name = 'vcMenuBtn'
    common_exp_menuitem_css_selector = '.ng-scope.default-contextmenu.dropdownOverlay.overlay.themeableElement.overlayActive ng-transclude ng-repeat h6'

    diagram = wait_until(True, 'diagram to find', find_element_by_classname_cap if if_classname else find_element_by_cssfmt_cap, driver, diagram_classname_cssfmt, diagram_cap)
    diagram.click()

    context_menu_btn = wait_until(True, 'context_menu_btn to find', driver.find_element_by_class_name,
                                  common_context_menu_class_name)
    #context_menu_btn.click()
    driver.execute_script("arguments[0].click();", context_menu_btn)

    exp_menuitem = wait_until(True, 'exp_menuitem to find', driver.find_element_by_css_selector,
                              common_exp_menuitem_css_selector)
    exp_menuitem.click()

    print('remove file to be downloaded if exists...')
    excel_file_path = env_config.dlpath + diagram_cap + '.xlsx'
    if os.path.exists(excel_file_path):
        os.remove(excel_file_path)

    exp_btn = wait_until(True, 'exp_btn to find', find_element_by_classname_cap, driver, 'primary', '导出')
    exp_btn.click()
    sleep(3)
    print('exp_btn clicked')

    wait_until(False, 'file downloading', os.path.exists, excel_file_path)

    # 多次下载时从第3次开始，点击确定后download对话框不关闭
    dl_dailog_x_btn = None
    try:
        dl_dailog_x_btn = driver.find_element_by_xpath('//input[@class=\'infonav-dialogCloseIcon\']')
    except Exception as e:
        print(str(e))
        pass
    else:
        pass
    finally:
        if dl_dailog_x_btn is not None:
            dl_dailog_x_btn.click()
            sleep(3)
            print('x clicked')

    df = pd.read_excel(excel_file_path, sheet_name='Sheet1', skiprows=2)
    print('df read\n:{}'.format(df))
    if d_col_2_append is not None:
        for (k, v) in d_col_2_append.items():
            df[k] = v
        print('df appended\n:{}'.format(df))

    engine = sqlalchemy.create_engine(env_config.mssql_url + d_complex_config['to_import_db_name'], echo=True)
    df.to_sql(name=to_import_tbl_name, con=engine, chunksize=1000, if_exists='replace' if if_replace else 'append',
              index=None)
    print('table wrote')

if __name__ == '__main__':
    driver = webdriver.Chrome(env_config.drvpath)
    driver.set_window_size(1400, 1000)
    '''
    for d_simple_config in config.l_2_simple_eximport:
        print('d_config:{}'.format(d_simple_config))
        to_import_tbl_name = config.tbl_prefix + d_simple_config['to_import_tbl_name']

        init(d_simple_config, driver)

        diagram_classname = d_simple_config['div_classname']
        class_cap = d_simple_config['div_cap']

        download(driver, diagram_classname, True, class_cap, to_import_tbl_name)
    '''
    complex_input_date_xpath_fmt = '//input[@class=\'date-slicer-input hasDatepicker enable-hover\' and contains(@aria-label, \'{}\')]'
    complex_dropdown_item_css_selector_fmt = 'span[title=\'{}\']'
    for d_complex_config in config.l_2_complex_eximport:
        print('d_complex_config:{}'.format(d_complex_config))
        to_import_tbl_name = config.tbl_prefix + d_complex_config['to_import_tbl_name']

        init(d_complex_config, driver)

        diagram_css = d_complex_config['div_cssfmt']
        css_cap = d_complex_config['div_cap']

        for date in d_complex_config['dates']:
            if isinstance(date['value'], str):
                str_input = date['value']
            else:
                str_input = date['value']()
            # input = wait_until(True, 'input:{} to find'.format(date['input_name']), find_element_by_class_id, driver, 'input', date['input_id'])
            # input = wait_until(True, 'input:{} to find'.format(date['input_name']), driver.find_element_by_id, date['input_id'])
            input = wait_until(True, 'input:{} to find'.format(date['input_name']), driver.find_element_by_xpath,
                               complex_input_date_xpath_fmt.format(date['input_prop_value']))
            input.click()
            input.send_keys(str_input)

        l_l_item_revref = []
        menu_index = 0
        for dropdown in d_complex_config['dropdowns']:
            menu_caption = dropdown['div_caption']
            menu_class = dropdown['div_class']
            menu_col_2_select = dropdown['col_2_select']
            menu_item_default = None
            l_item_revref = []
            for item_caption in dropdown['drop_items']:
                item_revref = {
                    'item_caption': item_caption,
                    'revref': {
                        'menu_index': menu_index,
                        'menu_init_caption': menu_caption,
                        'menu_class': menu_class,
                        'menu_col_2_select': menu_col_2_select,
                        'menu_item_default': menu_item_default,
                    }
                }
                l_item_revref.append(item_revref)
            l_l_item_revref.append(l_item_revref)
            menu_index += 2

        url = env_config.mssql_url + d_complex_config['to_import_db_name'] + env_config.url_suffix
        engine = sqlalchemy.create_engine(url, echo=True)
        sql_truncate = 'DELETE FROM {}'.format(to_import_tbl_name)
        conn = engine.connect()
        conn.execute(sql_truncate)
        conn.close()
        print('table truncated')

        l_tuple_item_combination = list(itertools.product(*l_l_item_revref))
        d_menu_index_2_last_item_caption = {}
        for tuple_item in l_tuple_item_combination:
            d_col_2_append = {}

            #init(d_complex_config, driver)

            for item in tuple_item:
                item_revref = item['revref']
                item_caption = item['item_caption']
                d_col_2_append[item_revref['menu_col_2_select']] = item_caption
                #menu_caption = item_revref['menu_init_caption']
                changed_menu_caption = d_menu_index_2_last_item_caption.get(item_revref['menu_index'])
                menu_caption = item_revref['menu_init_caption'] if changed_menu_caption is None else changed_menu_caption
                d_menu_index_2_last_item_caption[item_revref['menu_index']] = item_caption
                ele_menu = wait_until(True, 'menu:{} to find'.format(menu_caption), find_element_by_classname_cap,
                                      driver, item_revref['menu_class'], menu_caption)
                ele_menu.click()
                sleep(1)
                ele_item = wait_until(True, 'item:{} to find'.format(item_caption), driver.find_element_by_css_selector, complex_dropdown_item_css_selector_fmt.format(item_caption))
                ele_item.click()
                sleep(1)
            download(driver, diagram_css, False, css_cap, to_import_tbl_name, False, d_col_2_append)

    driver.quit()

