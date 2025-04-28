import logging
import re
from random import randint

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, BrowserContext, Page
from sqlalchemy.orm import Session

from src.crud.DriveDisc import create_or_update_drive_disc
from src.crud.WEngine import create_or_update_w_engine
from src.database import get_db
from src.models import Specialty
from src.models import StatsType
from src.schemas.DriveDisc import DriveDiscBase
from src.schemas.Stats import StatsBase
from src.schemas.WEngine import WEngineBase

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_main_data(soup: BeautifulSoup, value_type: str) -> str:
    node = soup.find("div", class_="base-info-item-key", string=value_type).find_parent('div', class_='base-info-item')
    value = node.find('div', class_='base-info-item-value')

    return value.text.strip()


def block_images(route):
    if route.request.resource_type == "image":
        return route.abort()
    return route.continue_()


def scroll_to_bottom(page: Page):
    previous_height = page.evaluate("document.body.scrollHeight")

    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(randint(750, 1250))

        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == previous_height:
            break

        previous_height = new_height


# DRIVE DISC
def get_drive_disc_data(db: Session, html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")

    drive_disc = DriveDiscBase(
        name=get_main_data(soup, "Name"),
        description_2p_set=get_main_data(soup, "2-Piece Set"),
        description_4p_set=get_main_data(soup, "4-Piece Set")
    )

    logger.debug(f" Create or update drive disc : {drive_disc.name}")
    create_or_update_drive_disc(db, drive_disc)


def get_all_drive_discs(db: Session, context: BrowserContext, url: str):
    page = context.new_page()
    page.goto(url)
    page.wait_for_timeout(randint(2000, 2500))
    scroll_to_bottom(page)

    drive_discs_nodes = page.locator(".hover\\:tw-border-zzz-l-brand-yellow-3")
    logger.debug(f" Getting {drive_discs_nodes.count()} drive discs to create or update")

    for i in range(drive_discs_nodes.count()):
        with context.expect_page() as page_info:
            drive_discs_nodes.nth(i).click()

        drive_disc_page = page_info.value
        drive_disc_page.wait_for_timeout(randint(2000, 2500))

        get_drive_disc_data(db, drive_disc_page.content())

        drive_disc_page.close()


# W-ENGINE
def get_specialty(specialty: str) -> Specialty:
    match specialty:
        case "Defense":
            return Specialty.DEFENSE
        case "Anomaly":
            return Specialty.ANOMALY
        case "Attack":
            return Specialty.ATTACK
        case "Stun":
            return Specialty.STUN
        case "Support":
            return Specialty.SUPPORT


def get_stats_type(stats: str) -> StatsType:
    match stats:
        case "ATK":
            return StatsType.PERCENT_ATK
        case "ATK %":
            return StatsType.PERCENT_ATK
        case "Base ATK":
            return StatsType.BASE_ATK
        case "HP":
            return StatsType.PERCENT_HP
        case "HP %":
            return StatsType.PERCENT_HP
        case "DEF":
            return StatsType.PERCENT_DEF
        case "DEF %":
            return StatsType.PERCENT_DEF
        case "PEN Ratio":
            return StatsType.PEN_RATIO
        case "CRIT Rate":
            return StatsType.CRIT_RATE
        case "CRIT DMG":
            return StatsType.CRIT_DMG
        case "Anomaly Proficiency":
            return StatsType.ANOMALY_PROFICIENCY
        case "Energy Regen":
            return StatsType.ENERGY_REGEN
        case "Energy Regen %":
            return StatsType.ENERGY_REGEN
        case "Impact":
            return StatsType.IMPACT


def extract_stats(soup: BeautifulSoup, label: str, index: int):
    stats_list = []

    level_node = soup.select_one(".dot_b4p1b")
    level = int(re.sub(r"\D", "", level_node.text)) if level_node is not None else 0
    values = soup.select("tr.tr_AusNU")[index].select("td.td_bbiIZ")[:2]

    for value in values:
        value_text = re.sub(r"[^\d.]", "", value.text)

        if is_number(value_text):
            stats_list.append(StatsBase(
                stats=get_stats_type(get_main_data(soup, label)),
                level=level,
                value=float(value_text)
            ))

    return stats_list


def get_w_engine_data(db: Session, page: Page):
    base_stats_list = []
    advanced_stats_list = []

    soup = BeautifulSoup(page.content(), "html.parser")

    base_stats_list.extend(extract_stats(soup, "Base Stats", 1))
    advanced_stats_list.extend(extract_stats(soup, "Advanced Stats", 2))

    slider_nodes = page.locator(".mark_qjAbg")

    for i in range(1, slider_nodes.count()):
        slider_nodes.nth(i).click()
        page.wait_for_timeout(randint(400, 600))

        soup = BeautifulSoup(page.content(), "html.parser")

        base_stats_list.extend(extract_stats(soup, "Base Stats", 1))
        advanced_stats_list.extend(extract_stats(soup, "Advanced Stats", 2))

    headers = soup.select(".c-entry-tag-item")

    for tag in headers:
        value = tag.text.strip()

        if len(value) > 1:
            specialty = get_specialty(value)
        else:
            rank = value

    effect = soup.select_one(".base-info-content > .base-info-item:last-child .base-info-item-value").text.replace("*Stats shown are at Base level.", "").strip()

    w_engine = WEngineBase(
        name=get_main_data(soup, "Name"),
        rank=rank,
        specialty=specialty,
        base_stats=base_stats_list,
        advanced_stats=advanced_stats_list,
        effect=effect or "no description"
    )

    logger.debug(f" Create or update w-engine : {w_engine.name}")
    create_or_update_w_engine(db, w_engine)


def get_all_w_engines(db: Session, context: BrowserContext, url: str):
    page = context.new_page()
    page.goto(url)
    page.wait_for_timeout(randint(2000, 2500))
    scroll_to_bottom(page)

    w_engines_nodes = page.locator(".hover\\:tw-border-zzz-l-brand-yellow-3")
    logger.info(f" Getting {w_engines_nodes.count()} w-engines to create or update")

    for i in range(w_engines_nodes.count()):
        with context.expect_page() as page_info:
            w_engines_nodes.nth(i).click()

        w_engine_page = page_info.value
        w_engine_page.wait_for_timeout(randint(2000, 2500))

        get_w_engine_data(db, w_engine_page)

        w_engine_page.close()


if __name__ == '__main__':
    db = next(get_db())

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()

        # drive discs
        url = 'https://wiki.hoyolab.com/pc/zzz/aggregate/12'
        get_all_drive_discs(db, context, url)

        # w-engines
        url = 'https://wiki.hoyolab.com/pc/zzz/aggregate/11'
        get_all_w_engines(db, context, url)

        browser.close()