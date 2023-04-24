
import random
import string
import time
from playwright.sync_api import Playwright, sync_playwright, expect


meeting_link = "https://us02web.zoom.us/j/86900950117?pwd=UW1mVWgxWFZoU0w3MXJQZnQxVkJKZz09"
web_link = meeting_link.replace("/j/","/wc/join/")
print(web_link)

def run(playwright: Playwright) -> None:
    def gen_name():    
        tags = ["DE","En","DE/ENG","ENG"]
        random_tag_id = round(random.random()*(len(tags)-1))

        # initializing size of string
        N = 7
        
        # using random.choices()
        # generating random strings
        random_str = ''.join(random.choices(string.ascii_letters, k=N))
        
        name =  tags[random_tag_id]+" "+ random_str

        return name
    
    def open_zoom():
        permanent_users = True
        context = browser.new_context(locale='de-DE',timezone_id='Europe/Berlin')
        page = context.new_page()
        page.goto(web_link)
        page.get_by_placeholder("Ihr Name").fill(gen_name())
        page.get_by_role("button", name="Beitreten").click()
        page.get_by_text("Cookies ablehnen Cookies akzeptieren").click()
        page.get_by_role("button", name="Cookies akzeptieren").click()
        page.get_by_role("button", name="Ich stimme zu").click()


        #page.get_by_role("button", name="Beitreten").nth(1).click()

        url = page.url
        time.sleep(5)
        page.close()
        while True:
            if permanent_users:
                context = browser.new_context(locale='de-DE',timezone_id='Europe/Berlin')
            
            page = context.new_page()
            page.goto(web_link)
            page.get_by_placeholder("Ihr Name").fill(gen_name())
            page.get_by_role("button", name="Beitreten").click()
            #page.get_by_role("button", name="Beitreten").nth(1).click()
            time.sleep(5)
            
            if permanent_users:
                page.get_by_text("Cookies ablehnen Cookies akzeptieren").click()
                page.get_by_role("button", name="Cookies akzeptieren").click()
                page.get_by_role("button", name="Ich stimme zu").click()
            else:
                page.close()
        #page1.get_by_text("[Urgent Discard]").nth(0).click()

        return context,url
        

    def refresh_participant(participant):
        page = participant[0].new_page()
        page.goto(participant[1])

    #browser = playwright.chromium.launch(headless=False)
    browser = playwright.chromium.launch()
    participants = []
    context,url = open_zoom()
    
    participants.extend([[context,url]])
    #refresh
    #refresh_participant(participants[0])
    
    
    #context.set_offline(True)
    # context = open_zoom()
    # context = open_zoom()
    # context = open_zoom()

    time.sleep(2000)
    # ---------------------

    browser.close()


with sync_playwright() as playwright:
    run(playwright)
