import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config

import time

from CSV import CSV
from JSON import JSON
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
    d.execute_script('''window.open("https://opensea.io/collection/cryptoch0x61d/assets/create","_blank")''')
    d.switch_to.window(d.window_handles[2])
    time.sleep(3)


def signin_to_opensea(d):
    # d.find_element_by_xpath('//span[text()="MetaMask"]').click()
    # For now you have to click to select the wallets, it's seems it's not working now.
    time.sleep(6)
    d.switch_to.window(d.window_handles[3])
    d.find_element_by_xpath('//button[text()="Next"]').click()
    time.sleep(2)
    d.find_element_by_xpath('//button[text()="Connect"]').click()


def fillMetadata(d, metadataMap: dict):
    d.find_element_by_xpath('//div[@class="AssetFormTraitSection--side"]/button').click()
    for index, value in enumerate(metadataMap):
        input1 = d.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[1]/div/div/input')
        input2 = d.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[2]/div/div/input')

        input1.send_keys(str(value))
        input2.send_keys(str(metadataMap[value]))
        if index != len(metadataMap) - 1:
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
    d.execute_script('''location.href="https://opensea.io/collection/cryptoch0x61d/assets/create"''')


if __name__ == '__main__':
    # setup metamask
    opt = webdriver.ChromeOptions()
    opt.add_extension(EXTENSION_PATH)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=opt)
    setup_metamask_wallet(driver)
    time.sleep(2)
    move_to_opensea(driver)
    signin_to_opensea(driver)
    driver.execute_script('''window.open("https://opensea.io/collection/cryptoch0x61d/assets/create","_blank")''')
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(7)  # todo- need to manually click on sign button for now
    data = JSON(os.getcwd() + "/data/metadata.json").readFromFile()
    for key in data:
        name = "#"+key # NAME OF YOUR FILE
        description = name + " from DemonQueenNFT" #NOTE: YOU NEED TO UPDATE THIS ACCORDINGLY
        file = key+".png"
        metadata = data[key]
        upload(driver, NFT(name, description, metadata, os.getcwd() + "/data/" + file))
    print("DONE!!")
