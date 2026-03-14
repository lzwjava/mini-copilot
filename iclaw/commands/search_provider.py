import os

SEARCH_PROVIDERS = ["duckduckgo", "startpage", "bing", "tavily"]


def handle_search_provider_command(search_provider):
    print(f"\nCurrent search provider: {search_provider}")
    print("Available providers:")
    for i, prov in enumerate(SEARCH_PROVIDERS, 1):
        marker = "*" if prov == search_provider else " "
        print(f"  {marker} {i}. {prov}")

    try:
        choice = input(
            "Select search provider (number, Enter to keep current): "
        ).strip()
        if choice:
            if choice.isdigit():
                n = int(choice)
                if 1 <= n <= len(SEARCH_PROVIDERS):
                    provider = SEARCH_PROVIDERS[n - 1]
                    if provider == "tavily" and not os.getenv("TAVILY_API_KEY"):
                        print(
                            "TAVILY_API_KEY environment variable not found. Please set it to use Tavily.\n"
                        )
                        api_key = input("Enter your Tavily API key: ").strip()
                        if api_key:
                            os.environ["TAVILY_API_KEY"] = api_key
                            print("TAVILY_API_KEY set for this session.\n")
                        else:
                            print(
                                "Tavily API key not provided. Keeping current selection.\n"
                            )
                            return search_provider

                    print(f"Search provider set to: {provider}\n")
                    return provider
                else:
                    print("Invalid selection.\n")
            else:
                print("Please enter a number.\n")
    except (EOFError, KeyboardInterrupt):
        print()

    return search_provider
