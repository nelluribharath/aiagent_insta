const form = document.getElementById('postForm');
const responseDiv = document.getElementById('response');

const API_ENDPOINT = "http://localhost:8000/post_to_instagram/";

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  
  const usernameInput = document.getElementById('usernameInput');
  const passwordInput = document.getElementById('passwordInput');
  const textInput = document.getElementById('textInput');
  const captionInput = document.getElementById('captionInput');
  const tokenInput = document.getElementById('tokenInput');

  const formData = new FormData();
  formData.append('username', usernameInput.value);
  formData.append('password', passwordInput.value);
  formData.append('text', textInput.value);
  formData.append('caption', captionInput.value);
  formData.append('token', tokenInput.value);

  try {
    const res = await fetch(API_ENDPOINT, {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    responseDiv.innerText = data.message || "Post successful!";
  } catch (err) {
    responseDiv.innerText = "Error posting: " + err.message;
  }
});
