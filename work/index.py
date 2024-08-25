import network  # type: ignore
import asyncio
import socket
import time
import random
from machine import Pin  #type: ignore

ssid = 'Airtel_9945511001_5GHz'
password = 'air84391'

led_blink = Pin(20, Pin.OUT)
led_control = Pin(19, Pin.OUT)

state = "OFF"
random_value = 0

def webpage(random_value, state):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>ESD Monitoring Status</title>
      <style>
        /* Define your styles here */
        :root {{
            --bg-color-light: #fff;
            --text-color-light: #000;
            --bg-color-dark: #333;
            --text-color-dark: #fff;
            --switch-width: 60px;
            --switch-height: 34px;
            --switch-bg-color: #ccc;
            --switch-active-color: #4CAF50;
            --icon-safe-color: #4CAF50;
            --icon-unsafe-color: #f44336;
          }}
          
          body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            transition: background-color 0.4s, color 0.4s;
          }}
          
          body.light-mode {{
            background-color: var(--bg-color-light);
            color: var(--text-color-light);
          }}
          
          body.dark-mode {{
            background-color: var(--bg-color-dark);
            color: var(--text-color-dark);
          }}
          
          table {{
            width: 100%;
            border-collapse: collapse;
          }}
          
          th, td {{
            padding: 10px;
            text-align: left;
          }}
          
          .switch-container {{
            position: absolute;
            top: 20px;
            right: 20px;
            display: inline-block;
            width: var(--switch-width);
            height: var(--switch-height);
          }}
          
          .switch {{
            position: relative;
            display: inline-block;
            width: var(--switch-width);
            height: var(--switch-height);
          }}
          
          .switch input {{
            opacity: 0;
            width: 0;
            height: 0;
          }}
          
          .slider {{
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: var(--switch-bg-color);
            -webkit-transition: .4s;
            transition: .4s;
          }}
          
          .slider:before {{
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            -webkit-transition: .4s;
            transition: .4s;
          }}
          
          input:checked + .slider {{
            background-color: var(--switch-active-color);
          }}
          
          input:focus + .slider {{
            box-shadow: 0 0 1px var(--switch-active-color);
          }}
          
          input:checked + .slider:before {{
            -webkit-transform: translateX(26px);
            -ms-transform: translateX(26px);
            transform: translateX(26px);
          }}
          
          .slider.round {{
            border-radius: 34px;
          }}
          
          .slider.round:before {{
            border-radius: 50%;
          }}
          
          .icon {{
            font-size: 18px;
            font-weight: bold;
          }}
          
          .icon.safe {{
            color: var(--icon-safe-color);
          }}
          
          .icon.unsafe {{
            color: var(--icon-unsafe-color);
          }}

          .status-container {{
            margin-top: 20px;
            font-size: 18px;
          }}
          
          .status-item {{
            margin-bottom: 10px;
          }}

          .date-time {{
            margin-top: 20px;
            font-size: 16px;
          }}
      </style>
    </head>
    <body class="light-mode">
      <div class="switch-container">
        <label class="switch">
          <input type="checkbox" id="switch-input">
          <span class="slider round"></span>
        </label>
      </div>
    
      <h1>ESD Monitoring Status</h1>
    
      <div class="status-container">
        <div class="status-item">Devices: Loading...</div>
        <div class="status-item">Device Status: Loading...</div>
        <div class="status-item">ESD Status: Safe</div>
      </div>
    
      <div class="date-time" id="date-time"></div>
    
      <script>
        // Fetch device status from the server (e.g., Raspberry Pi)
        function fetchDeviceStatus() {{
            // Example implementation using Fetch
            fetch('/device-status')
              .then(response => response.json())
              .then(data => {{
                updateDeviceStatus(data);
              }})
              .catch(error => {{
                console.error('Error fetching device status:', error);
              }});
          }}
          
          function updateDeviceStatus(data) {{
            let deviceStatusHTML = '';
          
            data.forEach(device => {{
              deviceStatusHTML += `
                <tr>
                  <td>${{device.name}}</td>
                  <td>${{device.status}}</td>
                  <td><span class="icon safe">&#9679;</span></td>
                </tr>
              `;
            }});
          
            document.getElementById('device-status').innerHTML = deviceStatusHTML;
          }}
          
          // Toggle dark/light mode
          function toggleMode() {{
            document.body.classList.toggle('light-mode');
            document.body.classList.toggle('dark-mode');
            const switchInput = document.getElementById('switch-input');
            switchInput.checked = document.body.classList.contains('dark-mode');
          }}
          
          // Add event listener to the switch input
          document.getElementById('switch-input').addEventListener('change', toggleMode);
          
          // Fetch device status initially
          fetchDeviceStatus();
          
          // Fetch device status periodically (e.g., every 5 seconds)
          setInterval(fetchDeviceStatus, 5000);

          // Update date and time every second
          function updateDateTime() {{
            const now = new Date();
            const options = {{ 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric',
              hour: 'numeric',
              minute: 'numeric',
              second: 'numeric'
            }};
            const dateTimeString = `Date: ${{now.toLocaleDateString(undefined, options)}} | Time: ${{now.toLocaleTimeString()}}`;
            document.getElementById('date-time').textContent = dateTimeString;
          }}

          // Update date and time every second
          setInterval(updateDateTime, 1000);
          updateDateTime(); // Initial call to display the date-time immediately
      </script>
    </body>
    </html>
    """
    return str(html)




def init_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    wlan.connect(ssid, password)
    
    connection_timeout = 10
    while connection_timeout > 0:
        print(wlan.status())
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        time.sleep(1)
    
    if wlan.status() != 3:
        print('Failed to connect to Wi-Fi')
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True


async def handle_client(reader, writer):
    global state
    
    print("Client connected")
    request_line = await reader.readline()
    print('Request:', request_line)
    
    
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line, 'utf-8').split()[1]
    print('Request:', request)
    
    
    if request == '/lighton?':
        print('LED on')
        led_control.value(1)
        state = 'ON'
    elif request == '/lightoff?':
        print('LED off')
        led_control.value(0)
        state = 'OFF'
    elif request == '/value?':
        global random_value
        random_value = random.randint(0, 20)

    
    response = webpage(random_value, state)  

    
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()
    print('Client Disconnected')
    
async def blink_led():
    while True:
        led_blink.toggle()  
        await asyncio.sleep(0.5)  

async def main():    
    if not init_wifi(ssid, password):
        print('Exiting program.')
        return
    
    
    print('Setting up server')
    server = asyncio.start_server(handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)
    asyncio.create_task(blink_led())
    
    while True:
        
        await asyncio.sleep(5)
        print('This message will be printed every 5 seconds')
        


loop = asyncio.get_event_loop()

loop.create_task(main())

try:
    
    loop.run_forever()
except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')