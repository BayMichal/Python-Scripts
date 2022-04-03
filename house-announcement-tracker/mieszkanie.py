
#################################################################################
#                                                                               #
#                       Bajkos Michał                                           #
#       Scirpt for send email when new announcement is on Rzeszowiak            #
#                                                                               #
#################################################################################
#                       Init
##############################################################
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from selenium import webdriver
from pyvirtualdisplay import Display
from time import sleep
from smtplib import SMTP
from selenium.webdriver.chrome.options import Options
import pathlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess  
import os
import multiprocessing as mp

##############################################################
#
#                  Email protocol sender function
#
##############################################################
def email_sender(emailBody,  screenName, Announcement, fromPage):
    with SMTP('smtp.gmail.com', 587) as smtp:
        debugLog("PROBA WYSLANIA EMAIL")
        sender =  #write
        sender_password = #write
        receiver = #write
        filename='screen.png'
        fp=open(filename,'rb')
    
        msg = MIMEMultipart()
        msg['Subject'] = 'WebDriver ' + str(Announcement) + " " + str(fromPage)
        text = MIMEText(emailBody)
        msg.attach(text)

        path = pathlib.Path().resolve()
        with open(str(path) + "/" + screenName, 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name=screenName)
        msg.attach(image)
        debugLog("DODANO ZALACZNIK")
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender, sender_password)
        debugLog("ZALOGOWANO")

        smtp.sendmail(sender, receiver, msg.as_string())
        debugLog("WYSLANO EMAIL")
        os.remove(screenName)
        debugLog("USUNIETO ZDJECIE")

##############################################################
#
#                  Debug logs function
#
#                  Bash:
#                  Debug mode:      python3 name_script.py
#                  Release mode:    python3 -O name_script.py
#
##############################################################
def debugLog(text):
    if __debug__:
        print("DEBUG_LOG: ", text)
    else:
        return

##############################################################
#
#                  For restart script once a day
#
##############################################################
def run_again(cmd):
    subprocess.call(["bash", "-c", "source ~/.profile; " + cmd])  


def main():
    #Variable
    ogloszenia_gold_id = []
    ogloszenia_silver_id = []
    Task = True
    time = 0
    screenName = "screen.png"
    page0 = "Rzeszowiak"
    typePremium = "PREMIUM"
    typeNormal = "Normal"
    interval = 60 

    #Background display on
    display = Display(visible=0, size=(1920, 1080))

    #Selenium driver on
    display.start()
    
    #Driver chromium On
    driver = webdriver.Chrome()
    driver.get("https://www.rzeszowiak.pl/Nieruchomosci-Mam-do-wynajecia-2100011255?r=mieszkanie")

    licznik_gold = 0
    licznik_silver = 0
    #Ogloszenia premium
    for i in driver.find_elements_by_xpath('//div[@class="promobox-body"]'):
        #print(i.get_attribute("id"))
        ogloszenia_gold_id.append(i.get_attribute("id"))
        const_gold = len(ogloszenia_gold_id)

    for i in driver.find_elements_by_xpath('//div[@class="normalbox-body"]'):
        #print(i.get_attribute("id"))
        ogloszenia_silver_id.append(i.get_attribute("id"))
        const_silver = len(ogloszenia_silver_id)
        


    
    while(Task):
        for i in driver.find_elements_by_xpath('//div[@class="promobox-body"]'):
            if(licznik_gold == const_gold):
                    licznik_gold = 0

            if(i.get_attribute("id") != ogloszenia_gold_id[licznik_gold]):
                debugLog("Wchodze w ogłoszenie")
                i.click()
                debugLog("Jestem w nowym ogłoszeniu")
                driver.execute_script("window.scrollTo(0, 500)")
                debugLog("Scroll okna") 
                driver.save_screenshot(screenName)
                debugLog("Zapisano Screena")
                link = driver.current_url


                #wyslij maila
                try:
                    email_sender(link, screenName, typePremium, page0)
                    print("Scipt restart")
                    driver.close()
                    run_again("python3 -O mieszkanie.py")
                except:
                    debugLog("EXCEPTION")
                    driver.close()
                    run_again("python3 -O mieszkanie.py")
                
            
            licznik_gold = licznik_gold + 1

        for i in driver.find_elements_by_xpath('//div[@class="normalbox-body"]'):
            if(licznik_silver == const_silver):
                    licznik_silver = 0

            if(i.get_attribute("id") != ogloszenia_silver_id[licznik_silver]):
                debugLog("Wchodze w ogłoszenie")
                i.click()
                debugLog("Jestem w nowym ogłoszeniu")
                driver.execute_script("window.scrollTo(0, 500)")
                debugLog("Scroll okna") 
                driver.save_screenshot(screenName)
                debugLog("Zapisano Screena")
                link = driver.current_url


                #wyslij maila
                try:
                    email_sender(link, screenName, typeNormal, page0)
                    print("Scipt restart")
                    driver.close()
                    run_again("python3 -O mieszkanie.py")
                except:
                    debugLog("EXCEPTION")
                    driver.close()
                    run_again("python3 -O mieszkanie.py")
                
            
            licznik_silver = licznik_silver + 1

            
        debugLog("Sleep mode 1 min")
        sleep(interval)


    
        

if __name__ == "__main__":
    #p = mp.Pool(mp.cpu_count())
    #p.map(worker())
    main()

