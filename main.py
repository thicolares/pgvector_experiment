"""
Main script for pgvector embeddings experiment.
Provides CLI interface for creating and querying embeddings.
"""

import argparse
import sys
from db import create_embeddings, query_embeddings


def main():
    parser = argparse.ArgumentParser(
        description="pgvector embeddings experiment - Create and query vector embeddings"
    )
    parser.add_argument(
        "operation",
        choices=["create", "query"],
        help="Operation to perform: 'create' to create embeddings, 'query' to query embeddings",
    )
    parser.add_argument(
        "--text", type=str, help="Text to create embedding from or to query with"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of results to return for query operation (default: 5)",
    )

    args = parser.parse_args()

    try:
        if args.operation == "create":
            if not args.text:
                print("Error: --text is required for create operation")
                sys.exit(1)
            create_embeddings(args.text)
            print(f"Successfully created embedding for: {args.text}")

        elif args.operation == "query":
            if not args.text:
                print("Error: --text is required for query operation")
                sys.exit(1)
            results = query_embeddings(args.text, limit=args.limit)
            print(f"\nTop {len(results)} results for query: '{args.text}'")
            for idx, result in enumerate(results, 1):
                print(f"{idx}. {result}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
