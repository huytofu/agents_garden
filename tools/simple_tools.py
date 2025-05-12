import helium
import math
from typing import Tuple
from smolagents import tool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def calculate_haversine_distance(
    origin_coords: Tuple[float, float],
    destination_coords: Tuple[float, float],
) -> float:
    """
    Calculate the travel time for a cargo plane between two points on Earth using great-circle distance.

    Args:
        origin_coords: Tuple of (latitude, longitude) for the starting point
        destination_coords: Tuple of (latitude, longitude) for the destination

    Returns:
        float: The estimated travel time in hours

    Example:
        >>> # Chicago (41.8781° N, 87.6298° W) to Sydney (33.8688° S, 151.2093° E)
        >>> result = calculate_haversine_distance((41.8781, -87.6298), (-33.8688, 151.2093))
    """

    def to_radians(degrees: float) -> float:
        return degrees * (math.pi / 180)

    # Extract coordinates
    lat1, lon1 = map(to_radians, origin_coords)
    lat2, lon2 = map(to_radians, destination_coords)

    # Earth's radius in kilometers
    EARTH_RADIUS_KM = 6371.0

    # Calculate great-circle distance using the haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    distance = EARTH_RADIUS_KM * c
    return distance

@tool
def initialize_driver() -> webdriver.Chrome:
    """Initialize the Selenium WebDriver."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--window-size=1000,1350")
    chrome_options.add_argument("--disable-pdf-viewer")
    chrome_options.add_argument("--window-position=0,0")
    return helium.start_chrome(headless=False, options=chrome_options)

@tool
def search_item_ctrl_f(driver: webdriver.Chrome, text: str, nth_result: int = 1) -> str:
    """
    Searches for text on the current page via Ctrl + F and jumps to the nth occurrence.
    Args:
        driver: The driver returned by initialize_driver function
        text: The text to search for
        nth_result: Which occurrence to jump to (default: 1)
    """
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        raise Exception(f"Match n°{nth_result} not found (only {len(elements)} matches found)")
    result = f"Found {len(elements)} matches for '{text}'."
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    result += f"Focused on element {nth_result} of {len(elements)}"
    return result


@tool
def go_back(driver: webdriver.Chrome) -> None:
    """Goes back to previous page.
    Args:
        driver: The driver returned by initialize_driver function
    """
    driver.back()


@tool
def close_popups(driver: webdriver.Chrome) -> str:
    """
    Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows! This does not work on cookie consent banners.
    Args:
        driver: The driver returned by initialize_driver function
    """
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

HELIUM_INSTRUCTIONS = """
    Use your web_search tool when you want to get Google search results.
    Then you can use helium to access websites. Don't use helium for Google search, only for navigating websites!
    Don't bother about the helium driver, it's already managed.
    We've already ran "from helium import *"
    Then you can go to pages!
    Code:
    ```py
    go_to('github.com/trending')
    ```<end_code>

    You can directly click clickable elements by inputting the text that appears on them.
    Code:
    ```py
    click("Top products")
    ```<end_code>

    If it's a link:
    Code:
    ```py
    click(Link("Top products"))
    ```<end_code>

    If you try to interact with an element and it's not found, you'll get a LookupError.
    In general stop your action after each button click to see what happens on your screenshot.
    Never try to login in a page.

    To scroll up or down, use scroll_down or scroll_up with as an argument the number of pixels to scroll from.
    Code:
    ```py
    scroll_down(num_pixels=1200) # This will scroll one viewport down
    ```<end_code>

    When you have pop-ups with a cross icon to close, don't try to click the close icon by finding its element or targeting an 'X' element (this most often fails).
    Just use your built-in tool `close_popups` to close them:
    Code:
    ```py
    close_popups()
    ```<end_code>

    You can use .exists() to check for the existence of an element. For example:
    Code:
    ```py
    if Text('Accept cookies?').exists():
        click('I accept')
    ```<end_code>

    Proceed in several steps rather than trying to solve the task in one shot.
    And at the end, only when you have your answer, return your final answer.
    Code:
    ```py
    final_answer("YOUR_ANSWER_HERE")
    ```<end_code>

    If pages seem stuck on loading, you might have to wait, for instance `import time` and run `time.sleep(5.0)`. But don't overuse this!
    To list elements on page, DO NOT try code-based element searches like 'contributors = find_all(S("ol > li"))': just look at the latest screenshot you have and read it visually, or use your tool search_item_ctrl_f.
    Of course, you can act on buttons like a user would do when navigating.
    After each code blob you write, you will be automatically provided with an updated screenshot of the browser and the current browser url.
    But beware that the screenshot will only be taken at the end of the whole action, it won't see intermediate states.
    Don't kill the browser.
    When you have modals or cookie banners on screen, you should get rid of them before you can click anything else.
"""