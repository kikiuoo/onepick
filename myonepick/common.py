def getPageList ( nowPage, allPage) :

    sPage = nowPage - 2
    if sPage <= 0 :
        startPage = 1
    elif sPage + 4 > allPage :
        startPage = allPage - 4
    else :
        startPage = sPage

    ePage = 1
    if allPage < 5 :
        ePage = allPage
    elif startPage + 4 > allPage :
        ePage = allPage
    else :
        ePage = startPage + 4

    paging = list(range(int(startPage), int(ePage)+1))

    return paging