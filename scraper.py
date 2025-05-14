import logging
import re
from random import randint
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, BrowserContext, Page
from sqlalchemy.orm import Session

from src.crud.DriveDisc import create_or_update_drive_disc
from src.crud.WEngine import create_or_update_w_engine
from src.database import get_db
from src.models import Specialty, StatsType
from src.schemas.DriveDisc import DriveDiscBase
from src.schemas.Stats import StatsBase
from src.schemas.WEngine import WEngineBase

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def block_images(route):
    if route.request.resource_type == "image":
        return route.abort()
    return route.continue_()


def scroll_to_bottom(page: Page):
    previous_height = page.evaluate("document.body.scrollHeight")

    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(randint(500, 750))

        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == previous_height:
            break

        previous_height = new_height


# DRIVE DISC
def extract_main_data_wh(soup: BeautifulSoup, value_type: str) -> str:
    node = soup.find("div", class_="base-info-item-key", string=value_type).find_parent('div', class_='base-info-item')
    value_node = node.find('div', class_='base-info-item-value')

    return value_node.text.strip()


def parse_drive_disc(soup: BeautifulSoup) -> DriveDiscBase:
    return DriveDiscBase(
        name=extract_main_data_wh(soup, "Name"),
        description_2p_set=extract_main_data_wh(soup, "2-Piece Set"),
        description_4p_set=extract_main_data_wh(soup, "4-Piece Set")
    )


def get_drive_disc_data(db: Session, page: Page):
    soup = BeautifulSoup(page.content(), "html.parser")

    try:
        drive_disc = parse_drive_disc(soup)
    except Exception as e:
        logger.error(f" Error parsing Drive Disc: {e}")

    logger.debug(f" Create or update drive disc : {drive_disc.name}")
    create_or_update_drive_disc(db, drive_disc)


def get_all_drive_discs(db: Session, context: BrowserContext, url: str):
    page = context.new_page()
    page.goto(url)
    page.wait_for_timeout(randint(2000, 2500))
    scroll_to_bottom(page)

    drive_discs_nodes = page.locator(".hover\\:tw-border-zzz-l-brand-yellow-3")

    for i in range(drive_discs_nodes.count()):
        with context.expect_page() as page_info:
            drive_discs_nodes.nth(i).click()

        drive_disc_page = page_info.value
        drive_disc_page.wait_for_timeout(randint(2000, 2500))

        get_drive_disc_data(db, drive_disc_page)

        drive_disc_page.close()
    
    page.close()


# W-ENGINE
def get_stats_type(stats: str) -> StatsType:
    match stats:
        case "Percent ATK":
            return StatsType.PERCENT_ATK
        case "Base ATK":
            return StatsType.BASE_ATK
        case "Percent HP":
            return StatsType.PERCENT_HP
        case "Percent DEF":
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
        case "Impact":
            return StatsType.IMPACT


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
        case "Rupture":
            return Specialty.RUPTURE


def extract_main_data_hhw(soup: BeautifulSoup, value_type: str):
    return soup.select_one("table.genshin_table.main_table").find("td", string=value_type).next_sibling


def parse_w_engine(soup: BeautifulSoup) -> WEngineBase:
    stats_table_node = soup.select_one("#char_stats .stat_table")

    stats_type_nodes = stats_table_node.select("thead td")
    base_stats_type = get_stats_type(stats_type_nodes[1].text.strip())
    advanced_stats_type = get_stats_type(stats_type_nodes[2].text.strip())

    base_stats_list, advanced_stats_list = [], []

    for tr in stats_table_node.select("tbody > tr"):
        td_nodes = tr.select("td")

        level = int(re.sub(r"\D", "", td_nodes[0].text))
        base_stats_value = float(re.sub(r"[^\d.]", "", td_nodes[1].text))
        advanced_stats_value = float(re.sub(r"[^\d.]", "", td_nodes[2].text))

        base_stats_list.append(StatsBase(stats=base_stats_type, level=level, value=base_stats_value))
        advanced_stats_list.append(StatsBase(stats=advanced_stats_type, level=level, value=advanced_stats_value))


    name_node = extract_main_data_hhw(soup, "Name")
    rank_node = extract_main_data_hhw(soup, "Rarity").find_all("img")
    specialty_node = extract_main_data_hhw(soup, "Class")
    effect_node = soup.select_one("#char_skills .skill_dmg_table tr:nth-of-type(2) td:nth-of-type(2)")

    return WEngineBase(
        name=name_node.text.strip(),
        rank={5: "S", 4: "A", 3: "B"}.get(len(rank_node)),
        specialty=get_specialty(specialty_node.text.strip()),
        base_stats=base_stats_list,
        advanced_stats=advanced_stats_list,
        effect=effect_node.text.strip()
    )


def get_w_engine_data(db: Session, page: Page) -> None:
    soup = BeautifulSoup(page.content(), "html.parser")

    try:
        w_engine = parse_w_engine(soup)
    except Exception as e:
        logger.error(f" Error parsing W-Engine: {e}")
        return

    logger.debug(f" Create or update w-engine : {w_engine.name}")
    create_or_update_w_engine(db, w_engine)


def get_all_w_engines(db: Session, context: BrowserContext, url: str):
    page = context.new_page()
    page.route("**/*", block_images)
    page.goto(url)
    page.wait_for_timeout(randint(1000, 1500))
    page.get_by_role("button", name="Accept").click()

    pagination_node = page.locator(".sortable_page_table td")

    while True:
        cells_nodes = page.locator(".genshin_table.sortable tbody tr td:nth-of-type(2)")

        for i in range(cells_nodes.count()):
            w_engine_page = context.new_page()
            w_engine_page.route("**/*", block_images)
            w_engine_page.goto(urljoin(url, cells_nodes.nth(i).locator("a").get_attribute("href")))
            w_engine_page.wait_for_timeout(randint(1000, 1500))

            get_w_engine_data(db, w_engine_page)
            
            w_engine_page.close()

        if pagination_node.nth(pagination_node.count() - 2).get_attribute("class") != "checked":
            pagination_node.last.click()
            page.wait_for_timeout(randint(1000, 1500))
        else:
            break
    
    page.close()


if __name__ == '__main__':
    db = next(get_db())

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()

        # drive discs
        logger.info(" Creating or updating Drive Discs ...")
        url = "https://wiki.hoyolab.com/pc/zzz/aggregate/12"
        get_all_drive_discs(db, context, url)

        # w-engines
        logger.info(" Creating or updating W-Engines ...")
        url = "https://zzz.honeyhunterworld.com/w-drives"
        get_all_w_engines(db, context, url)

        browser.close()