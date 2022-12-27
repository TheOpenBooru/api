from pickledb import PickleDB

blacklist = PickleDB("./data/blacklist.json", True, True)

if not blacklist.exists("blacklist"):
    blacklist.dcreate("blacklist")


def check_blacklist(ip: str) -> bool:
    return blacklist.dexists("blacklist", ip)


def get_ban_reason(ip: str) -> str:
    return blacklist.dget("blacklist", ip)


def ban(ip: str, message: str):
    blacklist.dadd("blacklist", (ip, message))
