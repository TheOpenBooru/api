from openbooru.modules import account
import pytest


def createAccount():
    account.register("","")
    account.login("","")