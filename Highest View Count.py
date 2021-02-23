from selenium import webdriver
import time

driver = webdriver.Chrome('./chromedriver')   #크롬 실행
ch = 'n'

login_url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
driver.get(login_url)   #로그인 페이지로 이동
time.sleep(1)

id = input('ID를 입력하세요 : ')
pw = input('비밀번호를 입력하세요 : ')

driver.execute_script("document.getElementsByName('id')[0].value = \'" + id + "\'")
driver.execute_script("document.getElementsByName('pw')[0].value = \'" + pw + "\'")
time.sleep(1)

driver.find_element_by_id('log.login').click()
time.sleep(1)

blog_url = 'https://blog.naver.com/PostList.nhn?blogId=kjsjsj1109&categoryNo=0&from=postList'
driver.get(blog_url)   #블로그로 이동
time.sleep(1)

driver.find_element_by_xpath('//*[@id="category-name"]/div/table[2]/tbody/tr/td[2]/div/a').click()   #목록 열기
time.sleep(1)

title_list = []   #제목 리스트
count_list = []   #조회수 리스트
pages = driver.find_elements_by_css_selector('.page.pcol2._goPageTop')   #전체 페이지 수 가져오기
page = 1

titles = driver.find_elements_by_css_selector('a.pcol2._setTop._setTopListUrl')   #1페이지 게시글 제목 가져오기
counts = driver.find_elements_by_css_selector('a.pcol2.aggregate_click_delegate')   #1페이지 게시글 조회수 가져오기

for t in titles:
    title_list.append(t.text)   #1페이지 제목 입력

for c in counts:
    count_list.append(c.text)   #1페이지 조회수 입력
    
for p in pages:   #전체 페이지 수만큼 반복
    driver.find_element_by_xpath('//*[@id="toplistWrapper"]/div[2]/div/a[%s]'%page).click()   #다음페이지로 이동
    time.sleep(1)
    
    titles = driver.find_elements_by_css_selector('a.pcol2._setTop._setTopListUrl')   #해당 페이지 제목 가져오기
    counts = driver.find_elements_by_css_selector('a.pcol2.aggregate_click_delegate')   #해당 페이지 조회수 가져오기

    for t in titles:
        title_list.append(t.text)   #해당 페이지 제목 입력

    for c in counts:
        count_list.append(c.text)   #해당 페이지 조회수 입력

    page += 1   #페이지 수 증가
driver.close()   #크롬 종료

max = int(count_list[0])   #첫번째 값을 최대값으로 가정
num = 0

for i in range(1, len(title_list)):   #게시글 수 만큼 반복하며
    if int(count_list[i]) > max:   #현재 조회수와 max값을 비교
        max = int(count_list[i])   #최대값을 max에 저장
        num = i   #몇 번째 요소인지 num에 저장

for i in range(0, len(title_list)):
    print(title_list[i] + ' : ' + count_list[i])   #전체 게시글의 제목과 조회수 출력
    
print('조회수가 가장 높은 게시글은 "{}"입니다.(총 {}번 조회)'.format(title_list[num], max))   #가장 높은 조회수의 게시글과 조회수 출력
