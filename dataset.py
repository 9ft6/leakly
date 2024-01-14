import pickle

import Levenshtein

from config import cfg
from models import Strain, Comment
from parser import Parser
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
    parser: Parser

    def __init__(self):
        self.parser = Parser(self)
        self.load()

        if cfg.update_strains:
            self.parser.run()
            self.dump()

    def show_similar(self, state: str):
        for strain in self.items.values():
            if self.is_similar(state, strain):
                logger.success(self._get_strain_line(strain))

    def is_similar(self, state: str, strain: Strain):
        for state in state.split():
            if not state:
                continue
            if state.lower() in strain.name.lower():
                return strain.name

    def _get_strain_line(self, strain):
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

    def put_strains(self, strains: list[Strain]):
        self.items.update({s.id: s for s in strains})
        total = len(self.items)
        logger.success(f"Put {len(strains)} {total=}")
        self.dump()

    def show(self):
        for strain in self.items.values():
            logger.info(strain)
