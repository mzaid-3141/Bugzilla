from auth import verify_password, create_access_token
import models

def login_user(db, email, password):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not verify_password(password, user.password):
        return None

    token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    return {"access_token": token, "token_type": "bearer"}