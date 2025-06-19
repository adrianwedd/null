#!/usr/bin/env python3
import argparse
import sys
import runpy

import thought_logger


def main():
    parser = argparse.ArgumentParser(description="Run a Python module with thought logging")
    parser.add_argument("module", help="Module to run as __main__")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parser.add_argument("--redact-think", action="store_true", dest="redact_think",
                        help="Redact contents of <think> blocks in stdout/stderr")
    args = parser.parse_args()

    thought_logger.install(redact=args.redact_think)
    sys.argv = [args.module] + args.args
    runpy.run_module(args.module, run_name="__main__")


if __name__ == "__main__":
    main()
