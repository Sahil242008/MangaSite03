from flask import Blueprint, render_template_string, request
from requests import get
from bs4 import BeautifulSoup

bp = Blueprint('main', __name__)

def homePageData(n):
    url = f"https://manhwabtt.com/?page={n}&typegroup=0"
    p = get(url).text
    soup = BeautifulSoup(p, "lxml")
    data = soup.find_all("div", class_='ModuleContent')
    mangasContent = data[4]
    mangas = mangasContent.find_all('div', class_='item')

    content = ""
    for manga in mangas:
        a_tag = manga.find('a')
        linkFull = a_tag['href']
        baseUrl = 'https://manhwabtt.com/manga/'
        link = linkFull.replace(baseUrl, '')
        title = a_tag['title']
        img_tag = a_tag.find('img')
        image = img_tag['src']
        img_value = f'<a href="/infoPage?link={link}" title="{title}"><img alt="{title}" src="{image}"/></a><h3><a class="" href="/infoPage?link={link}">{title}</a></h3>'

        chapters = manga.find('ul')
        chapters = chapters.find_all('li')
        
        for chap in chapters:
            a_tag2 = chap.find('a')
            link2Full = a_tag2['href']
            link2 = link2Full.replace(baseUrl, '')
            title2 = a_tag2['title']
            time = chap.find('i', class_='time').text
            chap_link = f'<li class=""><a href="/chapterPage?link={link2}" title="{title2}">{title2} </a><i class="">{time}</i></li>'
            img_value += chap_link

        content += img_value

    return content

@bp.route('/', methods=['GET', 'POST'])
def home():
    n = int(request.args.get('page', 1))
    content = homePageData(n)

    home_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Manga Home</title>
        <style>
            .nav-buttons {
                margin-top: 20px;
                text-align: center;
            }
            .nav-buttons form {
                display: inline;
            }
            .nav-buttons button {
                padding: 10px 15px;
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .nav-buttons button:hover {
                background-color: #e0a800;
            }
            .hidden {
                display: none;
            }
            .search-form {
                text-align: center;
                margin-bottom: 20px;
            }
            .search-form input[type="text"] {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
                width: 60%;
                margin-right: 10px;
            }
            .search-form button {
                padding: 10px 15px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                cursor: pointer;
            }
            .search-form button:hover {
                background-color: #0056b3;
            }
        .home-button {
                //position: fixed;
                top: 10px;
                right: 10px;
            }
            .home-button form {
                display: inline;
            }
            .home-button button {
                padding: 10px 15px;
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .home-button button:hover {
                background-color: #e0a800;
            }
        </style>
    </head>
    <body>
<br>
<div class="home-button">
            <form action="/" method="get">
                <button type="submit">Home</button>
            </form>
        </div>
    
    <div class="search-form">
            <form action="/searchPage" method="get">
                <input type="text" name="query" placeholder="Search..." value="">
                <button type="submit">Search</button>
            </form>
        </div>
        <div class="manga-content">
            {{ content|safe }}
        </div>
        <div class="nav-buttons">
            {% if page > 1 %}
            <form action="/" method="get">
                <input type="hidden" name="page" value="{{ page - 1 }}">
                <button type="submit">Previous Page</button>
            </form>
            {% endif %}
            <form action="/" method="get">
                <input type="hidden" name="page" value="{{ page + 1 }}">
                <button type="submit">Next Page</button>
            </form>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(home_template, content=content, page=n)

@bp.route('/infoPage', methods=['GET', 'POST'])
def infoPage():
    link = request.args.get('link')
    fullTitle, imageUrl, summary, allChaptersLink = infoPageData(link)

    info_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ fullTitle }}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 90%;
                max-width: 800px;
                margin: auto;
                padding: 20px;
            }
            .title {
                text-align: center;
                font-size: 2em;
                margin-bottom: 20px;
            }
            .image {
                text-align: center;
                margin-bottom: 20px;
            }
            .image img {
                max-width: 100%;
                height: auto;
            }
            .about {
                margin-bottom: 20px;
            }
            .about h2 {
                font-size: 1.5em;
                margin-bottom: 10px;
            }
            .about p {
                font-size: 1em;
                line-height: 1.6;
            }
            .chapters {
                margin-bottom: 20px;
            }
            .chapters h2 {
                font-size: 1.5em;
                margin-bottom: 10px;
            }
            .chapters a {
                display: block;
                font-size: 1em;
                margin-bottom: 5px;
                color: #007bff;
                text-decoration: none;
            }
            .chapters a:hover {
                text-decoration: underline;
            }
            .search-form {
                text-align: center;
                margin-bottom: 20px;
            }
            .search-form input[type="text"] {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
                width: 60%;
                margin-right: 10px;
            }
            .search-form button {
                padding: 10px 15px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                cursor: pointer;
            }
            .search-form button:hover {
                background-color: #0056b3;
            }
           
        .home-button {
                //position: fixed;
                top: 10px;
                right: 10px;
            }
            .home-button form {
                display: inline;
            }
            .home-button button {
                padding: 10px 15px;
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .home-button button:hover {
                background-color: #e0a800;
            }
        </style>
    </head>
    <body>
<br>
<div class="home-button">
            <form action="/" method="get">
                <button type="submit">Home</button>
            </form>
        </div>
    <br>
    
    <div class="search-form">
            <form action="/searchPage" method="get">
                <input type="text" name="query" placeholder="Search..." value="">
                <button type="submit">Search</button>
            </form>
        </div>
        <div class="container">
            <div class="title">{{ fullTitle }}</div>
            <div class="image">
                <img src="{{ imageUrl }}" alt="{{ fullTitle }}">
            </div>
            <div class="about">
                <h2>About</h2>
                <p>{{ summary }}</p>
            </div>
            <div class="chapters">
                <h2>Chapters</h2>
                {{ allChaptersLink|safe }}
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(info_template, fullTitle=fullTitle, imageUrl=imageUrl, summary=summary, allChaptersLink=allChaptersLink)

def infoPageData(u):
    url = f'https://manhwabtt.com/manga/{u}'
    p = get(url).text
    soup = BeautifulSoup(p, "lxml")
    
    dataManga = soup.find('div', class_='detail-content')
    mangaData = soup.find('p', id="summary")
    summary = mangaData.text
    title = summary[:summary.find(' is a')]
    
    imageTag = soup.find('img', alt=title)
    imageUrl = imageTag['src']
    summary = summary.replace('https://manhwabtt.com', 'mySiteUrl')

    firstLastLink = soup.find('div', class_='read-action mrt10').find_all('a')
    lastLinkTag = str(firstLastLink[1])
    start = lastLinkTag.find('href="') + 6
    end = lastLinkTag.find('">')
    lastLink = lastLinkTag[start:end]

    p2 = get(lastLink).text
    soup2 = BeautifulSoup(p2, "lxml")
    options = soup2.find('select').find_all('option')
    allChaptersLink = ''
    Base_Url='https://manhwabtt.com/manga/'
    for option in options:
        linkToChapter = str(option['value']).replace(Base_Url, '')
        chapterNumber = option.text
        linkChap = f'<a href="/chapterPage?link={linkToChapter}" title="{chapterNumber}">{chapterNumber}</a><br>'
        allChaptersLink += linkChap
    
    return title, imageUrl, summary, allChaptersLink

def chapterPageData(u):
    url = f'https://manhwabtt.com/manga/{u}'
    p = get(url).text
    soup = BeautifulSoup(p, "lxml")
    
    mangaPageUrl = soup.find('h1', class_='txt-primary')
    title = mangaPageUrl.find('a')
    titleChapter = mangaPageUrl.find('span')
    fullTitle = title.text + ' ' + titleChapter.text
    
    options = soup.find('select').find_all('option')
    
    imgList = soup.find('div', class_='reading-detail box_doc')
    imgAll = imgList.find_all('div', class_='page-chapter')
    
    filtered_imgAll = [img for img in imgAll if img.get('id') != 'page_0']
    imgData = ""
    
    v = u.find('chapter-')
    w = u.find('-eng-li/')
    
    currentChapter = u[v:w]
    currentChapterNo = int(currentChapter[8:])
    nextChapterNo = f'Chapter {currentChapterNo + 1}'
    prevChapterNo = f'Chapter {currentChapterNo - 1}'
    nextChapterLink = None
    prevChapterLink = None
    Base_Url = 'https://manhwabtt.com/manga/'
    
    selectAll = """
    <form id="chapterSelectForm" action="/chapterPage" method="get">
        <select name="link" onchange="document.getElementById('chapterSelectForm').submit();" style="padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc;">
    """
    for option in options:
        linkToChapter = str(option['value']).replace(Base_Url, '')
        chapterNumber = option.text
        selected = 'selected' if f'chapter-{currentChapterNo}' in linkToChapter else ''
        selectAll += f'<option value="{linkToChapter}" {selected}>{chapterNumber}</option>'
        if chapterNumber == nextChapterNo:
            nextChapterLink = linkToChapter
        if chapterNumber == prevChapterNo:
            prevChapterLink = linkToChapter
        
    selectAll += "</select></form>"

    # Process each div and all images in chapter
    for img_div in filtered_imgAll:
        # Copy the div contents
        div_content = str(img_div)

        # For the last div, remove the specific img tag
        if img_div == filtered_imgAll[-1]:
            # Find and remove the specific img tag
            soup_div = BeautifulSoup(div_content, 'html.parser')
            specific_img = soup_div.find('img', class_='lazyload', src="https://image.mangabtt.com//Upload/Content/images/chapter/top.jpg")
            if specific_img:
                specific_img.decompose()
            div_content = str(soup_div)

        imgData += div_content
        
    return fullTitle, nextChapterLink, prevChapterLink, selectAll, imgData


@bp.route('/chapterPage', methods=['GET', 'POST'])
def chapterPage():
    link = request.args.get('link', 'reincarnation-of-the-swordmaster/chapter-20-eng-li/742103')
    fullTitle, nextChapterLink, prevChapterLink, selectAll, imgData = chapterPageData(link)

    chapter_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ fullTitle }}</title>
        <style>
            body {
                margin: 0;
                padding: 0;
            }
            .chapter-container {
                text-align: center;
                margin-bottom: 20px;
            }
            .chapter-title {
                font-size: 24px;
                margin-top: 20px;
            }
            .nav-buttons {
                margin-top: 20px;
                margin-bottom: 20px;
            }
            .nav-buttons form {
                display: inline;
            }
            .nav-buttons button {
                padding: 10px 15px;
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin: 0 10px;
            }
            .nav-buttons button:hover {
                background-color: #e0a800;
            }
            .chapter-images img {
                width: 100%;
                display: block;
            }
            .search-form {
                text-align: center;
                margin-bottom: 20px;
            }
            .search-form input[type="text"] {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
                width: 60%;
                margin-right: 10px;
            }
            .search-form button {
                padding: 10px 15px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                cursor: pointer;
            }
            .search-form button:hover {
                background-color: #0056b3;
            }
        .home-button {
                //position: fixed;
                top: 10px;
                right: 10px;
            }
            .home-button form {
                display: inline;
            }
            .home-button button {
                padding: 10px 15px;
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .home-button button:hover {
                background-color: #e0a800;
            }
        </style>
    </head>
    <body>
<br>
<div class="home-button">
            <form action="/" method="get">
                <button type="submit">Home</button>
            </form>
        </div>
    <br>
    <div class="search-form">
            <form action="/searchPage" method="get">
                <input type="text" name="query" placeholder="Search..." value="">
                <button type="submit">Search</button>
            </form>
        </div>
        <div class="chapter-container">
            <div class="chapter-title">{{ fullTitle }}</div>
            <div class="nav-buttons">
                {% if prevChapterLink %}
                <form action="/chapterPage" method="get">
                    <input type="hidden" name="link" value="{{ prevChapterLink }}">
                    <button type="submit">{{ prevChapterNo }}</button>
                </form>
                {% endif %}
                {% if nextChapterLink %}
                <form action="/chapterPage" method="get">
                    <input type="hidden" name="link" value="{{ nextChapterLink }}">
                    <button type="submit">{{ nextChapterNo }}</button>
                </form>
                {% endif %}
            </div>
            {{ selectAll|safe }}
            <div class="chapter-images">
                {{ imgData|safe }}
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(chapter_template, fullTitle=fullTitle, nextChapterLink=nextChapterLink, prevChapterLink=prevChapterLink, nextChapterNo=f'Chapter {int(link.split("chapter-")[1].split("-")[0]) + 1}', prevChapterNo=f'Chapter {int(link.split("chapter-")[1].split("-")[0]) - 1}', selectAll=selectAll, imgData=imgData)



def searchPageData(search_title, searchPageNumber):
    title_lower = search_title.lower()
    title_formatted = title_lower.replace(' ', '+').replace('△', '').replace(':', '').replace('(', '').replace(')', '').replace('.', '').replace('!', '').replace(',', '').replace('?', '').replace('~', '')
    searchUrl = f'https://manhwabtt.com/find-story?keyword={title_formatted}&page={searchPageNumber}'
    
    p = get(searchUrl).text
    soup = BeautifulSoup(p, "lxml")
    data = soup.find_all("div", class_='ModuleContent')
    searchContents = data[3]
    allSearchPage = soup.find('ul', class_='pagination m0 tr-paging')
    allSearchPageData = allSearchPage.find_all('li') if allSearchPage else []

    prevNone, nextNone, prevPageUrl, nextPageUrl, pTitle, nTitle, pPageNum, nPageNum = None, None, None, None, None, None, None, None
    
    if allSearchPageData:
        prevNone = allSearchPage.find('li', class_='previous disabled')
        nextNone = allSearchPage.find('li', class_='next disabled')
        prevPage = allSearchPage.find('li', class_='previous')
        nextPage = allSearchPage.find('li', class_='next')
        
        if prevPage and not prevNone:
            prevPageUrl = prevPage.find('a')['href']
            i = prevPageUrl.find('keyword=')
            j = prevPageUrl.find('&page=')
            pTitle = prevPageUrl[i+8:j]
            pPageNum = prevPageUrl[j+6:]
        
        if nextPage and not nextNone:
            nextPageUrl = nextPage.find('a')['href']
            k = nextPageUrl.find('keyword=')
            l = nextPageUrl.find('&page=')
            nTitle = nextPageUrl[k+8:l]
            nPageNum = nextPageUrl[l+6:]
    
    mangas = searchContents.find_all('div', class_='item')
    Base_Url = 'https://manhwabtt.com/manga/'
    content = ""
    for manga in mangas:
        a_tag = manga.find('a')
        link = a_tag['href']
        link3 = str(link).replace(Base_Url, '')
        title = a_tag['title']
        img_tag = a_tag.find('img')
        image = img_tag['src']
        img_value = f'<a href="/infoPage?link={link3}" title="{title}"><img alt="{title}" src="{image}"/></a><h3><a class="" href="/infoPage?link={link3}">{title}</a></h3>'
        
        chapters = manga.find('ul').find_all('li')
        for chap in chapters:
            a_tag2 = chap.find('a')
            link2 = a_tag2['href']
            link4 = str(link2).replace(Base_Url, '')
            title2 = a_tag2['title']
            time = chap.find('i', class_='time').text
            chap_link = f'<li class=""><a href="/chapterPage?link={link4}" title="{title2}">{title2} </a><i class="">{time}</i></li>'
            img_value += chap_link

        content += img_value

    return content, prevNone, nextNone, prevPageUrl, nextPageUrl, pTitle, pPageNum, nTitle, nPageNum, allSearchPageData

@bp.route('/searchPage', methods=['GET', 'POST'])
def searchPage():
    query = request.args.get('query','')
    page = request.args.get('page',1)
    content, prevNone, nextNone, prevPageUrl, nextPageUrl, pTitle, pPageNum, nTitle, nPageNum, allSearchPageData = searchPageData(query, page)
    
    search_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search Results</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
            }
            .container {
                width: 80%;
                margin: 0 auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .search-form {
                text-align: center;
                margin-bottom: 20px;
            }
            .search-results {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
            }
            .search-item {
                width: 48%;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 20px;
                padding: 15px;
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            }
            .search-item img {
                max-width: 100%;
                border-radius: 5px;
            }
            .search-item h3 {
                font-size: 18px;
                margin: 10px 0;
            }
            .search-item ul {
                list-style: none;
                padding: 0;
            }
            .search-item li {
                font-size: 14px;
                margin: 5px 0;
            }
            .search-item a {
                text-decoration: none;
                color: #007bff;
            }
            .search-item a:hover {
                text-decoration: underline;
            }
            .pagination {
                text-align: center;
                margin: 20px 0;
            }
            .pagination form {
                display: inline;
            }
            .pagination button {
                padding: 10px 15px;
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin: 0 10px;
            }
            .pagination button:hover {
                background-color: #e0a800;
            }
            .search-form {
                text-align: center;
                margin-bottom: 20px;
            }
            .search-form input[type="text"] {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
                width: 60%;
                margin-right: 10px;
            }
            .search-form button {
                padding: 10px 15px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                cursor: pointer;
            }
            .search-form button:hover {
                background-color: #0056b3;
            }
        .home-button {
                //position: fixed;
                top: 10px;
                right: 10px;
            }
            .home-button form {
                display: inline;
            }
            .home-button button {
                padding: 10px 15px;
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .home-button button:hover {
                background-color: #e0a800;
            }
        </style>
    </head>
    <body>
<br>
<div class="home-button">
            <form action="/" method="get">
                <button type="submit">Home</button>
            </form>
        </div>
    <br>
    
        <div class="container">
            <div class="search-form">
                <form action="/searchPage" method="get">
                    <input type="text" name="query" placeholder="Search..." value="{{ query }}">
                    <button type="submit">Search</button>
                </form>
            </div>
            <div class="search-results">
                {{ content|safe }}
            </div>
            <div class="pagination">
                {% if allSearchPageData %}
                    {% if prevNone %}
                        <form action="/searchPage" method="get">
                            <input type="hidden" name="query" value="{{ nTitle }}">
                            <input type="hidden" name="page" value="{{ nPageNum }}">
                            <button type="submit">Next Page {{ nPageNum }}</button>
                        </form>
                    {% elif nextNone %}
                        <form action="/searchPage" method="get">
                            <input type="hidden" name="query" value="{{ pTitle }}">
                            <input type="hidden" name="page" value="{{ pPageNum }}">
                            <button type="submit">Previous Page {{ pPageNum }}</button>
                        </form>
                    {% else %}
                        <form action="/searchPage" method="get">
                            <input type="hidden" name="query" value="{{ pTitle }}">
                            <input type="hidden" name="page" value="{{ pPageNum }}">
                            <button type="submit">Previous Page {{ pPageNum }}</button>
                        </form>
                        <form action="/searchPage" method="get">
                            <input type="hidden" name="query" value="{{ nTitle }}">
                            <input type="hidden" name="page" value="{{ nPageNum }}">
                            <button type="submit">Next Page {{ nPageNum }}</button>
                        </form>
                    {% endif %}
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(search_template, query=query, content=content, prevNone=prevNone, nextNone=nextNone, prevPageUrl=prevPageUrl, nextPageUrl=nextPageUrl, pTitle=pTitle, pPageNum=pPageNum, nTitle=nTitle, nPageNum=nPageNum, allSearchPageData=allSearchPageData)

