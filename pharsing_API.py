from bs4 import BeautifulSoup
from selenium import webdriver

# driver = webdriver.Chrome('\\Users\\dlxor\\Desktop\\melee\\Develop\\chromedriver')

driver = webdriver.Firefox(executable_path='C:\\Users\\dlxor\\Desktop\\melee\\Develop\\geckodriver.exe')
driver.implicitly_wait(3)


def url(ss, page):
    return 'http://overwatch.inven.co.kr/overank/rank/all/season' + str(ss) + '/summary/all/page/' + str(page)


def get_user_url(_id, _season):
    return 'http://overwatch.inven.co.kr/overank/profile/' + str(_id) + '/season/' + str(_season)


def get_url_html_soup(url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_user_list(soup):
    user_data = []
    _list = soup.find_all('td', {'class': 'col1'})
    a = 1
    for i in _list:
        temp_list = []
        for season in range(1, 8):
            temp_list.append(get_user_data(get_user_url(i.find('a').get('data-pidx'), season+1)))
        user_data.append(temp_list)
        print(a)
        a += 1
    return user_data


def get_user_data(url):
    soup = get_url_html_soup(url)
    top_data = soup.find('div', {'class': 'bb_dataBox'})
    return top_data


max_page_list = [6466, 5014, 4149, 3094]
season = 5
current_worked_page = 51
f = open("C:\\Users\\dlxor\\Desktop\\python_projects\\overwatch_dataset3.txt", 'a')
for n in range(current_worked_page, max_page_list[season-2]):
    print('Season: ', season, 'Page: ', n)
    f.write(n)
    data_list = []
    user_url_list = get_user_list(get_url_html_soup(url(season, n)))
    for i in range(len(user_url_list)):
        if len(user_url_list[i]) < 2:
            continue
        for k in range(len(user_url_list[i])):
            # index 0: 최고점수, 1: 총 게임 수, 2: 승률, 3: KDA
            for j in range(4):
                data = user_url_list[i][k].find_all('div', {'class': 'bb_topData'})

                if len(data) == 3 or data[1].find('span').get_text() == '0':  # 빠대 전적 or 언랭
                    break

                data_list.append(data[j+1].find('span').get_text())
        # if data_list[len(data_list)-1] == '\n' or data_list[len(data_list)-5] == '\n':  # 전적이 한 시즌도 없거나 한 시즌
            # continue
        data_list.append('\n')  # 플레이어간 구분

    print(data_list)
    index = 0
    write_text = ''
    for i in range((len(data_list) - 50) // 4):  # 수정필요 3/2
        if data_list[index] == '\n':
            index = index+1
            continue
        if data_list[index] == '':
            index = index+4
            continue
        _str = ''
        it = 0
        for text in data_list[index:index+5]:
            _str = _str + text
            it += 1
            if it == 5:
                write_text = _str
                break
            _str = _str + ','
        print(index)
        print(write_text)
        if write_text[len(write_text)-1] != '\n':
            f.write(write_text + '\n')
        index = index + 4

f.close()



