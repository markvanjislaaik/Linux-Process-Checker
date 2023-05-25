import logging
import sys
import time

import schedule
import paramiko

from ssh_config import servers
from mailer import EmailSender

log_format = ('[%(asctime)s] - %(levelname)s %(name)s %(funcName)s %(message)s')
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def check_processes() -> None:

    for server in servers:
        hostname = server
        username = servers[server]['username']
        password = servers[server]['password']
        port = servers[server]['port']
        processes = servers[server]['processes']

        try:

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port=port, username=username, password=password)

            for process_name in processes:
                
                command = f"ps aux | grep '{process_name}' | grep -v grep"
                _, stdout, _ = client.exec_command(command)
                output = stdout.read().decode().strip()

                if output:
                    logger.info(f"Process '{process_name}' on '{hostname}' is running.")
                else:
                    logger.critical(f"Process '{process_name}' on '{hostname}' is not running.")
                    email_header = f"Service {process_name} is NOT RUNNING!"
                    subject = f"Linux Service Down | {process_name}"

                    custom_message_body = f"""
                    <p>This service is NOT RUNNING</p>
                    <p>You need to check on {hostname}</p>
                    """
                    
                    email = EmailSender()
                    email.send_email(subject, custom_message_body, email_header)

            client.close()

        except Exception as client_error:

            email_header = f"Server Client {hostname} is UNREACHABLE!"
            subject = f"Linux Server Down | {process_name}"

            custom_message_body = f"""
            <p>This server is UNREACHABLE</p>
            <p>You need to check on {hostname}</p>
            <p> ERROR: {client_error}</p>
            """

            email = EmailSender()
            email.send_email(subject, custom_message_body, email_header)


if __name__ == '__main__':
    
    check_processes()

    schedule.every(10).minutes.do(check_processes)

    while True:
        schedule.run_pending()
        time.sleep(1)