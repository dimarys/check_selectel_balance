# check_selectel_balance
Get early warning from Nagios before your balance at Selectel runs out of credits.

## Usage

1. Get the API key in the Selectel control panel.
2. Add the following to Nagios configuration files:

### commands.cfg

<pre>define command {
    command_name check_selectel_balance
    command_line /path/to/check_selectel_balance.py -t $ARG1$ -s $ARG2$ -w $ARG3$ -c $ARG4$
}</pre>

### services.cfg
<pre>define service{
    use generic-service
    host_name SERVER_NAME
    service_description Selectel balance
    is_volatile 0
    check_period 24x7
    max_check_attempts 3
    normal_check_interval 720
    retry_check_interval 5
    contact_groups admins
    notification_interval 120
    notification_period 24x7
    notification_options w,u,c,r
    check_command check_selectel_balance!SELECTEL_API_KEY!vpc!10!5
}</pre>
