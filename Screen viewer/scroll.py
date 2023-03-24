def scroll_to_bottom_and_back(driver):
    # Hämta höjden på webbsidan och höjden av webbläsarfönstret
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    window_height = int(driver.execute_script("return window.innerHeight"))

    # Bestäm hur mycket som ska scrollas per iteration
    scroll_by = int(window_height / 100)

    # Scrolla sidan långsamt genom att göra flera små scrollningar med mellanrum
    scroll_count = 0
    for i in range(0, total_height, scroll_by):
        driver.execute_script(f"window.scrollTo(0, {i})")
        #scroll_count += 1
        #if scroll_count % 99 == 0:
        #    time.sleep(1)
        time.sleep(0.1)    
    # Scrolla tillbaka till toppen av sidan när scrollningen är klar
    driver.execute_script("window.scrollTo(0, 0)")
