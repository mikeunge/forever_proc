import run_forever_proc as proc


class ServiceTest:
    def __init__(self):
        self.service = proc.Service()

    def run(self):
        i = 0
        cases = 2
        if ServiceTest.isUp_True(self, "bot.js"):
            print("✔ isUp_True ... passed")
            i += 1
        else:
            print("❌ isUp_True ... failed")
        if not ServiceTest.isUp_False(self, "bot.py"):
            print("✔ isUp_False ... passed")
            i += 1
        else:
            print("❌ isUp_False ... failed")
        print(f"Tests done. [{str(i)}/{str(cases)}]")


    def isUp_True(self, param):
        if not self.service.isUp(param):
            return False
        return True

    def isUp_False(self, param):
        if not self.service.isUp(param):
            return False
        return True


def main():
    # Start the service tests.
    service_test = ServiceTest()
    service_test.run()


if __name__ == '__main__':
    main()