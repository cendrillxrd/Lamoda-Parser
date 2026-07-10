from utils.db_helper import save_info
from workers.info_collector import InfoCollector
from workers.info_redactor import InfoRedactor


def main():
    info_collector = InfoCollector()
    info = info_collector.collect_info()

    info_redactor = InfoRedactor()
    result = info_redactor.redact_info(info)

    save_info(result)


if __name__ == '__main__':
    main()
