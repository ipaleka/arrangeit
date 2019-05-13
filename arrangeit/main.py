from arrangeit.utils import get_app


def main():
    app_class = get_app()
    app_class().run()


if __name__ == "__main__":
    main()