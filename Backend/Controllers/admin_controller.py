from Models.models import Admin,UsernameChangeRequest
from fastapi import APIRouter, HTTPException
from Connections.connections import session,EMAIL,EMAIL_PASSWORD
import secrets
import requests
import smtplib
from hashing import Harsher
from jose import JWTError, jwt
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


SECRET_KEY = "437125588a32a48932c07911f45df783d34379f0b866440da76960384c688ec97d5b4b6b07153d0a5f4276bb336134adf126613d5151627d09710c799ee98530"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_unique_username(db_session):
    letter_counter = 65 
    counter = 1
    
    while True:
        potential_username = f"{chr(letter_counter)}{counter:03}@Animex.ug"
        
        if not Admin.username_exists(db_session, potential_username):
            return potential_username
        else:
            counter += 1
            if counter > 999:
                counter = 1
                letter_counter += 1
                if letter_counter > 90: 
                    raise Exception("Exhausted all usernames")

async def create_admin(admin):
    db = session
    email = admin["email"]
    admin_username = await create_unique_username(db)
    password = await create_password()
    hashed_password = Harsher.get_hash_password(password)
    admin = Admin(username=admin_username, password=hashed_password, email=email)
    try:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        send_welcome_email(admin,password)
    except Exception as e:
        print(f"Error occurred: {e}")
        db.rollback()
    return {"username": admin_username, "password": password, "email": email}


async def create_user_name():
    counter = 1
    letter_counter = 65  
    while True:
        admin_username = f"{chr(letter_counter)}{counter:03}@Animex.ug"
        counter += 1
        if counter > 999999:  
            counter = 1
            letter_counter += 1
            if letter_counter > 90: 
                letter_counter = 65

        return admin_username

    

async def create_password(length=8):
    password = secrets.token_hex(length)

    return password

def send_welcome_email(user_details,password):
    sender_email = EMAIL
    sender_password = EMAIL_PASSWORD

    reset_token = secrets.token_urlsafe(20)

    # Create the email
    msg = MIMEMultipart('related')
    msg['From'] = sender_email
    msg['To'] = user_details.email
    print(f"I am sending to {user_details.email}")
    msg['Subject'] = "Welcome to Animex UG"

    # Make name flexible for DoctorName and name
    # name = user_details.name if hasattr(user_details, 'name') else user_details.DoctorName

    # Make access number flexible for accessnumber, access_no, Accessnumber, AccessNumber
    access_no = user_details.username

    html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <center><img src="cid:company_logo" alt="Company Logo" style="width: 100px; height: auto; margin-bottom: 20px;"></center>
            <!-- <p>Dear ,<br><br> -->
            Welcome to Animex!<br><br>
            We are thrilled to have you join us in our mission to care for roaming dogs.<br> At Animax, we are dedicated to providing the best support and solutions for the welfare of these animals.<br>
            Please log in to your account using these credentials:<br>
            Username: <strong>{access_no}</strong><br>
            Password: <strong>{password}</strong><br><br>
            We encourage you to change your password after logging in for security reasons.<br>
            If you have any questions or need assistance, our dedicated support team is here to assist you.<br><br>
            Thank you for joining us in making a difference in the lives of roaming dogs. Your participation and support are invaluable to our cause.<br><br>
            Warm regards,<br>
            The Animex Team<br><br>
            Note: This is an automated message. Please do not reply to this email.</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(html_body, 'html'))

    # firebase_url = 'https://firebasestorage.googleapis.com/v0/b/bfamproject-80d95.appspot.com/o/prod%2Fproducts%2F1705940735027_gen_visual.jpeg?alt=media&token=de7a990b-2238-455f-a6d2-1f0ba71f55d2'

    # response = requests.get(firebase_url)
    # if response.status_code == 200:
    #     img_data = response.content
    #     img = MIMEImage(img_data)
    #     img.add_header('Content-ID', '<company_logo>')
    #     msg.attach(img)
    # else:
    #     print("Failed to retrieve image from Firebase")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender_email, sender_password)
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: The username or password you entered is not correct.")
        return

    server.send_message(msg)
    server.quit()

async def login(credentials):
    db = session
    username = credentials["username"]
    input_password = credentials["password"]
    admin = db.query(Admin).filter(Admin.username == username).first()

    if admin and Harsher.verify_password(input_password, admin.password):
        token_data = {"sub": username}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # admin_data = Admin.get_admin(db)
        access_token = create_access_token(
            data=token_data, 
            expires_delta=access_token_expires
        )
        admin_data = {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email
        }
        return {"data": admin_data,"access_token": access_token, "token_type": "bearer"}
    else:
        raise Exception("Invalid Username or Password")


# async def change_password(credentials):
#     db = session
#     user = Admin.get_userdata_by_username(db, credentials)

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     reset_token = create_access_token(data={"sub": credentials}, expires_delta=timedelta(hours=1))
#     reset_link = f"https://frontend.com/reset_password?token={reset_token}"
#     send_reset_email(user.email, reset_link)

#     return {"status": True, "message": "Reset link sent to your email address"}

def send_password_reset(username):
    db = session
    user = db.query(Admin).filter(Admin.username == username).first()

    if not user:
        raise Exception("User not found")

    reset_token = create_access_token(data={"sub": username}, expires_delta=timedelta(hours=1))
    reset_link = f"https://yourfrontend.com/reset_password?token={reset_token}"
    send_reset_email(user.email, reset_link)
    return True


def send_reset_email(email: str, reset_link: str):
    sender_email = EMAIL
    sender_password = EMAIL_PASSWORD
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Animex Password Reset"

    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <!-- <center><img src="cid:company_logo" alt="Company Logo" style="width: 100px; height: auto; margin-bottom: 20px;"></center> -->
            <!-- <p>Dear ,<br><br> -->
            Password Reset <br><br>
             Please click on the link to reset your password:
            {reset_link}<br><br>
            The Animex Team<br><br>
            Note: This is an automated message. Please do not reply to this email.</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

def reset_user_password(token, new_password):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise Exception("Invalid token")
    except JWTError:
        raise Exception("Invalid token")

    db = session
    user = db.query(Admin).filter(Admin.username == username).first()
    if not user:
        raise Exception("User not found")

    user.update_password(new_password)
    try:
        db.commit()
        print("Password updated and committed")  
    except Exception as e:
        print(f"Error in commit: {e}")
        db.rollback()
        raise

    return True

def change_username(request):
    db = session
    admin = db.query(Admin).filter(Admin.username == request.current_username).first()

    if not admin:
        raise Exception("Admin not found")
    
    new_username = f"{request.new_username_prefix}@Animex.ug"

    if Admin.username_exists(db, new_username):
        raise Exception("This username is already taken")
    
    admin.username = new_username

    try:
        db.commit()
        return {"message":"Username updated successfully"}
    except Exception as e:
        print(f"Error in commit: {e}")
        db.rollback()
        raise