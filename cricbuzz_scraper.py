from flask import Flask, render_template
from flask import request
from scrapy.http import HtmlResponse
import requests

cricket = Flask (__name__)

@cricket.route("/live_score/<id_no>" , methods=["GET"])
def live_data(id_no):
    
    cookies = {
        '__gads': 'ID=eb35dd6a312b96c7:T=1666236989:S=ALNI_MbRrIsmE0-uU5gBZRiLOqlpJtHvKQ',
        '_col_uuid': '1c58e40f-eb84-4708-9b77-62901975fb5f-62t8',
        'cb_config': '%7B%7D',
        'cbzads': 'IN|not_set|not_set|not_set',
        'cbgeo': 'IN',
        '_ga_4H06J8XXQH': 'GS1.1.1667373042.9.0.1667373042.0.0.0',
        'cookie_test': '1',
        '_gid': 'GA1.2.565548616.1667450614',
        '__gpi': 'UID=00000b66b26f70ac:T=1666236989:RT=1667450613:S=ALNI_MYYVSu9lfPndpwAkM33o2fG15WSug',
        'rb_ads': '1',
        '_ga_83LXEV4P47': 'GS1.1.1667450617.1.1.1667450707.0.0.0',
        '_ga': 'GA1.1.888649699.1666237002',
    }

    headers = {
        'authority': 'm.cricbuzz.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7',
        # Requests sorts cookies= alphabetically
        # 'cookie': '__gads=ID=eb35dd6a312b96c7:T=1666236989:S=ALNI_MbRrIsmE0-uU5gBZRiLOqlpJtHvKQ; _col_uuid=1c58e40f-eb84-4708-9b77-62901975fb5f-62t8; cb_config=%7B%7D; cbzads=IN|not_set|not_set|not_set; cbgeo=IN; _ga_4H06J8XXQH=GS1.1.1667373042.9.0.1667373042.0.0.0; cookie_test=1; _gid=GA1.2.565548616.1667450614; __gpi=UID=00000b66b26f70ac:T=1666236989:RT=1667450613:S=ALNI_MYYVSu9lfPndpwAkM33o2fG15WSug; rb_ads=1; _ga_83LXEV4P47=GS1.1.1667450617.1.1.1667450707.0.0.0; _ga=GA1.1.888649699.1666237002',
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }

    return_data={}

    cribuzz_summary='https://m.cricbuzz.com/live-cricket-scorecard/43041'
    cribuzz_summary=cribuzz_summary.replace("43041",id_no)

    response_html = requests.get(cribuzz_summary, cookies=cookies, headers=headers)

    # with open("D:\PROGRAM\python\Flask_app\cricket.html","w", encoding="utf-8") as fp:
    #     fp.write(str(response_html.text))

    response_html = HtmlResponse(url="https://random_url",body=response_html.text, encoding="utf-8")
    
    return_data["Match"] = response_html.xpath('//*[@id="top"]/div/div[13]/div[2]/div[1]/div/div/div/text()').get()
    return_data["summary"] = response_html.xpath('//*[@id="top"]/div/div[7]/div/div/h3/span/text()').get()
    return_data["First_Inning"] = response_html.xpath('//*[@id="inn_1"]/div[1]/div[1]/text()').get()
    return_data["Second_Inning"] = response_html.xpath('//*[@id="inn_2"]/div[1]/div[1]/text()').get()

    innings1_bat={}
    innings2_bat={}
    innings1_boller={}
    innings2_boller={}
    return_batting=[]
    
    
    
    for i  in range(2,13):
        try: 
            First_inning_batsman_name = response_html.xpath(f'//*[@id="inn_1"]//*[@class="table-responsive"][{i}]/table/tr/td/a/b/span/text()').get().strip()
            innings1_bat[First_inning_batsman_name] = response_html.xpath(f'//*[@id="inn_1"]//*[@class="table-responsive"][{i}]/table/tr/td[2]/b/text()').get()+ response_html.xpath(f'//*[@id="inn_1"]//*[@class="table-responsive"][{i}]/table/tr/td[2]/b/span/text()').get()
        except Exception as e:
            print(e)
            break
    return_data["First_inning_batsman_stats"]=innings1_bat

    for i  in range(2,13):
        try: 
            Second_inning_batsman_name = response_html.xpath(f'//*[@id="inn_2"]//*[@class="table-responsive"][{i}]/table/tr/td/a/b/span/text()').get().strip()
            innings2_bat[Second_inning_batsman_name] = response_html.xpath(f'//*[@id="inn_2"]//*[@class="table-responsive"][{i}]/table/tr/td[2]/b/text()').get()+ response_html.xpath(f'//*[@id="inn_2"]//*[@class="table-responsive"][{i}]/table/tr/td[2]/b/span/text()').get()
        except Exception as e:
            print(e)
            break
    return_data["Second_inning_batsman_stats"]=innings2_bat

    for i  in range(2,13):
        try: 
            Second_inning_boller_name = response_html.xpath(f'//*[@id="inn_2"]//*[@class="list-group"][3]//*[@class="table-responsive"]/table/tr[{i}]/td/a/b/span/text()').get().strip()
            innings2_boller[Second_inning_boller_name] = "over:"+  response_html.xpath(f'//*[@id="inn_2"]//*[@class="list-group"][3]//*[@class="table-responsive"]/table/tr[{i}]/td[2]/text()').get()+", Runs:"+response_html.xpath(f'//*[@id="inn_2"]//*[@class="list-group"][3]//*[@class="table-responsive"]/table/tr[{i}]/td[4]/text()').get()+", Wickets:"+response_html.xpath(f'//*[@id="inn_2"]//*[@class="list-group"][3]//*[@class="table-responsive"]/table/tr[{i}]/td[5]/b/text()').get()
        except Exception as e:
            print(e)
            break
    return_data["Second_inning_bowler_stats"]=innings2_boller

    for i  in range(2,13):
        try: 
            First_inning_boller_name = response_html.xpath(f'//*[@id="inn_1"]//*[@class="list-group"][3]//*[@class="table-responsive"]/table/tr[{i}]/td/a/b/span/text()').get().strip()
            innings1_boller[First_inning_boller_name] = "over:"+  response_html.xpath(f'//*[@id="inn_1"]//*[@class="list-group"][3]//*[@class="table-responsive"]/table/tr[{i}]/td[2]/text()').get()+", Runs:"+response_html.xpath(f'//*[@id="inn_1"]//*[@class="list-group"][3]//*[@class="table-responsive"]/table/tr[{i}]/td[4]/text()').get()+", Wickets:"+response_html.xpath(f'//*[@id="inn_1"]//*[@class="list-group"][3]//*[@class="table-responsive"]/table/tr[{i}]/td[5]/b/text()').get()
        except Exception as e:
            print(e)
            break
    return_data["First_inning_bowler_stats"]=innings1_boller

    # return_data["Second_Inning_boller"] = response_html.xpath('//*[@id="inn_2"]//*[@class="list-group"][3]//*[@class="table-responsive"]/table/tr[4]/td/a/b/span/text()').get()
    

   
    return return_data

cricket.run("0.0.0.0",debug=True)