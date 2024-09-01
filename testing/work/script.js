// Fetch device status from the server (e.g., Raspberry Pi)
function fetchDeviceStatus() {
    // Make an AJAX request to fetch the device status
    // and update the HTML content accordingly
    // You can use a library like Fetch or Axios for this
  
    // Example implementation using Fetch
    fetch('/device-status')
      .then(response => response.json())
      .then(data => {
        updateDeviceStatus(data);
      })
      .catch(error => {
        console.error('Error fetching device status:', error);
      });
  }
  
  function updateDeviceStatus(data) {
    let deviceStatusHTML = '';
  
    data.forEach(device => {
      deviceStatusHTML += `
        <table>
          <tr>
            <th>Device</th>
            <th>Status</th>
            <th>ESD Status</th>
          </tr>
          <tr>
            <td>${device.name}</td>
            <td>${device.status}</td>
            <td>${device.esdStatus}</td>
          </tr>
        </table>
      `;
    });
  
    document.getElementById('device-status').innerHTML = deviceStatusHTML;
  }
  
  // Toggle dark/light mode
  // Toggle dark/light mode
  function toggleMode() {
    document.body.classList.toggle('light-mode');
    document.body.classList.toggle('dark-mode');
    const switchInput = document.getElementById('switch-input');
    switchInput.checked = document.body.classList.contains('dark-mode');
  }
  
  // Add event listener to the switch input
  document.getElementById('switch-input').addEventListener('change', toggleMode);
  
  // Fetch device status initially
  fetchDeviceStatus();
  
  // Fetch device status periodically (e.g., every 5 seconds)
  setInterval(fetchDeviceStatus, 5000);