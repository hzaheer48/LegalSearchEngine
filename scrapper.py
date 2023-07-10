'''
CA:606
CMA:120
CP:522
CONST.P:195
CRL.A:184
CRL.P:321
SMC:101

'''
import requests,os,win32com.client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from docx import Document
from docx.shared import Inches
import aspose.words as aw
from docx2pdf import convert
def get_judgements(case_types):
    my_dict = {}
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.supremecourt.gov.pk/judgement-search/#1573035933449-63bb4a39-ac81')
    for cases in case_types:
        if not os.path.exists(cases):
            os.makedirs(cases)
        select_element = Select(driver.find_element(By.ID,'case_type'))
        select_element.select_by_value(cases)
        search_result = driver.find_element(By.XPATH,'//input[@value="Search Result"]')
        search_result.click()
        jugdments_list = []
        while(True):
            time.sleep(5)
            history_body = driver.find_element(By.ID,'historyBody')
            tr_elements = history_body.find_elements(By.XPATH, './/tr')
            for row in tr_elements:
                if 'background: rgb(251, 251, 251);' in row.get_attribute('style'):
                    continue
                tds = row.find_elements(By.XPATH, './/td')
                jugdments_list.append((tds[0].text,tds[1].text,tds[3].text,tds[4].text,'.Dated: '+tds[6].text))
                pdf_url = tds[9].find_element(By.XPATH, './a').get_attribute('href')
                response = requests.get(pdf_url)
                with open(os.path.join(cases, cases+tds[0].text+'.pdf'), 'wb') as f:
                    f.write(response.content)
            next_page = driver.find_element(By.ID,'resultsTable_next')
            if 'disabled' in next_page.get_attribute('class') or len(jugdments_list)>250:
                my_dict[cases] = jugdments_list
                break
            else:
                next_page_link = next_page.find_element(By.TAG_NAME, 'a')
                actions = ActionChains(driver)
                actions.move_to_element(next_page_link).perform()
                driver.execute_script("window.scrollBy(0, 50);")
                next_page_link.click()
    driver.quit()
    return my_dict

def writing_to_txt(my_dict):
    with open('task1_document1.txt', 'w') as f:
        f.write('{:<25}{:<15}{:<100}\n'.format('Category/Class Name', 'Serial No.','Abstract Of Judgments'))
        for key in my_dict.keys():
            for i in range(len(my_dict[key])):
                if(i==0):            
                    f.write('{:<25}{:<15}{:<25}\n'.format(key, str(my_dict[key][i][0]),str(my_dict[key][i][1])))
                    list_of_words = my_dict[key][i][2]
                    words = list_of_words.split()
                    chunks = [' '.join(words[i:i+4]) for i in range(0, len(words), 4)]
                    for chunk in chunks:
                        f.write('{:<25}{:<15}{:<25}\n'.format('','',chunk))
                    f.write('{:<25}{:<15}{:<25}\n'.format('','',str(my_dict[key][i][3])))
                    f.write('{:<25}{:<15}{:<25}\n'.format('','',str(my_dict[key][i][4])))
                else:
                    f.write('{:<25}{:<15}{:<25}\n'.format('', str(my_dict[key][i][0]),str(my_dict[key][i][1])))
                    list_of_words = my_dict[key][i][2]
                    words = list_of_words.split()
                    chunks = [' '.join(words[i:i+4]) for i in range(0, len(words), 4)]
                    for chunk in chunks:
                        f.write('{:<25}{:<15}{:<25}\n'.format('','',chunk))
                    f.write('{:<25}{:<15}{:<25}\n'.format('','',str(my_dict[key][i][3])))
                    f.write('{:<25}{:<15}{:<25}\n'.format('','',str(my_dict[key][i][4])))
    with open('task1_document2.txt', 'w') as f:
        f.write('{:<25}{:<15}\n'.format('Category/Class Name', 'Number of Judgments'))
        for key in my_dict.keys():
            f.write('{:<25}{:<15}\n'.format(key, str(len(my_dict[key]))))

if __name__ == '__main__':
    case_types = ['C.A.','C.M.A.','C.P.','Const.P.','Crl.A.','Crl.P.','S.M.C.']
    my_dict = get_judgements(case_types)
    writing_to_txt(my_dict)