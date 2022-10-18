from typing import Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By

def readFromFile(fileName) -> list:
    file = open(fileName, "r", encoding="utf8")
    content = pruneAndUpdateFile(file.read().splitlines(), fileName)
    file.close
    return content

def pruneAndUpdateFile(content, fileName) -> list:
    fileModified = False
    while True: 
        duplicateCheck = checkForDuplicates(content)
        # If duplicate found
        if duplicateCheck[0]:
            fileModified = True
            content.remove(duplicateCheck[1])
        else:
            break

    if fileModified:
        writeListToFile(content, fileName)

    return content

def writeListToFile(list, fileName):
    file = open(fileName, "w")
    list = map(lambda x: x + '\n', list)
    file.writelines(list)
    file.close


def checkForDuplicates(content) -> Tuple:
    setOfContent = set()
    for line in content:
        if line in setOfContent:
            return (True, line)
        else:
            setOfContent.add(line)
    return (False,)

def findLowestPrice(product, driver) -> str:
    url = "https://www.tilbudsugen.dk/tilbud/" + product
    acceptable_stores = {"Føtex", "Netto", "Lidl", "Fakta", "SPAR", "REMA 1000"}
    driver.get(url)
    productElements = driver.find_elements(By.CSS_SELECTOR, "a[class*='search-result-item search_result_list']")
    if len(productElements) == 0:
        return product + " er ikke på tilbud denne uge"

    for productElement in productElements:
        store = productElement.get_attribute("data-chain")
        if store in acceptable_stores:
            productName =  productElement.find_element(By.CLASS_NAME, "details-product-name").text
            href = productElement.get_attribute("href")
            price = productElement.find_element(By.CLASS_NAME, "price").text
            validity = productElement.find_element(By.CLASS_NAME, "order-validity").text
            return productName + " | " + store + " | " + price + " | " + validity + " | " + href
    return product + " er ikke på tilbud i de ønskede butikker"

def main():
    productsFile = "Products.txt"
    pricesFile = "Prices.txt"
    products = readFromFile(productsFile)
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    lowestPriceDetails = list()

    for product in products:
        lowestPriceDetails.append(findLowestPrice(product, driver))

    driver.close
    writeListToFile(lowestPriceDetails, pricesFile)

if __name__ == "__main__" :
    main()
