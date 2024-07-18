document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
  document.querySelector('#compose-view').addEventListener('submit',send_email)
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-mail').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-mail').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 style="color:blue;">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(mail=>{
      if (mailbox==='sent'){
        let element =document.createElement('div');
        element.className = mail.read ? "list-group-item-primary" : "list-group-item";
        element.innerHTML = `
        <h2>${mail['recipients'][0]}</h2>
        <h4>Sub: ${mail.subject}</h4>
        <p>${mail.timestamp}</p>
        `;
        element.addEventListener('click',()=> view_mail(mail,mailbox)
        );
        document.querySelector('#emails-view').append(element);

      }
      else{
        let element = document.createElement('div');
        element.className = mail.read ? "list-group-item-primary" : "list-group-item";
        element.innerHTML = `
        <h2>${mail.sender}</h2>
        <h4>Sub: ${mail.subject}</h4>
        <p>${mail.timestamp}</p>
        `;
        element.addEventListener('click',()=> view_mail(mail,mailbox)
        );
        document.querySelector('#emails-view').append(element);
      }
    })
});
}

function send_email(event){
  event.preventDefault();
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
      document.querySelector('#compose-body').value = '';
      document.querySelector('#compose-subject').value = '';
      document.querySelector('#compose-recipients').value = '';

  });
}

function view_mail(mail,mailbox){
  document.querySelector('#single-mail').style.display='block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  if(mailbox==='sent'){
  let element = document.createElement('div');
  element.className = "info-box";
  element.innerHTML = `
  <div>
     <h2 style="color:blue; margin-bottom:35px;">${mail.subject}</h2>
     <p><strong>From: </strong>${mail.sender}</p>
     <p><strong>To: </strong>${mail.recipients[0]}</p>
     <p><strong>Time: </strong>${mail.timestamp}</p>
  </div>
  <hr style=" border-top: 1px solid blue;">
  <p>${mail.body}</p>
  `;
  fetch(`/emails/${mail.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  document.querySelector('#single-mail').innerHTML = element.innerHTML;
 }
 else{
  let element = document.createElement('div');
  element.className = "info-box";
  element.innerHTML = `
  <div>
     <h2 style="color:blue; margin-bottom:35px;">${mail.subject}</h2>
     <p><strong>From: </strong>${mail.sender}</p>
     <p><strong>To: </strong>${mail.recipients[0]}</p>
     <p><strong>Time: </strong>${mail.timestamp}</p>
  </div>
  <hr style=" border-top: 1px solid blue;">
  `;
  let mail_body = document.createElement('div');
  mail_body.className = "mail_body";
  mail_body.innerHTML = `
  <p>${mail.body}</p>
  `;
  if(!mail.read){
  fetch(`/emails/${mail.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })

  })
}
const archive_button = document.createElement('button');
archive_button.innerHTML = mail.archived ? "Unarchive" : "Archive";
archive_button.className = mail.archived ? "btn btn-success" : "btn btn-danger";
archive_button.addEventListener('click', function(){
  fetch(`/emails/${mail.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !mail.archived
    })
    })
    .then(() => {
      load_mailbox('archive');
  })
})
const reply_button = document.createElement('button');
reply_button.innerHTML = "Reply";
reply_button.className = "btn btn-primary";
reply_button.addEventListener('click', function(){
  compose_email(),
  document.querySelector('#compose-recipients').value = mail.sender;
  document.querySelector('#compose-recipients').readOnly = true;
  document.querySelector('#compose-subject').value = `Re: ${mail.subject}`;
  document.querySelector('#compose-subject').readOnly = true;
  document.querySelector('#compose-body').value = `\n\n\n\n\n\nOn ${mail.timestamp} ${mail.sender} wrote:\nSee the Subject`
})

  document.querySelector('#single-mail').innerHTML = element.innerHTML;
  document.querySelector('#single-mail').append(mail_body);
  document.querySelector('#single-mail').append(archive_button);
  document.querySelector('#single-mail').append(reply_button);
}

}

