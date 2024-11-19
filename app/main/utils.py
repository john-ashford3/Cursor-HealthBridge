import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    """Save profile picture with a random name and resize it."""
    # Generate random hex for filename
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    # Resize image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Save picture
    i.save(picture_path)
    
    return picture_fn 