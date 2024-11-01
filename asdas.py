import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# LambdaTest credentials
USERNAME = "mananawasthi7"
ACCESS_KEY = "sS6luvJXSkX3esYqLz3gvTmbgWN9oaIpSLYWodSmPhfjto0d2Y"

# LambdaTest URL for Selenium Grid
LT_GRID_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub.lambdatest.com/wd/hub"

# Streamlit Inputs
st.title("Automated Account Creation with LambdaTest")
admin_username = st.text_input("Admin Username", "Sunny11038")
admin_password = st.text_input("Admin Password", "Lalit@8765", type="password")

client_name = st.text_input("Client Full Name", "Rehan Jain1212321")
client_password = st.text_input("Client Password", "Manan123111212", type="password")
credit_reference = st.text_input("Credit Reference", "100")
transaction_password = st.text_input("Transaction Password", "174889", type="password")

if st.button("Run Script"):
    start_time = time.time()
    st.write("Starting automation process...")

    # Set up the browser options with capabilities
    options = webdriver.ChromeOptions()
    options.browser_version = "latest"
    options.platform_name = "Windows 10"

    # Additional LambdaTest capabilities
    lt_options = {
        "user": USERNAME,
        "accessKey": ACCESS_KEY,
        "build": "Streamlit LambdaTest Demo",
        "name": "Account Creation Test on LambdaTest",
        "network": True,
        "console": True,
        "visual": True,
    }
    options.set_capability("LT:Options", lt_options)

    # Initialize remote WebDriver with LambdaTest capabilities
    driver = webdriver.Remote(
        command_executor=LT_GRID_URL,
        options=options
    )

    try:
        # Step 1: Open the login page
        driver.get("https://www.saffronexch.com/admin")
        time.sleep(1)
        st.write("Opened login page.")

        # Step 2: Login
        try:
            username_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input-1")))
            password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input-2")))
            username_field.send_keys(admin_username)
            password_field.send_keys(admin_password)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            WebDriverWait(driver, 10).until(EC.url_contains("/admin"))
            st.success("Login successful, proceeding to List of Accounts page.")
        except (TimeoutException, NoSuchElementException) as e:
            st.error(f"Error during login: {e}")
            driver.quit()
            st.stop()

        # Step 3: Wait for loader overlay
        WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, "loader-overlay")))
        st.write("Loader overlay disappeared, navigating to List of Accounts page.")

        # Step 4: Navigate to "List of Accounts"
        try:
            list_of_accounts_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "List of Clients")))
            list_of_accounts_link.click()
            st.write("Navigated to List of Accounts page.")
        except (TimeoutException, NoSuchElementException) as e:
            st.error(f"Error finding 'List of Clients' link: {e}")
            driver.quit()
            st.stop()

        # Step 5: Click "Add Account"
        try:
            add_account_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Add Account")))
            add_account_button.click()
            st.write("Navigated to Add Account page.")
        except (TimeoutException, NoSuchElementException) as e:
            st.error(f"Error finding 'Add Account' button: {e}")
            driver.quit()
            st.stop()

        # Step 6: Fill in form
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "clientname"))).send_keys(client_name)
            st.write("Client Name filled.")
        except NoSuchElementException:
            st.error("Error: 'Client Name' field not found.")

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(client_password)
            st.write("Password filled.")
        except NoSuchElementException:
            st.error("Error: 'Password' field not found.")

        try:
            account_type_dropdown = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "newlvlno"))))
            account_type_dropdown.select_by_value("6")
            st.write("Account Type set to 'User'.")
        except NoSuchElementException:
            st.error("Error: 'Account Type' dropdown not found.")

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "rpassword"))).send_keys(client_password)
            st.write("Retype Password filled.")
        except NoSuchElementException:
            st.error("Error: 'Retype Password' field not found.")

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "fullname"))).send_keys(client_name)
            st.write("Full Name filled.")
        except NoSuchElementException:
            st.error("Error: 'Full Name' field not found.")

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "camt"))).send_keys(credit_reference)
            st.write("Credit Reference filled.")
        except NoSuchElementException:
            st.error("Error: 'Credit Reference' field not found.")

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "mpassword"))).send_keys(transaction_password)
            st.write("Transaction Password filled.")
        except NoSuchElementException:
            st.error("Error: 'Transaction Password' field not found.")

        # Step 7: Submit form
        try:
            submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-submit')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)
            submit_button.click()
            st.success("Form submitted successfully.")
        except (NoSuchElementException, ElementClickInterceptedException):
            st.error("Error: 'Submit' button not found or clickable.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    finally:
        # Calculate and display execution time
        execution_time = time.time() - start_time
        st.write(f"Total execution time: {execution_time:.2f} seconds")
        
        # Close the browser
        driver.quit()
