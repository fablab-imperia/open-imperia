import argparse
import logging

from collectors.core.registry import discover_sources, get_source


def main():
    parser = argparse.ArgumentParser(description="OpenImperia data collectors")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--source")
    group.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    sources = discover_sources()

    if args.list:
        for source in sources:
            print(f"{source.name}\t{source.title}")
        return

    selected = sources if args.all else [get_source(args.source)]

    for source in selected:
        logging.info("Running source: %s", source.name)
        source.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
