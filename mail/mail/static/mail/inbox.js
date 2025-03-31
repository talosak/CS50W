document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Send an email upon submitting the form
  document.querySelector('#compose-form').addEventListener('submit', send_email);
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    // Render emails
    emails.forEach(email => {
      let div = document.createElement('div');
      div.innerHTML = `<h4> Email from: ${email.sender}<h4>
                        <h3> Subject: ${email.subject}<h3>
                        <h5> Date of creation: ${email.timestamp}`;
      div.style.border = 'solid 2px #232323';
      div.style.padding = '10px';
      if (email.read) {
        div.style.backgroundColor = 'gray';
      } else {
        div.style.backgroundColor = 'white';
      }
      document.querySelector('#emails-view').append(div);
    });
  });
}

function send_email(event) {
  // Prevent form from submitting normally
  event.preventDefault();

  // Send POST request to /emails route
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json()); 

  // Load user's sent mailbox
  load_mailbox('sent');
}