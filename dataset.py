import json
import pickle

import Levenshtein

from config import cfg
from models import Strain
from logger import logger


def levenshtein_distance(str1, str2):
    return Levenshtein.distance(str1, str2)


def levenshtein_similarity(str1, str2):
    max_length = max(len(str1), len(str2))
    if max_length == 0:
        return 100.0
    else:
        similarity = (1 - levenshtein_distance(str1, str2) / max_length) * 100
        return similarity


class Strains():
    items: dict[int: Strain] = {}

    def __init__(self):
        logger.info("Loading strains dataset...")
        self.load()

    def __iter__(self):
        return iter(self.items.values())

    def show_similar(self, state: str):
        for strain in self.items.values():
            if self.is_similar(state, strain):
                logger.success(self._get_strain_line(strain))

    @staticmethod
    def is_similar(state: str, strain: Strain):
        for state in state.split():
            if not state:
                continue
            if state.lower() in strain.name.lower():
                return strain.name

    @staticmethod
    def _get_strain_line(strain):
        return (f"reviews: {strain.reviewCount:<4} {strain.category:<10} "
                f"https://www.leafly.com/strains/{strain.slug:40}")

    def get_by_slug(self, slug: str):
        for strain in self.items.values():
            if strain.slug == slug:
                return strain

    def dump(self):
        with open(cfg.dump_strains, 'wb') as file:
            pickle.dump(self.items, file)

    def load(self):
        try:
            with open(cfg.dump_strains, 'rb') as file:
                self.items = pickle.load(file)
        except:
            logger.error("Cannot read strains.pickle")

    def put_strains(self, strains: list[Strain]) -> bool:
        '''
        We sort strains by the date they were created, starting with the newest.
        Once we get all the strains from a page, we don't need to look at the
        next pages because they won't have new information. If we notice this,
        we'll set a flag to stop looking through more pages.
        '''
        exists = any(s.id in self.items for s in strains)
        self.items.update({s.id: s for s in strains})
        total = len(self.items)
        logger.success(f"Put {len(strains)} {total=}")
        self.dump()
        return exists

    def show(self):
        for strain in self.items.values():
            logger.info(strain)

    def export(self):
        with open('export.json', 'w') as file:
            items = {i: s.dict() for i, s in self.items.items()}
            json.dump(items, file)
