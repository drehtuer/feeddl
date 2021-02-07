#!/usr/bin/env python3
"""
feeddl - podcatcher/feed encosure downloader
"""

import argparse
import sys
import FeedDl

"""
Default values
"""
DEFAULT_CONFIG = '~/.config/feeddl/config'

"""
Map FeedDl functions
"""
CMD_DOWNLOAD='download'
CMD_FEEDS='feeds'
CMD_EPISODES='episodes'
CMD_RAW='raw'
CMD_VERSION='version'


def build_parser(arg0):
    """
    Build input parser
    """
    parser = argparse.ArgumentParser(
            '{} - podcatcher/feed enclosure downloader'.format(arg0)
    )
    
    parser.add_argument(
            '--config',
            type=str,
            help='Configuration file (default: \'{}\''.format(DEFAULT_CONFIG)
    )
    parser.add_argument(
            '--version',
            action='store_true',
            help='Print out version'
    )

    subparsers = parser.add_subparsers()

    parser_feeds = subparsers.add_parser(
            'feeds',
            help='Show all feeds'
    )
    parser_feeds.set_defaults(cmd=CMD_FEEDS)

    parser_episodes = subparsers.add_parser(
            'episodes',
            help='List all episodes for a feed'
    )
    parser_episodes.add_argument(
            'name',
            type=str,
            help='Name of the feed to list episodes for'
    )
    parser_episodes.set_defaults(cmd=CMD_EPISODES)

    parser_download = subparsers.add_parser(
            'download',
            help='Download latest enclosures from all feeds'
    )
    parser_download.add_argument(
            '--dryrun',
            action='store_true',
            help='Dry run, do not download anything'
    )
    parser_download.set_defaults(cmd=CMD_DOWNLOAD)

    parser_raw = subparsers.add_parser(
            'raw',
            help='Show raw feed'
    )
    parser_raw.add_argument(
            'name',
            type=str,
            help='Name of the feed to show as raw'
    )
    parser_raw.set_defaults(cmd=CMD_RAW)

    return parser


def main(argv):
    """
    main function
    Parses input and starts FeedDl function
    (with possible paramteres)
    """
    parser = build_parser(argv[0])
    args = parser.parse_args(argv[1:])
    if args.version:
        """
        Handle version check
        Done after version check
        """
        print('{} version: \'{}\''.format(argv[0], FeedDl.FeedDl.version()))
        parser.exit(0)
    try:
        cmd = args.cmd
    except AttributeError:
        """
        No parameter given,
        show usage and exit
        """
        parser.print_usage()
        parser.exit(1)

    """
    Call function from FeedDl class
    and hand over args
    """
    feeddl = FeedDl.FeedDl(args.config)
    func = getattr(feeddl, cmd)
    func(args)

if __name__ == '__main__':
    """
    Entry point
    """
    main(sys.argv)
