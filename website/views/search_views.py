from django.shortcuts import render
from django.db import connection
from django.utils import timezone

from picktalk.models import *
from myonepick.common import *

# Create your views here.
def searchList(request, search) :

    nUrl = nowDevice(request)

    try:
        cursor = connection.cursor()
        user = request.session.get('id', '')

        # 검색 결과 등록
        nowTime = timezone.now()
        saveSearch = UserSearch.objects.create(userid=user, search=search, regdate=nowTime)

        query = "SELECT * " \
                "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                "where ( ai.isDelete = '0' or ai.isDelete is null ) " \
                "     and ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                                                                                                                                                                                                                                      "ORDER BY ai.regTime DESC ";

        result = cursor.execute(query)
        all_audi = cursor.fetchall()

        if user:
            query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.logoImage, DATEDIFF(NOW(),  ai.regTime) AS diffDate, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = ai.num ) AS audiPick " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                    "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                    "where ( ai.isDelete = '0' or ai.isDelete is null ) " \
                    "     and ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                    "ORDER BY ai.regTime DESC limit 5"
        else:
            query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.logoImage, DATEDIFF(NOW(),  ai.regTime) AS diffDate , '0' AS audiPick " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                    "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                    "where ( ai.isDelete = '0' or ai.isDelete is null ) " \
                    "     and ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                    "ORDER BY ai.regTime DESC  limit 5 "\

        result = cursor.execute(query)
        search_audi = cursor.fetchall()

        query = "SELECT * " \
                "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS c ON p.num = c.profileNum " \
                "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS d ON p.num = d.profileNum " \
                "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                "ORDER BY regDate DESC "

        result = cursor.execute(query)
        all_profile = cursor.fetchall()

        if user:
            query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS c ON p.num = c.profileNum " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS d ON p.num = d.profileNum " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                    "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                    "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                    "ORDER BY regDate DESC limit 4 "

        else:
            query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS c ON p.num = c.profileNum " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS d ON p.num = d.profileNum " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                    "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                    "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                    "ORDER BY regDate DESC LIMIT 4"


        print( query )


        result = cursor.execute(query)
        search_pro = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
       connection.rollback()

    return render(request, nUrl +  '/search/search.html',
                  { "search_audi": search_audi, "search_pro": search_pro, "search":search,
                    "all_audi" : len(all_audi) , "all_profile" : len(all_profile) })



def searchDetail_audi(request, search, page) :

    nUrl = nowDevice(request)

    try:
        cursor = connection.cursor()
        user = request.session.get('id', '')

        block = 10
        start = (int(page) - 1) * block
        end = int(page) * block

        query = "SELECT * " \
                "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                "where ( ai.isDelete = '0' or ai.isDelete is null ) " \
                "     and ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                "ORDER BY ai.regTime DESC ";

        result = cursor.execute(query)
        allList = cursor.fetchall()

        if user:
            query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.logoImage, DATEDIFF(NOW(),  ai.regTime) AS diffDate, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = ai.num ) AS audiPick " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                    "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                    "where ( ai.isDelete = '0' or ai.isDelete is null ) " \
                    "     and ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                    "ORDER BY ai.regTime DESC limit " + str(start) + ", " + str(block)
        else:
            query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.logoImage, DATEDIFF(NOW(),  ai.regTime) AS diffDate , '0' AS audiPick " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                    "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                    "where ( ai.isDelete = '0' or ai.isDelete is null ) " \
                    "     and ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                    "ORDER BY ai.regTime DESC limit " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        searching = cursor.fetchall()

        connection.commit()
        connection.close()

        allPage = int(len(allList) / block) + 1
        paging = getPageList_v2(page, allPage)

    except:
        connection.rollback()

    return render(request, nUrl + '/search/search_audi.html',
                  {"cateType": "audi", "searching": searching, "search":search, "paging":paging, "page" : page,
                   "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage,"allList":len(allList)})


def searchDetail_pro(request, search) :

    nUrl = nowDevice(request)

    try:
        cursor = connection.cursor()

        user = request.session.get('id', '')

        page = request.GET.get("page", "1")
        page = int(page)

        order = request.GET.get('order', "")

        nationality = request.GET.get('nationality', "")
        geneder = request.GET.get('geneder', "")
        military = request.GET.get('military', "")

        ageRadio = request.GET.get('ageRadio', "")
        age1 = request.GET.get('age1', "")
        age2 = request.GET.get('age2', "")

        heightRadio = request.GET.get('heightRadio', "")
        height1 = request.GET.get('height1', "")
        height2 = request.GET.get('height2', "")

        careerRadio = request.GET.get('careerRadio', "")
        career1 = request.GET.get('career1', "")
        career2 = request.GET.get('career2', "")

        foreSpec = request.GET.get('foreSpec', "")
        findSpec = request.GET.get('findSpec', "")
        tagSpec = request.GET.get('tagSpec', "")
        school = request.GET.get('school', "")

        where = ""
        if nationality != "":
            where = where + " and nationality='" + nationality + "'"

        if military != "":
            where = where + " and military='" + military + "'"

        if geneder != "":
            where = where + " and gender='" + geneder + "'"

        if ageRadio != "":
            nowTime = str(timezone.now())
            year = nowTime.split('-')
            if ageRadio == "1":
                year10 = int(year[0]) - 9
                where = where + " and birth >= '" + str(year10) + "-12-31' "
            else:
                yearsOver = int(year[0]) - int(ageRadio) + 1
                where = where + " and birth <= '" + str(yearsOver) + "-12-31' "
        elif age1 != "" and age2 != "":
            nowTime = str(timezone.now())
            year = nowTime.split('-')
            age_1 = int(year[0]) - int(age1) + 1
            age_2 = int(year[0]) - int(age2) + 1
            where = where + " and birth >= '" + str(age_1) + "-01-01' and birth <= '" + str(age_2) + "-12-31' "
        elif age1 != "" or age2 != "":
            age1 = ""
            age2 = ""

        if heightRadio != "":
            where = where + " and height >= '" + heightRadio + "' "
        elif height1 != "" and height2 != "":
            where = where + " and height >= '" + str(height1) + "' and height <= '" + str(height2) + "' "
        elif height1 != "" or height2 != "":
            height1 = ""
            height2 = ""

        if careerRadio != "":
            if careerRadio == "0":
                where = where + " and isCareer = '0' and ( careerYear < '1' or careerYear is null ) "
            else:
                where = where + " and isCareer = '0' and careerYear >= " + str(careerRadio) + " "
        elif career1 != "" and career2 != "":
            where = where + " and isCareer = '0' and careerYear >= '" + str(career1) + "' and careerYear <= '" + str(career2) + "'"
        elif career1 != "" or career2 != "":
            career1 = ""
            career2 = ""

        if foreSpec != "":
            foreign = foreSpec.split("|")

            where = where + " and ( "
            count = 0
            for fore in foreign:
                count = count + 1
                if count == 1:
                    where = where + " `foreign` like '%" + fore + "%' "
                else:
                    where = where + " or `foreign` like '%" + fore + "%' "

            where = where + " ) "

        else:
            foreign = ""

        if findSpec != "":
            specList = findSpec.split("|")

            where = where + " and ( "
            count = 0
            for spec in specList:
                count = count + 1
                specDetail = spec.split("$")
                if count == 1:
                    where = where + " talent like '%" + specDetail[1] + "%' "
                else:
                    where = where + " or talent like '%" + specDetail[1] + "%' "

            where = where + " ) "

        else:
            specList = ""

        if tagSpec != "":
            tagSpecList = tagSpec.split("|")

            where = where + " and ( "
            count = 0
            for tag in tagSpecList:
                count = count + 1
                if count == 1:
                    where = where + " tag like '%" + tag + "%' "
                else:
                    where = where + " or tag like '%" + tag + "%' "
            where = where + " ) "
        else:
            tagSpecList = ""

        if school != "":
            where = where + " and school like '%" + school + "%'"


        block = 10
        start = (int(page) - 1) * block
        end = int(page) * block

        query = "SELECT * " \
                "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS c ON p.num = c.profileNum " \
                "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS d ON p.num = d.profileNum " \
                "WHERE public = '0' and isDelete = '0'  and ui.userID != '' " + where + " and  " \
                "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                "ORDER BY regDate DESC "

        print(query)

        result = cursor.execute(query)
        allList = cursor.fetchall()

        if user:
            query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS c ON p.num = c.profileNum " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS d ON p.num = d.profileNum " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' " + where + " and  " \
                    "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                    "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                    "ORDER BY regDate DESC " \
                    " LIMIT " + str(start) + ", " + str(block)
        else:
            query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS c ON p.num = c.profileNum " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS d ON p.num = d.profileNum " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' " + where + " and  " \
                    "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                    "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                    "ORDER BY regDate DESC  " \
                    " LIMIT " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        searching = cursor.fetchall()

        query = "SELECT * FROM profile_specialty GROUP BY `class` ORDER BY num ASC"

        result = cursor.execute(query)
        specialty = cursor.fetchall()

        connection.commit()
        connection.close()

        allPage = int(len(allList) / block) + 1
        paging = getPageList_v2(page, allPage)

    except:
        connection.rollback()

    tagList = ProfileTag.objects.all().order_by("tag")

    return render(request, nUrl +  '/search/search_profile.html',
                  {"cateType": "profile", "searching": searching, "search":search, "paging":paging, "page" : page,
                   "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage,"allList":len(allList),
                   "nationality": nationality, "geneder": geneder, "military": military, "ageRadio": ageRadio
                   , "age1": age1, "age2": age2, "school": school, "heightRadio": heightRadio, "height1": height1, "height2": height2
                      , "careerRadio": careerRadio, "career1": career1, "career2": career2, "foreSpec": foreSpec, "findSpec": findSpec, "tagSpec": tagSpec,
                   "foreList": foreign, "spList": specList, "tagSpecList": tagSpecList, "speList": specialty, "tagList": tagList
                   })


def getSearchProfile(request) :

    nUrl = nowDevice(request)

    try :
        cursor = connection.cursor()

        page = request.GET['page']
        search = request.GET['word']

        page = int(page)

        user = request.session.get('id', '')
        block = 10
        start = (page - 1) * block
        end = page * block

        if user:
            query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS c ON p.num = c.profileNum " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS d ON p.num = d.profileNum " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                    "      ( ui.name LIKE '%" + search + "%' OR  career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                    "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                    "ORDER BY regDate DESC " \
                    " LIMIT " + str(start) + ", " + str(block)

        else:
            query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS c ON p.num = c.profileNum " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS d ON p.num = d.profileNum " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                    "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                    "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                    "ORDER BY regDate DESC  " \
                    " LIMIT " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        searching = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render(request, nUrl + 'profiles/ajax_profileList.html', {'profiles':searching})

