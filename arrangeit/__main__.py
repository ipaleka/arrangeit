import logging

from arrangeit.utils import get_component_class


def main():
    """Retrieves, instantiates and runs platform specific app.

    Configures logger at the start.
    """
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    app_class = get_component_class("App")
    app_class().run()


if __name__ == "__main__":
    main()
