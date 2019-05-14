from arrangeit.utils import get_app


def main():
    """Retrieves, instantiates and runs platform specific app."""
    app_class = get_app()
    app_class().run()


if __name__ == "__main__":
    main()