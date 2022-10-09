from typing import Tuple
from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def readProducts(fileName) -> list:
    file = open(fileName, "r", encoding="utf8")
    products = pruneAndUpdateProducts(file.read().splitlines(), fileName)
    file.close
    return products

def pruneAndUpdateProducts(products, fileName) -> list:
    fileModified = False
    while True: 
        duplicateCheck = checkForDuplicates(products)
        # If duplicate found
        if duplicateCheck[0]:
            fileModified = True
            products.remove(duplicateCheck[1])
        else:
            break

    if fileModified:
        writeListToFile(products, fileName)

    return products

def writeListToFile(list, fileName):
    file = open(fileName, "w")
    list = map(lambda x: x + '\n', list)
    file.writelines(list)
    file.close


def checkForDuplicates(products) -> Tuple:
    setOfProducts = set()
    for product in products:
        if product in setOfProducts:
            return (True, product)
        else:
            setOfProducts.add(product)
    return (False,)

def findLowestPrice(product, driver) -> str:
    url = "https://www.tilbudsugen.dk/tilbud/" + product
    driver.get(url)
    try:
        productDetails = driver.find_element(By.CLASS_NAME, "details-product-name")
        productName = productDetails.text
        store = productDetails.get_attribute("data-chain")
        price = driver.find_element(By.CLASS_NAME, "price").text
        validity = driver.find_element(By.CLASS_NAME, "order-validity").text
    except:
        return product + " er ikke på tilbud denne uge"
    return productName + " | " + store + " | " + price + " | " + validity



def main():
    productsFile = "Products.txt"
    pricesFile = "Prices.txt"
    products = readProducts(productsFile)
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    lowestPriceDetails = list()

    for product in products:
        lowestPriceDetails.append(findLowestPrice(product, driver))

    driver.close
    writeListToFile(lowestPriceDetails, pricesFile)

if __name__ == "__main__" :
    main()
