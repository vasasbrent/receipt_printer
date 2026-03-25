const themeSelect = document.getElementById('theme-select');
const receipt = document.getElementById('receipt');
const headerEl = document.getElementById('receipt-header');
const messageInput = document.getElementById('message-input');
const senderLine = document.getElementById('sender-line');
const senderInput = document.getElementById('sender-input');
const submitBtn = document.getElementById('submit-btn');

const defaultSenders = {
  note: 'Psst, pass it on...',
  memo: 'Corporate',
};

const poets = [
  'William Shakespeare',
  'Emily Dickinson',
  'Robert Frost',
  'Langston Hughes',
  'Maya Angelou',
  'Walt Whitman',
  'Edgar Allan Poe',
  'Pablo Neruda',
  'Sylvia Plath',
  'T.S. Eliot',
  'Mary Oliver',
  'Diane Seuss',
];

let activePoet = null;

function randomPoet() {
  return poets[Math.floor(Math.random() * poets.length)];
}

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
  senderLine.style.display = 'none';
  senderInput.value = '';
  document.body.removeAttribute('data-theme');
});

// Theme switching
themeSelect.addEventListener('change', () => {
  const theme = themeSelect.value;
  receipt.className = 'receipt'; // reset any old theme class

  if (theme) {
    // Show the message box when a theme is selected
    messageInput.style.display = 'block';
    senderLine.style.display = 'flex';
    senderInput.value = '';
    activePoet = theme === 'poem' ? randomPoet() : null;
    senderInput.placeholder = activePoet ?? (defaultSenders[theme] || 'Anonymous');
    receipt.classList.add(theme);
    headerEl.textContent = headers[theme] || '';
    document.body.dataset.theme = theme;
  } else {
    // Hide message box, clear text, and reset visuals
    messageInput.style.display = 'none';
    messageInput.value = '';
    senderLine.style.display = 'none';
    senderInput.value = '';
    activePoet = null;
    headerEl.textContent = '';
    document.body.removeAttribute('data-theme');
  }
});

function showSentPopup() {
  const popup = document.getElementById('popup');
  popup.classList.add('show');
  setTimeout(() => popup.classList.remove('show'), 1500); // disappear after 1.5s
}

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
  if ((message.match(/\n/g) || []).length > 50) {
    // TODO: Improve message for frontend use.
    alert('Message has too many line breaks (max 50).');
    return;
  }

  submitBtn.disabled = true;

  const sender_name = senderInput.value.trim()
    || activePoet
    || defaultSenders[theme]
    || 'Anonymous';

  fetch('/print', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ theme, message, sender_name }),
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showSentPopup();
        messageInput.value = '';
      } else {
        alert('Print failed: ' + (data.error || 'Unknown error'));
      }
    })
    .catch(err => alert('Request failed: ' + err))
    .finally(() => { submitBtn.disabled = false; });
});
