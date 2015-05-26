#!/usr/bin/python
import argparse
import logging

import mtapi
import diff

#logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)


def main():
    # query = " ".join(sys.argv[1:])
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action",
                                       help="use \"[command] -h\" to see help message for individual command")

    parser_clone = subparsers.add_parser('clone')
    parser_clone.add_argument('resource_type', type=str,
                              choices=['caseversion', 'case', 'suite'], help="Resource type")
    parser_clone.add_argument('id', type=int, help="Resource ID")

    parser_diff = subparsers.add_parser('diff')
    parser_diff.add_argument('filename', type=str, help="File to be diffed")

    parser_push = subparsers.add_parser('push')
    parser_push.add_argument('-f', '--force', action="store_true",
                             help="Force overwrite (BE CAREFUL!)", required=True)
    parser_push.add_argument('filename', type=str, help="File to be pushed")
    parser_push.add_argument('-u', '--username',
                             help="MozTrap username", required=True)
    parser_push.add_argument('-k', '--api_key',
                             help="MozTrap api key", required=True)

    parser_push = subparsers.add_parser('create')
    # parser_push.add_argument('-f', '--force', action="store_true",
    #                          help="Force overwrite (BE CAREFUL!)", required=True)
    parser_push.add_argument('filename', type=str, help="File to be created")
    parser_push.add_argument('-u', '--username',
                             help="MozTrap username", required=True)
    parser_push.add_argument('-k', '--api_key',
                             help="MozTrap api key", required=True)
    args = parser.parse_args()

    # #print args
    if args.action == "clone":
        mtapi.clone(args.resource_type, args.id)
    elif args.action == "diff":
        diff.diff(args)
    elif args.action == "push":
        #if not args.force:
        #    raise Exception("Push will force override everything on the server."
        #                     + " Use \"push -f\" to acknowledge the risk")
        credental = {'username': args.username, 'api_key': args.api_key}
        mtapi.push(args.filename, credental)

    elif args.action == "create":
        #if not args.force:
        #    raise Exception("Push will force override everything on the server."
        #                     + " Use \"push -f\" to acknowledge the risk")
        credental = {'username': args.username, 'api_key': args.api_key}
        mtapi.create(args.filename, credental)


if __name__ == '__main__':
    main()
