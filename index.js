



const firebaseConfig = {
    apiKey: "AIzaSyBXuXtRBRifocqMWUptGaWoqnTnSTnjLTU",
    authDomain: "qrbased-ticket.firebaseapp.com",
    databaseURL: "https://qrbased-ticket-default-rtdb.firebaseio.com",
    projectId: "qrbased-ticket",
    storageBucket: "qrbased-ticket.appspot.com",
    messagingSenderId: "1032753801278",
    appId: "1:1032753801278:web:8b4b186a7cdb7f935ac96f"
  };


firebase.initializeApp(firebaseConfig);

var ticketdb = firebase.database().ref('tickets')
document.getElementById('registrationform').addEventListener('submit', submitform);

function generateTicketId() {
const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
let result = '';
for (let i = 0; i < 6; i++) {
  result += chars.charAt(Math.floor(Math.random() * chars.length));
}
return result;
}

function submitform(e){
e.preventDefault();

var name = getElementvalue('name');
var emailid = getElementvalue('emailid');
var seatnum = getElementvalue('seatnum');
var nationality = getElementvalue('nationality');
var dob = getElementvalue('dob');
var ticketId = generateTicketId();

var qrcodevalue = `Name: ${name}\nEmail: ${emailid}\nSeat Number: ${seatnum}\nNationality: ${nationality}\nDate of Birth: ${dob}\nTicket ID: ${ticketId}`

// Generate QR code
savevalue(name, emailid, seatnum, nationality, dob);

// Display QR code to user
var qrCodeImg = document.createElement('img');
qrCodeImg.src = `http://localhost:8080/generate_qr_code/${qrcodevalue}`;
document.body.appendChild(qrCodeImg);

document.querySelector('.alert').style.display = "block";

setTimeout(() =>{
  document.querySelector(".alert").style.display = "none";
}, 3000);

document.getElementById("registrationform").reset();
}

const savevalue = (name, emailid, seatnum, nationality, dob) =>{
var userdata = ticketdb.push();

userdata.set({
    name : name,
    emailid : emailid,
    seatnum : seatnum,
    nationality : nationality,
    dob : dob,
});
};

const getElementvalue = (id) =>{
return document.getElementById(id).value;
};
