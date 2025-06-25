import argparse
import get_data
import extract_data
import auto_request

def main():
    parser = argparse.ArgumentParser(prog="aldi-refill")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("get")
    subparsers.add_parser("extract")
    subparsers.add_parser("request")

    args = parser.parse_args()

    if args.command == "get":
        get_data.run()
    elif args.command == "extract":
        extract_data.run()
    elif args.command == "request":
        auto_request.run()
    elif args.command == "auto":
        auto_check.run()

if __name__ == "__main__":
    main()
