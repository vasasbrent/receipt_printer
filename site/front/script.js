const themeSelect = document.getElementById('theme-select');
const receipt = document.getElementById('receipt');
const headerEl = document.getElementById('receipt-header');
const messageInput = document.getElementById('message-input');
const submitBtn = document.getElementById('submit-btn');

// ASCII headers for each theme
const headers = {
  note:
`        ______________________________________
       |   __    _   ___    _______ .____     |
       |   |\\   |  .'   \`. '   /    /         |
       |   | \\  |  |     |     |    |__.      |
       |   |  \\ |  |     |     |    |         |
       |   |   \\|   \`.__.'     /    /----/    |
       |______________________________________|`,
  poem:
`      _________________________________________
      |    .-.                                |
      |   (_) )-.                             |
      |     .:   \\  .-.    .-.  . ,';.,';.    |
      |    .:'    );   ;'.;.-'  ;;  ;;  ;;    |
      |  .-:. \`--' \`;;'   \`:::'';  ;;  ';     |
      | (_/                   _;        \`-'   |
      |_______________________________________|`,
  memo:
`        ______________________________________
       |    __  __  ______  __  __   ____     |
       |   |  \\/  ||  ____||  \\/  | / __ \\    |
       |   | \\  / || |__   | \\  / || |  | |   |
       |   | |\\/| ||  __|  | |\\/| || |  | |   |
       |   | |  | || |____ | |  | || |__| |   |
       |   |_|  |_||______||_|  |_| \\____/    |
       |______________________________________|`
};

// Reset to default on page load
window.addEventListener('DOMContentLoaded', () => {
  themeSelect.selectedIndex = 0; // Reset dropdown to "Select a theme"
  headerEl.textContent = "";     // Clear header
  messageInput.value = "";       // Clear message box
  messageInput.style.display = 'none'; // Hide message box
  document.body.style.backgroundColor = '#f2f2f2'; // Default background
});

// Theme switching
themeSelect.addEventListener('change', () => {
  const theme = themeSelect.value;
  receipt.className = 'receipt'; // reset any old theme class

  if (theme) {
    // Show the message box when a theme is selected
    messageInput.style.display = 'block';
    receipt.classList.add(theme);
    headerEl.textContent = headers[theme] || '';

    // Theme backgrounds
    switch (theme) {
      case 'note':
        document.body.style.backgroundColor = '#645200';
        break;
      case 'poem':
        document.body.style.backgroundColor = '#f3e5f5';
        break;
      case 'memo':
        document.body.style.backgroundColor = '#e0e0e0';
        break;
    }
  } else {
    // Hide message box, clear text, and reset visuals
    messageInput.style.display = 'none';
    messageInput.value = '';
    headerEl.textContent = '';
    document.body.style.backgroundColor = '#ffffff';
  }
});

function showSentPopup() {
  const popup = document.getElementById('popup');
  popup.classList.add('show');
  setTimeout(() => popup.classList.remove('show'), 1500); // disappear after 1.5s
}

// Submit placeholder
submitBtn.addEventListener('click', () => {
  const theme = themeSelect.value;
  const message = messageInput.value.trim();

  if (!theme) {
    alert('Please select a theme.');
    return;
  }
  if (!message) {
    alert('Please enter a message.');
    return;
  }

  // Show popup
  showSentPopup();

  // Clear message box
  messageInput.value = '';

  console.log(`Theme: ${theme}, Message: ${message}`);
});
