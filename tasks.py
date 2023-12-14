from robocorp import browser
from RPA.HTTP import HTTP
from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from Libraries import DB
from RPA.Archive import Archive
from RPA.PDF import PDF
from RPA.FileSystem import FileSystem
#from progress.bar import barp

import time

selenium = Selenium()

@task
def order_robots_from_RobotSpareBin():
    """Challenge 2
    1. Orders robots from RobotSpareBin Industries Inc.
    2. Saves the order HTML receipt as a PDF file.
    3. Saves the screenshot of the ordered robot. 
    4. Embeds the screenshot of the robot to the PDF receipt.
    5. Creates ZIP archive of the receipts and the images.
    """
    # TODO: Implement your function here
    delete_files()
    get_order()
    #Database
    DB.DB()
    pagina= login()
    read_csv_file(pagina)
    create_zip()

def login():
     browser.configure(
         
          screenshot ="only-on-failure",
          headless = True,
     )
    # selenium.open_browser(url="https://robotsparebinindustries.com/", browser="chrome")
    # selenium.wait_until_element_is_visible(locator='//input[@id="username"]')
    # time.sleep(10)

     browser.goto("https://robotsparebinindustries.com/")
     pagina = browser.page()
     pagina.wait_for_selector('//button[@class="btn btn-primary"]')
     pagina.click(selector='//a[@class="nav-link"]')
     pagina.wait_for_selector('//div[@class="alert-buttons"]')
     return pagina
        
def get_order():
     http = HTTP()
     http.download('https://robotsparebinindustries.com/orders.csv', target_file="output/orders.csv", overwrite=True)

def read_csv_file(page):
     print("\n")
     table_csv = DB.obtain_dat()
     #barl = Bar('Procesando:', max=20)
     for item in table_csv:
        page = place_values(pagina = page, dat=item )
        parar = True 
        count = 0
        while parar:
            result = click_order(page)
            if count == 15:
                parar = False 
                break
            if result:
                parar = False 
                break 
            else:
                count += 1
                continue 
        Img_Pdf(page, item)
       # barl.next()
    #barl.finish()

def place_values(pagina,dat):
    # Variables
    head = dat['head']
    body = dat[ 'body']
    legs = dat['legs']
    address = dat['address']

    pagina.wait_for_selector('//button[@class="btn btn-dark"]')
    pagina.click(selector='//button[@class="btn btn-dark"]')
    pagina.wait_for_selector(selector= '//select[@id="head"]')
    pagina.select_option(selector='//select[@id="head"]', value=f'{head}')
    pagina.click(selector=f'//input[@id="id-body-{body}"]')
    pagina.fill(selector='//input[@placeholder="Enter the part number for the legs"]',value=f'{legs}')
    pagina.fill(selector='//input[@id="address"]', value=f'{address}') 
    pagina.click(selector='//button[@id="preview"]')
    pagina.wait_for_selector(selector='//dic[@id="robot-preview-image"]')
    return pagina 
    
def click_order(pagina):
    try:
        pagina.click(selector='//button[@id="order"]')
        pagina.wait_for_selector(selector='div[@id="receipt"]')
        return True 
    except:
        return False 
    
def Img_Pdf(page,dat ):   
     pdf = PDF()
     order_number = dat['order_number']
     page.locator('//div[@id="robot-preview-image"]').screenshot(path=f'IMG/image_robot_{order_number}.png')
     sales_result_html=page.locator(selector='xpath=//div[@id="receipt"]').inner.html()
     pdf.html_to_pdf(sales_result_html, f'PDF/pdf_robot_{order_number}.pdf')
     files = [f'IMG/image_robot_{order_number}.png']
     pdf.open_pdf(f'PDF/pdf_robot_{order_number}.pdf')
     pdf.add_files_to_pdf(files=files, target_document=f'PDF/pdf_robot_{order_number}.pdf', append=True)
     pdf.close_all_pdfs()
     page.click('//button[@id="order-another"]')

def delete_files():
         fileSystem = FileSystem()
         #Eliminar imagenes
         listfileIMG = fileSystem.list_directories_in_directory(path="IMG")
         for file in listfileIMG:
             fileSystem.remove_filepath(path=f'{file}')
        # Eliminar PDF
         listfilePDF = fileSystem.list_directories_in_directory(path="PDF")
         for file in listfilePDF:
             fileSystem.remove_file(path=f'{file}')

def create_zip():
    archive = Archive()
    FileSystem - FileSystem()
    FileSystem.remove_file('resultado/PDFS_robots')
    archive.archive_folder_with_zip(folder='PDF', archive_name='resultado/PDFS_robots.zip')
         

