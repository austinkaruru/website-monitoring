# Website Monitor & Auto-Recovery

A Python application that continuously monitors your website's availability and automatically performs recovery actions when issues are detected.

## Features

- **Continuous Monitoring**: Checks website availability every 5 seconds
- **Email Notifications**: Sends alerts when issues are detected
- **Auto-Recovery**: Automatically restarts Docker containers and Linode servers
- **Error Handling**: Comprehensive error handling with appropriate recovery strategies

## How It Works

1. **Health Check**: Performs HTTP GET requests to monitor website status
2. **Container Restart**: First attempts to restart the Docker container if issues are detected
3. **Server Reboot**: If container restart fails, reboots the entire Linode server
4. **Notifications**: Sends email alerts for all detected issues and recovery actions

## Requirements

- Python 3.6+
- Linode account with API access
- Gmail account for notifications
- SSH access to your server
- Docker container running your application

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd website-monitor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (see Configuration section)

## Configuration

Create a `.env` file in the project root or set the following environment variables:

```bash
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASS=your-app-password
SERVER=https://your-website.com
USER=your-ssh-username
SSH_KEY=/path/to/your/ssh/private/key
LINODE_TOKEN=your-linode-api-token
LINODE_ID=your-linode-instance-id
HOSTNAME=your-server-hostname-or-ip
```

### Environment Variables Explained

- `EMAIL_USER`: Gmail address for sending notifications
- `EMAIL_PASS`: Gmail app password (not your regular password)
- `SERVER`: Full URL of the website to monitor
- `USER`: SSH username for your server
- `SSH_KEY`: Path to your SSH private key file
- `LINODE_TOKEN`: Linode API token for server management
- `LINODE_ID`: Linode instance ID of your server
- `HOSTNAME`: Server hostname or IP address

## Gmail Setup

1. Enable 2-factor authentication on your Gmail account
2. Generate an app password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Create a new app password for this application
3. Use the generated app password as `EMAIL_PASS`

## Linode Setup

1. Generate a Linode API token:
   - Log into Linode Cloud Manager
   - Go to Profile → API Tokens
   - Create a new token with appropriate permissions
2. Find your Linode instance ID in the Cloud Manager URL or API

## Usage

Run the monitor:
```bash
python monitor.py
```

The application will:
- Start monitoring immediately
- Check your website every 5 seconds
- Print status messages to console
- Send email notifications for issues
- Automatically attempt recovery actions

## Recovery Process

When an issue is detected:

1. **Container Restart**: Attempts to restart the Docker container
2. **Server Reboot**: If container restart fails, reboots the Linode server
3. **Wait for Recovery**: Waits for server to come back online
4. **Resume Monitoring**: Continues monitoring after recovery

## Customization

### Monitoring Interval
Change the monitoring frequency by modifying:
```python
schedule.every(5).seconds.do(monitor_application)
```

### Docker Container ID
Update the container ID in the `restart_container()` function:
```python
stdout = ssh.exec_command('docker start YOUR_CONTAINER_ID')
```

### Success Criteria
Modify the health check logic in `monitor_application()` to match your requirements.

## Logging

The application prints status messages to the console. For production use, consider adding file logging:

```python
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
```

## Security Considerations

- Store sensitive information in environment variables
- Use SSH key authentication instead of passwords
- Restrict API token permissions to minimum required
- Use Gmail app passwords, not account passwords

## Troubleshooting

### Common Issues

1. **SSH Connection Failed**: Verify hostname, username, and SSH key path
2. **Email Not Sending**: Check Gmail app password and 2FA setup
3. **Linode API Errors**: Verify token permissions and instance ID
4. **Docker Container Not Found**: Update container ID in script

### Debug Mode

Add debugging output by uncommenting print statements or adding:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please create an issue in the repository or contact the maintainer.