import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config

import time

from CSV import CSV
from NFT import NFT

EXTENSION_PATH = config("EXTENSION_PATH")

RECOVERY_CODE = config("RECOVERY_CODE")

PASSWORD = config("PASSWORD")

CHROME_DRIVER_PATH = config("CHROME_DRIVER_PATH")

def setup_metamask_wallet(d):
    d.switch_to.window(d.window_handles[0])  # focus on metamask tab
    time.sleep(5)
    d.find_element(By.XPATH, '//button[text()="Get Started"]').click()

    time.sleep(1)
    d.find_element_by_xpath('//button[text()="Import wallet"]').click()
    time.sleep(1)

    d.find_element_by_xpath('//button[text()="No Thanks"]').click()
    time.sleep(1)

    inputs = d.find_elements_by_xpath("//input")
    inputs[0].send_keys(RECOVERY_CODE)
    time.sleep(1)
    inputs[1].send_keys(PASSWORD)
    inputs[2].send_keys(PASSWORD)
    time.sleep(1)

    d.find_element_by_css_selector(".first-time-flow__terms").click()
    d.find_element_by_xpath('//button[text()="Import"]').click()


def move_to_opensea(d):
    d.execute_script('''window.open("https://opensea.io/collection/guy-with-a-smirk/assets/create","_blank")''')
    d.switch_to.window(d.window_handles[2])
    time.sleep(3)


def signin_to_opensea(d):
    d.find_element_by_xpath('//span[text()="MetaMask"]').click()
    time.sleep(2)
    d.switch_to.window(d.window_handles[3])
    d.find_element_by_xpath('//button[text()="Next"]').click()
    time.sleep(2)
    d.find_element_by_xpath('//button[text()="Connect"]').click()


def fillMetadata(d, metadataMap: dict):
    d.find_element_by_xpath('//div[@class="AssetFormTraitSection--side"]/button').click()
    for key in metadataMap:
        input1 = d.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[1]/div/div/input')
        input2 = d.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[2]/div/div/input')

        input1.send_keys(str(key))
        input2.send_keys(str(metadataMap[key]))
        d.find_element_by_xpath('//button[text()="Add more"]').click()

    time.sleep(1)
    d.find_element_by_xpath('//button[text()="Save"]').click()


def upload(d, nft: NFT):
    d.switch_to.window(driver.window_handles[-1])
    time.sleep(3)
    d.find_element_by_id("media").send_keys(nft.file)
    d.find_element_by_id("name").send_keys(nft.name)
    d.find_element_by_id("description").send_keys(nft.description)

    time.sleep(3)

    fillMetadata(d, nft.metadata)

    time.sleep(2)
    d.find_element_by_xpath('//button[text()="Create"]').click()
    time.sleep(5)
    d.execute_script('''location.href="https://opensea.io/collection/guy-with-a-smirk/assets/create"''')


if __name__ == '__main__':
    # setup metamask
    opt = webdriver.ChromeOptions()
    opt.add_extension(EXTENSION_PATH)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=opt)
    setup_metamask_wallet(driver)
    time.sleep(2)
    move_to_opensea(driver)
    signin_to_opensea(driver)
    driver.execute_script('''window.open("https://opensea.io/collection/guy-with-a-smirk/assets/create","_blank")''')
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(7)  # todo- need to manually click on sign button for now
    data = CSV(os.getcwd() + "/data/data.csv").readFromFile()
    for nft in data:
        if "file" not in nft:
            raise Exception("Why, no file ??")
        file = nft["file"]
        name = nft["name"] if "name" in nft else "NFT 1"
        description = nft["description"] if "description" in nft else "Description og NFT 1"
        metadata = {
            "character": nft["character"] if "character" in nft else "None",
            "clothing": nft["clothing"] if "clothing" in nft else "None",
            "extra": nft["extra"] if "extra" in nft else "None"
        }
        upload(driver, NFT(name, description, metadata, os.getcwd() + "/data/" + file))
    print("DONE!!")

