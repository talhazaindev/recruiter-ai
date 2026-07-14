"""Ingest (Drive) queue worker entrypoint."""

from run_worker import main

if __name__ == "__main__":
    import sys

    sys.argv = [sys.argv[0], "ingest"]
    main()
