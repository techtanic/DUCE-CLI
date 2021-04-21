import json
import random
import re
from tqdm import tqdm
import threading
import time
import traceback
from urllib.parse import parse_qs, unquote, urlsplit
from decimal import Decimal
import requests
from bs4 import BeautifulSoup as bs
from colors import *


# DUCE-CLI

# Scraper
def discudemy():
    global du_links
    du_links = []
    big_all = []
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }

    for page in range(1, 4):
        r = requests.get("https://www.discudemy.com/all/" + str(page), headers=head)
        soup = bs(r.content, "html5lib")
        all = soup.find_all("section", "card")
        big_all.extend(all)
    du_bar = tqdm(total=len(big_all), desc="Discudemy")
    for index, items in enumerate(big_all):
        du_bar.update(1)
        try:
            title = items.a.text
            url = items.a["href"]

            r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            next = soup.find("div", "ui center aligned basic segment")
            url = next.a["href"]
            r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            du_links.append(title + "|:|" + soup.find("div", "ui segment").a["href"])
        except AttributeError:
            continue
    du_bar.close()


def udemy_freebies():
    global uf_links
    uf_links = []
    big_all = []

    for page in range(1, 3):
        r = requests.get(
            "https://www.udemyfreebies.com/free-udemy-courses/" + str(page)
        )
        soup = bs(r.content, "html5lib")
        all = soup.find_all("div", "coupon-name")
        big_all.extend(all)
    uf_bar = tqdm(total=len(big_all), desc="Udemy Freebies")

    for index, items in enumerate(big_all):
        uf_bar.update(1)
        title = items.a.text
        url = bs(requests.get(items.a["href"]).content, "html5lib").find(
            "a", class_="button-icon"
        )["href"]
        link = requests.get(url).url
        uf_links.append(title + "|:|" + link)
    uf_bar.close()


def tutorialbar():

    global tb_links
    tb_links = []
    big_all = []

    for page in range(1, 4):
        r = requests.get("https://www.tutorialbar.com/all-courses/page/" + str(page))
        soup = bs(r.content, "html5lib")
        all = soup.find_all(
            "div", class_="content_constructor pb0 pr20 pl20 mobilepadding"
        )
        big_all.extend(all)
    tb_bar = tqdm(total=len(big_all), desc="Tutorial Bar")

    for index, items in enumerate(big_all):
        tb_bar.update(1)
        title = items.a.text
        url = items.a["href"]

        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        link = soup.find("a", class_="btn_offer_block re_track_btn")["href"]
        if "www.udemy.com" in link:
            tb_links.append(title + "|:|" + link)
    tb_bar.close()

def real_discount():

    global rd_links
    rd_links = []
    big_all = []

    for page in range(1, 4):
        r = requests.get("https://app.real.discount/stores/Udemy?page=" + str(page))
        soup = bs(r.content, "html5lib")
        all = soup.find_all("div", class_="card-body")
        big_all.extend(all)
    rd_bar = tqdm(total=len(big_all), desc="Real Discount")

    for index, items in enumerate(big_all):
        rd_bar.update(1)
        title = items.a.h3.text
        url = "https://app.real.discount" + items.a["href"]
        r = requests.get(url)
        soup = bs(r.content, "html5lib")
        try:
            link = soup.select_one(
                "#panel > div:nth-child(4) > div:nth-child(1) > div.col-lg-7.col-md-12.col-sm-12.col-xs-12 > a"
            )["href"]
            if link.startswith("https://www.udemy.com"):
                rd_links.append(title + "|:|" + link)
        except:
            pass
    rd_bar.close()

def coursevania():

    global cv_links
    cv_links = []
    r = requests.get("https://coursevania.com/courses/")
    soup = bs(r.content, "html5lib")
    nonce = soup.find_all("script")[22].text[30:]
    nonce = json.loads(nonce[: len(nonce) - 6])["load_content"]
    r = requests.get(
        "https://coursevania.com/wp-admin/admin-ajax.php?&template=courses/grid&args={%22posts_per_page%22:%2230%22}&action=stm_lms_load_content&nonce="
        + nonce
        + "&sort=date_high"
    ).json()
    soup = bs(r["content"], "html5lib")
    all = soup.find_all("div", attrs={"class": "stm_lms_courses__single--title"})
    cv_bar = tqdm(total=len(all), desc="Course Vania")

    for index, item in enumerate(all):
        cv_bar.update(1)
        title = item.h5.text
        r = requests.get(item.a["href"])
        soup = bs(r.content, "html5lib")
        cv_links.append(
            title
            + "|:|"
            + soup.find("div", attrs={"class": "stm-lms-buy-buttons"}).a["href"]
        )
    cv_bar.close()

def idcoupons():

    global idc_links
    idc_links = []
    big_all = []
    for page in range(1, 4):
        r = requests.get(
            "https://idownloadcoupon.com/product-category/udemy-2/page/" + str(page)
        )
        soup = bs(r.content, "html5lib")
        all = soup.find_all("a", attrs={"class": "button product_type_external"})
        big_all.extend(all)
    idc_bar = tqdm(total=len(big_all), desc="IDownloadCopouns")

    for index, item in enumerate(big_all):
        idc_bar.update(1)
        title = item["aria-label"]
        link = unquote(item["href"]).split("url=")
        try:
            link = link[1]
        except IndexError:
            link = link[0]
        if link.startswith("https://www.udemy.com"):
            idc_links.append(title + "|:|" + link)
    idc_bar.close()

# Constants

version = "v1.0"


def create_scrape_obj():
    funcs = {
        "Discudemy": threading.Thread(target=discudemy, daemon=True),
        "Udemy Freebies": threading.Thread(target=udemy_freebies, daemon=True),
        "Tutorial Bar": threading.Thread(target=tutorialbar, daemon=True),
        "Real Discount": threading.Thread(target=real_discount, daemon=True),
        "Course Vania": threading.Thread(target=coursevania, daemon=True),
        "IDownloadCoupons": threading.Thread(target=idcoupons, daemon=True),
    }
    return funcs


animation = ["|", "/", "---", "\\"]

################


def cookiejar(client_id, access_token):
    cookies = dict(client_id=client_id, access_token=access_token)
    return cookies


def save_config(config):
    if True:
        with open("duce-cli-settings.json", "w") as f:
            json.dump(config, f, indent=4)


def load_config():
    try:
        with open("duce-cli-settings.json") as f:
            config = json.load(f)

    except FileNotFoundError:
        config = requests.get(
            "https://raw.githubusercontent.com/techtanic/DUCE-CLI/master/duce-cli-settings.json"
        ).json()

    instructor_exclude = "\n".join(config["exclude_instructor"])

    save_config(config)

    return config, instructor_exclude


def get_course_id(url):
    r2 = s.get(url, headers=head)
    soup = bs(r2.content, "html5lib")
    if r2.status_code == 404:
        return ""

    else:
        try:
            courseid = soup.find(
                "body",
                attrs={
                    "class": "ud-app-loader ud-component--course-landing-page-free-udlite udemy"
                },
            )["data-clp-course-id"]
        except:
            courseid = soup.find(
                "body", attrs={"data-module-id": "course-landing-page/udlite"}
            )["data-clp-course-id"]
            # with open("problem.txt","w",encoding="utf-8") as f:
            # f.write(str(soup))
    return courseid


def get_course_coupon(url):
    query = urlsplit(url).query
    params = parse_qs(query)
    try:
        params = {k: v[0] for k, v in params.items()}
        return params["couponCode"]
    except:
        return ""


def get_catlang(courseid):
    r = s.get(
        "https://www.udemy.com/api-2.0/courses/"
        + courseid
        + "/?fields[course]=locale,primary_category",
        headers=head,
    ).json()
    return r["primary_category"]["title"], r["locale"]["simple_english_title"]


def course_landing_api(courseid):
    r = s.get(
        "https://www.udemy.com/api-2.0/course-landing-components/"
        + courseid
        + "/me/?components=purchase,instructor_bio",
        headers=head,
    ).json()

    instructor = (
        r["instructor_bio"]["data"]["instructors_info"][0]["absolute_url"]
        .lstrip("/user/")
        .rstrip("/")
    )
    try:
        purchased = r["purchase"]["data"]["purchase_date"]
    except:
        purchased = False
    try:
        amount = r["purchase"]["data"]["list_price"]["amount"]
    except:
        print(r["purchase"]["data"])

    return instructor, purchased, Decimal(amount)


def update_available():
    if version.lstrip("v") < requests.get(
        "https://api.github.com/repos/techtanic/DUCE-CLI/releases/latest"
    ).json()["tag_name"].lstrip("v"):
        print(by + fr + "  Update Available  ")
    else:
        return


def check_login():
    head = {
        "authorization": "Bearer " + access_token,
        "accept": "application/json, text/plain, */*",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
        "x-forwarded-for": str(ip),
        "x-udemy-authorization": "Bearer " + access_token,
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.udemy.com",
        "referer": "https://www.udemy.com/",
        "dnt": "1",
    }

    r = requests.get(
        "https://www.udemy.com/api-2.0/contexts/me/?me=True&Config=True", headers=head
    ).json()
    currency = r["Config"]["price_country"]["currency"]
    user = ""
    user = r["me"]["display_name"]

    s = requests.session()
    s.cookies.update(cookies)
    s.keep_alive = False

    return head, user, currency, s


# -----------------
def free_checkout(coupon, courseid):
    payload = (
        '{"checkout_environment":"Marketplace","checkout_event":"Submit","shopping_info":{"items":[{"discountInfo":{"code":"'
        + coupon
        + '"},"buyable":{"type":"course","id":'
        + str(courseid)
        + ',"context":{}},"price":{"amount":0,"currency":"'
        + currency
        + '"}}]},"payment_info":{"payment_vendor":"Free","payment_method":"free-method"}}'
    )

    r = s.post(
        "https://www.udemy.com/payment/checkout-submit/",
        headers=head,
        data=payload,
        verify=False,
    )
    return r.json()


def free_enroll(courseid):

    s.get(
        "https://www.udemy.com/course/subscribe/?courseId=" + str(courseid),
        headers=head,
    )

    r = s.get(
        "https://www.udemy.com/api-2.0/users/me/subscribed-courses/"
        + str(courseid)
        + "/?fields%5Bcourse%5D=%40default%2Cbuyable_object_type%2Cprimary_subcategory%2Cis_private",
        headers=head,
    )
    return r.json()


# -----------------


def auto(list_st):

    se_c, ae_c, e_c, ex_c, as_c = 0, 0, 0, 0, 0
    for index, link in enumerate(list_st):
        title = link.split("|:|")
        print(fy + str(index) + " " + title[0], end=" ")
        link = title[1]
        print(fb + link)
        course_id = get_course_id(link)
        if course_id:
            coupon_id = get_course_coupon(link)
            cat, lang = get_catlang(course_id)
            instructor, purchased, amount = course_landing_api(course_id)
            if instructor in instructor_exclude:
                print(flb + "Instructor excluded\n")
                ex_c += 1

            elif cat in categories and lang in languages:

                if not purchased:

                    if coupon_id:
                        slp = ""

                        js = free_checkout(coupon_id, course_id)
                        try:
                            if js["status"] == "succeeded":
                                print(fg + "Successfully Enrolled\n")
                                se_c += 1
                                as_c += amount

                            elif js["status"] == "failed":
                                # print(js)
                                print(fr + "Coupon Expired\n")
                                e_c += 1

                        except:
                            try:
                                msg = js["detail"]
                                print(fr + msg)
                                print()
                                slp = int(re.search(r"\d+", msg).group(0))
                            except:
                                # print(js)
                                print(fr + "Expired Coupon\n")
                                e_c += 1

                        if slp != "":
                            slp += 5
                            print(
                                fr
                                + ">>> Pausing execution of script for "
                                + str(slp)
                                + " seconds\n",
                            )
                            time.sleep(slp)
                        else:
                            time.sleep(3.5)

                    elif not coupon_id:
                        js = free_enroll(course_id)
                        try:
                            if js["_class"] == "course":
                                print(fg + "Successfully Subscribed\n")
                                se_c += 1
                                as_c += amount

                        except:
                            print(fr + "COUPON MIGHT HAVE EXPIRED\n")
                            e_c += 1

                elif purchased:
                    print(flb + purchased)
                    print()
                    ae_c += 1

            else:
                print(flb + "User not interested\n")
                ex_c += 1

        elif not course_id:
            print(fr + "Course Doesn't exist\n")

        # main_window["pout"].update(index + 1)
    print(f"Successfully Enrolled: {se_c}")
    print(f"Already Enrolled: {ae_c}")
    print(f"Amount Saved: ${round(as_c,2)}")
    print(f"Expired Courses: {e_c}")
    print(f"Excluded Courses: {ex_c}")


def random_color():
    col = ["green", "yellow", "white"]
    return random.choice(col)


##########################################


def main1():
    try:
        links_ls = []
        for index in funcs:
            pass
        for index in funcs:
            funcs[index].start()
        for t in funcs:
            funcs[t].join()

        try:  # du_links
            links_ls += du_links
        except:
            pass
        try:  # uf_links
            links_ls += uf_links
        except:
            pass
        try:  # tb_links
            links_ls += tb_links
        except:
            pass
        try:  # rd_links
            links_ls += rd_links
        except:
            pass
        try:  # cv_links
            links_ls += cv_links
        except:
            pass
        try:  # idc_links
            links_ls += idc_links
        except:
            pass

        auto(links_ls)

    except:
        e = traceback.format_exc()
        print(e)


config, instructor_exclude = load_config()
ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

############## MAIN ############# MAIN############## MAIN ############# MAIN ############## MAIN ############# MAIN ###########


try:
    access_token = config["access_token"]
    client_id = config["client_id"]
    csrftoken = ""
    cookies = cookiejar(client_id, access_token)
    head, user, currency, s = check_login()

except Exception as e:
    print(fr + "Login error")
    exit()
try:
    update_available()
except:
    pass


all_functions = create_scrape_obj()
funcs = {}
sites = []
categories = []
languages = []
instructor_exclude = config["exclude_instructor"]
user_dumb = True

for name in config["sites"]:
    if config["sites"][name]:
        funcs[name] = all_functions[name]
        sites.append(name)
        user_dumb = False

for cat in config["category"]:
    if config["category"][cat]:
        categories.append(cat)

for lang in config["category"]:
    if config["category"][lang]:
        languages.append(lang)

if user_dumb:
    print(bw + fr + "  No sites selected  ")
if not user_dumb:
    tm = threading.Thread(target=main1, daemon=True)
    tm.start()

tm.join()
