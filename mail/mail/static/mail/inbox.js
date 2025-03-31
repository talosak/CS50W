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
  document.querySelector('#email-view').style.display = 'none';
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
  document.querySelector('#email-view').style.display = 'none';


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
      div.innerHTML = `<h4><div class="row">
                        <div class="col-3"><strong> ${email.sender}</strong></div>
                        <div class="col-6 ml-n5"><span> ${email.subject}</span></div>
                        <div class="col-3 ml-5"><span style="color:gray"> ${email.timestamp}</span></div>
                        </div></h4>`;
      div.style.border = 'solid 2px #232323';
      div.style.padding = '10px';
      div.style.cursor = 'pointer';
      if (email.read) {
        div.style.backgroundColor = 'gray';
      } else {
        div.style.backgroundColor = 'white';
      }
      div.addEventListener('click', () => {view_email(email.id)});
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

function view_email(email_id) {
  // Get the email via ID
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Load the email's page
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'none';

    document.querySelector('#email-sender').innerHTML = email.sender;
    document.querySelector('#email-recipients').innerHTML = email.recipients;
    document.querySelector('#email-subject').innerHTML = email.subject;
    document.querySelector('#email-timestamp').innerHTML = email.timestamp;
    document.querySelector('#email-body').innerHTML = email.body;
  });

  // Mark email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  }); 
}