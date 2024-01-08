import json

from config import cfg
from models import Strain
from parser import Parser
from logger import logger


class Strains():
    items: dict[int: Strain] = {}

    def __init__(self):
        if not cfg.dump_name.exists():
            Parser().run()

        self.load()

    def load(self):
        with open(cfg.dump_name, "r") as f:
            self.items = {i: Strain(**s) for i, s in json.load(f).items()}

    def show(self):
        for strain in self.items.values():
            logger.info(strain)
            input()