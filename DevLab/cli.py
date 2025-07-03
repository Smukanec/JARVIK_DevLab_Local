import argparse

from .dev_engine import DevEngine


def main() -> None:
    """Run DevLab from the command line."""
    parser = argparse.ArgumentParser(description="Run DevLab prompts")
    parser.add_argument("prompt", nargs="?", help="Prompt to send to the engine")
    parser.add_argument("--config", dest="config", help="Optional config file path")
    parser.add_argument("--log", action="store_true", help="Log output to file")
    args = parser.parse_args()

    engine = DevEngine(config_path=args.config)
    if args.prompt:
        print(engine.run(args.prompt, log=args.log))
        return

    # Interactive mode
    print("Enter prompt (blank line to exit):")
    while True:
        try:
            prompt = input("devlab> ")
        except EOFError:
            break
        if not prompt:
            break
        result = engine.run(prompt, log=args.log)
        print(result)


if __name__ == "__main__":
    main()

