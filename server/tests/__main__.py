import logging
import os
import unittest

import xmlrunner


def enable_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s,%(msecs)d %(levelname)s - %(name)s:%(funcName)s - %(message)s",
        datefmt="%H:%M:%S",
    )


if __name__ == "__main__":
    enable_logging(logging.ERROR)

    root_dir = os.path.dirname(__file__)
    test_loader = unittest.TestLoader()
    package_tests = test_loader.discover(start_dir=root_dir)

    testRunner = xmlrunner.XMLTestRunner(output="test-reports")
    testRunner.run(package_tests)
