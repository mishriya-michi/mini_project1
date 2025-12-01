const backendURL = "http://127.0.0.1:8000";

// -------------------- UI Helpers --------------------
function goToDecrypt() {
  const section = document.querySelector(".panel");
  section.scrollIntoView({ behavior: "smooth" });
}

function openDocs() {
  window.open(backendURL + "/docs", "_blank");
}

function autoFillLatest() {
  const last = localStorage.getItem('lastUploaded');
  const statusEl = document.getElementById('status');
  if (last) {
    document.getElementById('decryptFilename').value = last;
    statusEl.innerText = 'Filename loaded: ' + last;
    statusEl.classList.add('blink');
    setTimeout(() => statusEl.classList.remove('blink'), 2000);
  } else {
    alert('No last file saved. Upload one first.');
  }
}

function showWarning() {
  document.getElementById('warningBox').style.display = 'block';
}
function hideWarning() {
  document.getElementById('warningBox').style.display = 'none';
}

// -------------------- File Upload --------------------
async function uploadFile() {
  const fi = document.getElementById('fileInput');
  if (!fi.files || !fi.files[0]) { alert('Select a file first'); return; }
  const f = fi.files[0];
  const fd = new FormData();
  fd.append('file', f);

  const statusEl = document.getElementById('status');
  statusEl.innerHTML = '<div class="spinner" style="margin:6px auto"></div> Uploading...';
  statusEl.style.fontSize = '25px';

  try {
    const res = await fetch(backendURL + '/upload', { method: 'POST', body: fd });
    const j = await res.json();
    if (j.status === 'success') {
      document.getElementById('decryptFilename').value = j.filename;
      localStorage.setItem('lastUploaded', j.filename);
      statusEl.innerText = 'Upload successful: ' + j.filename;
      statusEl.classList.add('blink');
      setTimeout(() => statusEl.classList.remove('blink'), 2000);
    } else {
      statusEl.innerText = 'Upload error: ' + (j.message || JSON.stringify(j));
    }
  } catch (e) {
    statusEl.innerText = 'Upload failed: ' + e.message;
  }
}

// -------------------- File Decrypt --------------------
async function decryptFile() {
  const filename = document.getElementById('decryptFilename').value;
  if (!filename) { alert('Enter or upload filename first'); return; }
  const statusEl = document.getElementById('status');
  statusEl.innerHTML = '<div class="spinner"></div> Decrypting...';
  statusEl.style.fontSize = '25px';

  try {
    const res = await fetch(backendURL + '/decrypt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename })
    });
    const j = await res.json();
    if (j.status === 'success') {
      statusEl.innerText = 'Decryption success → ' + j.decrypted_file;
      statusEl.classList.add('blink');
      setTimeout(() => statusEl.classList.remove('blink'), 2000);

      const dl = document.getElementById('downloadLink');
      dl.href = backendURL + '/download/' + encodeURIComponent(j.decrypted_file);
      dl.style.display = 'inline-block';
      dl.onclick = () => setTimeout(() => alert('🎉 Your file has been successfully decrypted and downloaded!'), 300);
    } else {
      statusEl.innerText = 'Decrypt failed: ' + (j.message || JSON.stringify(j));
    }
  } catch (e) {
    statusEl.innerText = 'Decryption error: ' + e.message;
  }
}

// -------------------- Blink Hero Title on Load --------------------
window.addEventListener('load', () => {
  const heroTitle = document.querySelector('.hero-left h1');
  if (heroTitle) {
    heroTitle.classList.add('blink');
    setTimeout(() => heroTitle.classList.remove('blink'), 5000);
  }
});
// Show popup on page load
window.addEventListener('load', () => {
  const popup = document.getElementById('welcomePopup');
  popup.classList.add('show');
});

// Close popup
function closePopup() {
  const popup = document.getElementById('welcomePopup');
  popup.classList.remove('show');
}