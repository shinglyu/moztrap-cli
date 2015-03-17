#!/usr/bin/python
import argparse
import logging

import mtapi
import diff

logging.basicConfig(level=logging.INFO)


def main():
    # query = " ".join(sys.argv[1:])
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action",
                                       help="use \"[command] -h\" to see help message for individual command")

    parser_clone = subparsers.add_parser('clone')
    parser_clone.add_argument('resource_type', type=str,
                              choices=['caseversion', 'suite'], help="Resource type")
    parser_clone.add_argument('id', type=int, help="Resource ID")

    parser_diff = subparsers.add_parser('diff')
    parser_diff.add_argument('filename', type=str, help="File to be diffed")

    parser_push = subparsers.add_parser('push')
    parser_push.add_argument('-f', '--force', action="store_true",
                             help="Force overwrite (BE CAREFUL!)")
    parser_push.add_argument('filename', type=str, help="File to be pushed")

    args = parser.parse_args()

    # print args
    if args.action == "clone":
        mtapi.clone(args.resource_type, args.id)
    elif args.action == "diff":
        diff.diff(args)
    elif args.action == "push":
        raise NotImplementedError


if __name__ == '__main__':
    main()
