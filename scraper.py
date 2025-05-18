import logging
import re
from random import randint
from typing import Callable
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag
from playwright.sync_api import sync_playwright, BrowserContext, Locator, Page
from sqlalchemy.orm import Session

from src.crud.Bangboo import create_or_update_bangboo
from src.crud.DriveDisc import create_or_update_drive_disc
from src.crud.WEngine import create_or_update_w_engine
from src.database import get_db
from src.models import SkillType, Specialty, StatsType
from src.schemas.Bangboo import BangbooBase
from src.schemas.DriveDisc import DriveDiscBase
from src.schemas.Faction import FactionBase
from src.schemas.Skill import SkillBase
from src.schemas.SkillMultiplier import SkillMultiplierBase
from src.schemas.Stats import StatsBase
from src.schemas.WEngine import WEngineBase

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# WIKI HOYOLAB
def get_data_from_wh(db: Session, context: BrowserContext, url: str, get_data: Callable):
    main_page = context.new_page()
    main_page.goto(url)
    main_page.wait_for_timeout(randint(2000, 2500))

    scroll_to_bottom(main_page)

    data_nodes = main_page.locator(".hover\\:tw-border-zzz-l-brand-yellow-3")

    for i in range(data_nodes.count()):
        with context.expect_page() as page_info:
            data_nodes.nth(i).click()

        data_page = page_info.value
        data_page.wait_for_timeout(randint(2000, 2500))

        get_data(db, data_page)

        data_page.close()
    
    main_page.close()


def scroll_to_bottom(page: Page):
    previous_height = page.evaluate("document.body.scrollHeight")

    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(randint(500, 750))

        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == previous_height:
            break

        previous_height = new_height


def extract_main_data_wh(soup: BeautifulSoup, value_type: str) -> str:
    node = soup.find("div", class_="base-info-item-key", string=value_type).find_parent('div', class_='base-info-item')
    value_node = node.find('div', class_='base-info-item-value')

    return value_node.text.strip()


# HONEY HUNTER WORLD
def get_data_from_hhw(db: Session, context: BrowserContext, url: str, get_data: Callable):
    main_page = go_to_new_page(context, url)
    cookie_button = main_page.get_by_role("button", name="Accept")
    
    if cookie_button.count() > 0:
        cookie_button.click()

    pagination_node = main_page.locator(".sortable_page_table td")
    nb_pages = get_nb_pages(pagination_node)

    while True:
        cells_nodes = main_page.locator(".genshin_table.sortable tbody tr td:nth-of-type(2)")

        for i in range(cells_nodes.count()):
            data_page = go_to_new_page(context, urljoin(url, cells_nodes.nth(i).locator("a").get_attribute("href")))
            get_data(db, data_page)
            data_page.close()

        if pagination_node.nth(nb_pages).get_attribute("class") != "checked":
            pagination_node.last.click()
            main_page.wait_for_timeout(randint(500, 750))
        else:
            break

    main_page.close()


def go_to_new_page(context: BrowserContext, url: str) -> Page:
    page = context.new_page()
    page.route("**/*", block_images)
    page.goto(url)
    page.wait_for_timeout(randint(1000, 1500))

    return page


def block_images(route):
    if route.request.resource_type == "image":
        return route.abort()
    return route.continue_()


def get_nb_pages(pagination_node: Locator) -> int:
    pagination_node.nth(0).click()

    for i in range(pagination_node.count() - 1):
        next_node_text = pagination_node.nth(i + 1).inner_text().strip()

        if next_node_text in ["0", "Next"]:
            current_node_text = pagination_node.nth(i).inner_text().strip()

            if current_node_text.isdigit():
                return int(current_node_text)
    
    return 0


def extract_main_data_hhw(soup: BeautifulSoup, value_type: str):
    return soup.select_one("table.genshin_table.main_table").find("td", string=value_type).next_sibling


# DRIVE DISC
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
        return

    logger.debug(f" Create or update Drive Disc : {drive_disc.name}")
    create_or_update_drive_disc(db, drive_disc)


# W-ENGINE
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
        rank=get_rank(rank_node),
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

    logger.debug(f" Create or update W-Engine : {w_engine.name}")
    create_or_update_w_engine(db, w_engine)


# BANGBOO
def get_bangboo_data(db: Session, page: Page) -> None:
    soup = BeautifulSoup(page.content(), "html.parser")

    try:
        bangboo = parse_bangboo(soup)
    except Exception as e:
        logger.error(f" Error parsing Bangboo: {e}")
        return

    if bangboo.name in ["Eous", "Bangboo_Name_56001"]:
        return

    logger.debug(f" Create or update Bangboo : {bangboo.name}")
    create_or_update_bangboo(db, bangboo)


def parse_bangboo(soup: BeautifulSoup) -> BangbooBase:
    return BangbooBase(
        name=extract_main_data_hhw(soup, "Name").text.strip(),
        rank=get_rank(extract_main_data_hhw(soup, "Rarity").find_all("img")),
        faction=FactionBase(name="undefined"),
        base_stats=parse_bangboo_base_stats(soup),
        version_released=0.0,
        skills=parse_bangboo_skills(soup)
    )


def parse_bangboo_base_stats(soup: BeautifulSoup) -> list[StatsBase]:
    base_stats_list = []

    stats_table_node = soup.select_one("#char_stats .stat_table")
    head_cells = stats_table_node.select("thead td")
    body_rows = stats_table_node.select("tbody tr")

    for rows in body_rows:
        cells = rows.select("td")

        for i in range(1, len(cells) - 1):
            base_stats_list.append(StatsBase(
                stats=get_stats_type(head_cells[i].text.strip()),
                level=int(re.sub(r"\D", "", cells[0].text)),
                value=float(re.sub(r"[^\d.]", "", cells[i].text))
            ))

    return base_stats_list


def parse_bangboo_skills(soup: BeautifulSoup) -> list[SkillBase]:
    skills_list = []

    skill_tables = soup.select("#char_skills .skill_table")

    for skill_table_node in skill_tables:
        rows = skill_table_node.select("tr")
        br = rows[1].select_one('br')

        skills_list.append(SkillBase(
            name=rows[0].select_one("a").text.strip(),
            type=get_skill_type(parse_bangboo_skill_type(br)),
            description=parse_bangboo_skill_description(br),
            multipliers=parse_bangboo_skill_multipliers(skill_table_node)
        ))

    return skills_list


def parse_bangboo_skill_type(tag: Tag) -> str:
    result = []

    for sibling in tag.previous_siblings:
        result.insert(0, str(sibling))

    return BeautifulSoup("".join(result), "html.parser").text.strip()


def parse_bangboo_skill_description(tag: Tag) -> str:
    result = []

    for sibling in tag.next_siblings:
        result.append(str(sibling))

    return BeautifulSoup("".join(result), "html.parser").text.strip()


def parse_bangboo_skill_multipliers(tag: Tag) -> list[SkillMultiplierBase]:
    multipliers_list = []

    rows = tag.select_one(".skill_dmg_table").select("tr")
    cells_level = rows[0].select("td")

    for row in rows[1:]:
        cells = row.select("td")
        skill_multiplier_name = cells[0].text.strip()

        for i in range(1, len(cells)):
            multipliers_list.append(SkillMultiplierBase(
                name=skill_multiplier_name,
                level=int(re.sub(r"\D", "", cells_level[i].text.strip())),
                value=cells[i].text.strip()
            ))

    return multipliers_list


# GENERAL FUNCTION
def get_specialty(specialty: str) -> Specialty:
    match specialty.lower():
        case "defense":
            return Specialty.DEFENSE
        case "anomaly":
            return Specialty.ANOMALY
        case "attack":
            return Specialty.ATTACK
        case "stun":
            return Specialty.STUN
        case "support":
            return Specialty.SUPPORT
        case "rupture":
            return Specialty.RUPTURE


def get_rank(rank_node) -> str:
    return {5: "S", 4: "A", 3: "B"}.get(len(rank_node))


def get_stats_type(stats: str) -> StatsType:
    match stats.lower():
        case "atk":
            return StatsType.FLAT_ATK
        case "percent atk":
            return StatsType.PERCENT_ATK
        case "base atk":
            return StatsType.BASE_ATK
        case "hp":
            return StatsType.FLAT_HP
        case "percent hp":
            return StatsType.PERCENT_HP
        case "def":
            return StatsType.FLAT_DEF
        case "percent def":
            return StatsType.PERCENT_DEF
        case "pen ratio":
            return StatsType.PEN_RATIO
        case "crit rate":
            return StatsType.CRIT_RATE
        case "crit dmg":
            return StatsType.CRIT_DMG
        case "anomaly proficiency":
            return StatsType.ANOMALY_PROFICIENCY
        case "anomaly mastery":
            return StatsType.ANOMALY_MASTERY
        case "energy regen":
            return StatsType.ENERGY_REGEN
        case "impact":
            return StatsType.IMPACT


def get_skill_type(skill_type: str) -> SkillType:
    skill_type = skill_type.lower()

    if "active skill" in skill_type:
        return SkillType.BANGBOO_ACTIVE_SKILL
    elif "additional ability" in skill_type:
        return SkillType.BANGBOO_ADDITIONAL_SKILL
    elif "bangboo chain attack" in skill_type:
        return SkillType.BANGBOO_CHAIN_ATTACK


if __name__ == '__main__':
    db = next(get_db())

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()

        # drive discs
        logger.info(" Creating or updating Drive Discs ...")
        url = "https://wiki.hoyolab.com/pc/zzz/aggregate/12"
        get_data_from_wh(db, context, url, get_drive_disc_data)

        # w-engines
        logger.info(" Creating or updating W-Engines ...")
        url = "https://zzz.honeyhunterworld.com/w-drives"
        get_data_from_hhw(db, context, url, get_w_engine_data)

        # bangboo
        logger.info(" Creating or updating Bangboo ...")
        url = "https://zzz.honeyhunterworld.com/bangboos"
        get_data_from_hhw(db, context, url, get_bangboo_data)

        browser.close()