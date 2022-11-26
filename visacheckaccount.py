class VISACheckAccount:
    accountNumber = 0
    username = ""
    name = ""

    def __init__(self, *_):
        pass

    def isSettled() -> bool:
        return True

    def getUsername() -> str:
        raise NotImplementedError

    def getAccountNumber() -> int:
        raise NotImplementedError

    @staticmethod
    def fetchById(_id):
        return VISACheckAccount()

    @staticmethod
    def fetchByUsername(_username):
        return VISACheckAccount()
