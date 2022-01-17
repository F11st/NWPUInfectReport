from infect_report import XgdYqtb
import os


def main():
    xgd_username = os.environ.get('xgd_username')
    xgd_password = os.environ.get('xgd_password')

    yq = XgdYqtb()
    yq.login(xgd_username, xgd_password)
    yq.checkin()


def main_handler(event, context):
    main()


if __name__ == '__main__':
    main()
