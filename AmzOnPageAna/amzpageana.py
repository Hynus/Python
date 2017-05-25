# coding:utf-8
import urllib
import urllib2
import Image
import cStringIO
import os
from pyquery import PyQuery as pq

# 指定并爬取特定页面——————————————————————————————————————————————————————
def get_the_url_page(pdt_asin, filename):
    url = "https://www.amazon.com/dp/" + pdt_asin
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'name': 'Sunyh',
              'location': 'pythontab',
              'language': 'Python'}
    headers = {'User-Agent': user_agent}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    amz_pdt_page = pq(the_page)
    f = open(filename, 'w+')
    f.write('###############################################################\n')
    f.close()
    print "###############################################################"
    return amz_pdt_page
# —————————————————————————————————————————————————————————————————————

# 获取标题及长度—————————————————————————————————————————————————————————
def get_title(amz_pdt_page, filename):
    pdt_title = amz_pdt_page("#productTitle").text()
    pdt_title_size = len(pdt_title)
    print "The length of product's title is: " + str(pdt_title_size) + "!"
    f = open(filename, 'a')
    f.write("The length of product's title is: " + str(pdt_title_size) + "!\n")
    f.write('###############################################################\n')
    f.close()
    print "###############################################################"
    return pdt_title
# —————————————————————————————————————————————————————————————————————

# 获取bullet point及数量————————————————————————————————————————————————
def get_bullet_points(amz_pdt_page, filename):
    bullet_pt_pq = amz_pdt_page("#feature-bullets").find("li").not_("#replacementPartsFitmentBullet")
    bullet_pt_text = amz_pdt_page("#feature-bullets").find("li").not_("#replacementPartsFitmentBullet").text()
    bullet_pt_pq_size = len(bullet_pt_pq)
    bullet_pt_arr = []
    for temp_li in bullet_pt_pq.items():
        bullet_pt_arr.append(temp_li.text())             # 获取产品大体情况描述信息字符串列表
    print "There are " + str(bullet_pt_pq_size) + " points in the product's bullet!"
    print "###############################################################"
    f = open(filename, 'a')
    f.write("There are " + str(bullet_pt_pq_size) + " points in the product's bullet!\n")
    f.write("###############################################################\n")
    f.close()
    return bullet_pt_text
# ————————————————————————————————————————————————————————————————————

# 获取产品描述字符数量———————————————————————————————————————————————————
def get_details(amz_pdt_page, filename):
    # 第一部分：获取商品详情信息
    pdt_desp_pq = amz_pdt_page("#productDescription").find("p")
    pdt_desp_text = amz_pdt_page("#productDescription").find("p").text()
    pdt_desp_size1 = len(pdt_desp_text)
    # pdt_desp_arr = []
    # for temp_p in pdt_desp_pq.items():
    # pdt_desp_arr.append(temp_p.text())               # 获取产品详情描述信息字符串列表

    # 第二部分：获取商品详情表格信息
    pdt_details_table_pq = amz_pdt_page("#prodDetails").find(".pdTab")
    if len(pdt_details_table_pq) == 0:
        tem_pdt_details_table_text = amz_pdt_page("#productDetails_detailBullets_sections1").text()
        if len(tem_pdt_details_table_text) == 0:
            pass
        else:
            pd_start_spilt_idx = tem_pdt_details_table_text.find('Customer Reviews')
            pd_end_spilt_idx = tem_pdt_details_table_text.rfind('stars')
            pdt_details_table_text = tem_pdt_details_table_text[:pd_start_spilt_idx] + \
                                     tem_pdt_details_table_text[pd_end_spilt_idx + 5:]
            pdt_desp_size2 = len(pdt_details_table_text)
    else:
        tem_pdt_details_table_text = pdt_details_table_pq.text()
        pd_start_spilt_idx = tem_pdt_details_table_text.find('Customer Reviews')
        pd_end_spilt_idx = tem_pdt_details_table_text.rfind('stars')
        pdt_details_table_text = tem_pdt_details_table_text[:pd_start_spilt_idx] + \
                                 tem_pdt_details_table_text[pd_end_spilt_idx + 5:]  # 获取产品详情表格信息字符长度
        pdt_desp_size2 = len(pdt_details_table_text)

    pdt_desp_total_size = pdt_desp_size1 + pdt_desp_size2  # 获取商品描述字符总数量
    print "The total lengh of the product's detail is: " + str(pdt_desp_total_size) + "!"
    print "###############################################################"
    f = open(filename, 'a')
    f.write("The total lengh of the product's detail is: " + str(pdt_desp_total_size) + "!\n")
    f.write("###############################################################\n")
    f.close()
    return pdt_desp_text, pdt_details_table_text
# ————————————————————————————————————————————————————————————————————

# 获取当前页面的图片数量及分辨率——————————————————————————————————————————
def get_images(amz_pdt_page, filename):
    img_block = amz_pdt_page("#imageBlock").find("img")
    img_urls = []
    f = open(filename, 'a')
    for sub_block in img_block.items():
        img_urls.append(sub_block.attr('src'))
    img_size_list = []
    i = 1
    for tem_url in img_urls:
        img_file = cStringIO.StringIO(urllib2.urlopen(tem_url).read())
        imgs = Image.open(img_file)
        img_size_list.append(imgs.size)
        print "The No." + str(i) +" image's infomation is got!!!"
        f.write("The No." + str(i) +" image's infomation is got!!!\n")
        i += 1
    if (1,1) in img_size_list:
        img_size_list.remove((1,1))
    img_number = len(img_size_list)
    print "There are " + str(img_number) + " pictures in current page!"
    f.write("There are " + str(img_number) + " pictures in current page!\n")
    print "The size of these pictures are as followed:   (width, height)"
    f.write("The size of these pictures are as followed:   (width, height)\n")
    for a_img in img_size_list:
        print a_img
        f.write(str(a_img)+"\n")
    print "###############################################################"
    f.write("###############################################################\n")
    f.close()
# ————————————————————————————————————————————————————————————————————

# 判断关键字是否出现在标题，五点描述，产品描述中————————————————————————————
def judge_keyword(pdt_title, bullet_pt_text, pdt_desp_text, pdt_details_table_text, amz_search_keyword, filename):
    amz_search_words_list = amz_search_keyword.split(" ")
    f = open(filename, 'a')
    count_num = 0
    for wordi in amz_search_words_list:
        tag_in_pdt_title = pdt_title.lower().find(wordi.lower())
        if tag_in_pdt_title != -1:
            print "The keyword '" + wordi +"' can be found in the product's title!"
            f.write("The keyword '" + wordi +"' can be found in the product's title!\n")
        tag_in_pdt_bullet = bullet_pt_text.lower().find(wordi.lower())
        if tag_in_pdt_bullet != -1:
            print "The keyword '" + wordi +"' can be found in the product's bullet!"
            f.write("The keyword '" + wordi +"' can be found in the product's bullet!\n")
        tag_in_pdt_details1 = pdt_desp_text.lower().find(wordi.lower())
        tag_in_pdt_details2 = pdt_details_table_text.lower().find(wordi.lower())
        if (tag_in_pdt_details1 != -1) or (tag_in_pdt_details1 != -1):
            print "The keywords '" + wordi +"' can be found in the product's details!"
            f.write("The keyword '" + wordi +"' can be found in the product's details!\n")
        if tag_in_pdt_title == tag_in_pdt_bullet == tag_in_pdt_details1 == tag_in_pdt_details2 == -1:
            print "The keyword '" + wordi +"' can't be found anywhere!!"
            f.write("The keyword '" + wordi +"' can't be found anywhere!!\n")
        count_num += 1
        print "------THE NO." + str(count_num) +" KEYWORD SEARCHING COMPLETED!-----"
        f.write("------THE NO." + str(count_num) +" KEYWORD SEARCHING COMPLETED!-----\n")
    print "###############################################################"
    f.write("###############################################################\n")
    f.close()
# ————————————————————————————————————————————————————————————————————

# 产品星级以及产品的评价数量——————————————————————————————————————————————
def get_reviews(amz_pdt_page, filename):
    f = open(filename, 'a')
    judge_txt = amz_pdt_page("#dp-no-customer-review-yet").text()
    if len(judge_txt) != 0:
        print judge_txt
        f.write(judge_txt+"\n")
    else:
        pdt_review_pq = amz_pdt_page("#reviewSummary").find(".a-row.a-spacing-small")
        pdt_review_stars = pdt_review_pq.eq(0).text()
        print "The overall reviews is: " + pdt_review_stars + "!" # 产品星级
        f.write("The overall reviews is: " + pdt_review_stars + "!\n")
        review_people_count = amz_pdt_page("#reviewSummary").find(".a-size-medium.totalReviewCount").eq(0).text()
        review_star_details = pdt_review_pq.eq(1).text()
        tem_review_star_list = review_star_details.split("%")[:5]
        review_star_list = []
        for items_in_rs in tem_review_star_list:
            items_in_rs += '%'
            review_star_list.append(items_in_rs)
        review_star_list[0] = ' ' + review_star_list[0]

        print "There are " + review_people_count + " customer reviews!"  # 评价人数及分别评级占比详情
        f.write("There are " + review_people_count + " customer reviews!\n")
        print "The details are as follow:"
        f.write("The details are as follow:\n")
        for starItem in review_star_list:
            print starItem
            f.write(starItem + "\n")
    print "###############################################################"
    f.write("###############################################################\n")
    f.close()
# ————————————————————————————————————————————————————————————————————


# 判断产品是否是fulfilled by amazon—————————————————————————————————————
def judge_ful_byamz(amz_pdt_page, filename):
    f = open(filename, 'a')
    merchant_info = amz_pdt_page("#merchant-info").eq(0).text().lower()
    idx_f = merchant_info.find('fulfilled by amazon')
    idx_d = merchant_info.find('sold by amazon')
    if idx_f != -1 or idx_d != -1:
        print "The product is fulfilled by Amazon!"
        f.write("The product is fulfilled by Amazon!\n")
    else:
        print "The is not fulfilled by Amazon!"
        f.write("The is not fulfilled by Amazon!\n")
    print "#############################################################"
    f.write("###############################################################\n")
    f.close()
# ————————————————————————————————————————————————————————————————————



def run_main():
    pdt_asin = raw_input("Please enter a product's ASIN code: ")
    amz_search_keyword = raw_input("Please enter the keywords you want to search: ")
    filename = "Product_" + pdt_asin + ".txt"
    amz_pdt_page = get_the_url_page(pdt_asin, filename)
    pdt_title = get_title(amz_pdt_page, filename)
    bullet_pt_text = get_bullet_points(amz_pdt_page, filename)
    pdt_desp_text, pdt_details_table_text = get_details(amz_pdt_page, filename)
    get_images(amz_pdt_page, filename)
    judge_keyword(pdt_title, bullet_pt_text, pdt_desp_text, pdt_details_table_text, amz_search_keyword, filename)
    get_reviews(amz_pdt_page, filename)
    judge_ful_byamz(amz_pdt_page, filename)


if __name__=="__main__":
    run_main()
