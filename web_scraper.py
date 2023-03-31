from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class Scraper():

    def __init__(self):
        
        self.driver: webdriver = webdriver.Chrome()
        self.driver.get("https://pubmlst.org/bigsdb?db=pubmlst_campylobacter_isolates&page=projects")
        self.accept_cookies()

    
    def accept_cookies(self):

        time.sleep(1)
        self.driver.implicitly_wait(5)
        self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/a').click()


    def quit_driver(self):

        self.driver.quit()
        
    
    def go_to_sequences(self):

        self.driver.get("https://pubmlst.org/bigsdb?db=pubmlst_campylobacter_isolates&page=projects")

        time.sleep(1)

        self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div[2]/div/table/tbody/tr[50]/td[6]/a/span').click()

        time.sleep(1)

        self.driver.find_element(by=By.XPATH, value= '/html/body/div[2]/div[2]/div/div[2]/div/form/div[1]/fieldset[1]/ul/li/span/select[1]/option[7]').click()
        self.driver.find_element(by=By.XPATH, value= '/html/body/div[2]/div[2]/div/div[2]/div/form/div[1]/fieldset[1]/ul/li/span/input').send_keys("2018")
        self.driver.find_element(by=By.XPATH, value= '/html/body/div[2]/div[2]/div/div[2]/div/form/div[1]/fieldset[13]/input').click()
        time.sleep(1)
        container = self.driver.find_element(by=By.XPATH, value='//*[@id="plugins"]/div[5]/div/form[3]')
        container.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div[7]/div[5]/div/form[2]/input[6]').click()


    def get_records(self) -> list[str]:

        self.go_to_sequences()

        time.sleep(1)

        container = self.driver.find_element(by=By.XPATH, value='//*[@id="queryform"]/form/div[1]/fieldset[1]')
        text = container.find_element(by=By.TAG_NAME, value='textarea').text
        records = list(text.split())  

        for record in records:

            container = self.driver.find_element(by=By.XPATH, value='//*[@id="queryform"]/form/div[1]/fieldset[1]') # Redefines the container

            container.find_element(by=By.TAG_NAME, value='textarea').clear() # Clears the id
            container.find_element(by=By.TAG_NAME, value='textarea').send_keys(record) # Inserts the id of choice

            container.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div[2]/form/div/fieldset[4]/input').click()
            #container.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div/div[3]/table/tbody/tr/td[5]/a').click() # Clicks the download 
            
            #Wait until element appears
            WebDriverWait(self.driver, 10000).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[2]/div/div[3]/table/tbody/tr/td[5]/a'))).click()

            # Download here
            time.sleep(1)
            sequences = self.driver.find_element(by=By.XPATH, value = "/html/body/pre").text
            with open (rf"contig{record}.fasta", "w") as ofile:
                ofile.write(sequences)  
            
            self.go_to_sequences()

        return(record)

if __name__ == "__main__":

    scraper = Scraper()
    print(scraper.get_records())


scraper.quit_driver()

