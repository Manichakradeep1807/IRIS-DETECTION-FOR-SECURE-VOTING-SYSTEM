
import os
import json
import datetime
from PIL import Image, ImageDraw, ImageFont

def generate_pdf_receipt(person_id, username, party_name, party_symbol, timestamp, confidence_score, election="General"):
    """
    Generate a beautiful, professional PDF receipt using Pillow and converting to PDF.
    
    Args:
        person_id (int/str): The ID of the voter (from biometric scan)
        username (str): The logged in username
        party_name (str): Name of the party voted for
        party_symbol (str): Symbol of the party
        timestamp (str): Time of vote
        confidence_score (float): Biometric confidence score (0.0-1.0 or 0-100)
        election (str): Election name
        
    Returns:
        str: Path to the generated PDF file
    """
    
    # 1. Create a high-res white image (A4-ish ratio)
    width = 1240
    height = 1754 # A4 at ~150 DPI
    bg_color = (255, 255, 255) # White
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Premium Colors
    navy_blue = (15, 23, 42)    # Slate 900
    sky_blue = (56, 189, 248)   # Sky 400
    gold = (245, 158, 11)       # Amber 500
    light_gray = (241, 245, 249) # Slate 100
    text_dark = (30, 41, 59)    # Slate 800
    
    # Fonts
    try:
        # Try to use standard Windows fonts or fallbacks
        title_font = ImageFont.truetype("seguiemj.ttf", 60) # Segoe UI Emoji for symbols if possible, or standard
    except:
        try: title_font = ImageFont.truetype("arialbd.ttf", 60)
        except: title_font = ImageFont.load_default()
        
    try: header_font = ImageFont.truetype("arialbd.ttf", 45)
    except: header_font = ImageFont.load_default()
    
    try: label_font = ImageFont.truetype("arial.ttf", 30)
    except: label_font = ImageFont.load_default()
    
    try: value_font = ImageFont.truetype("arialbd.ttf", 30)
    except: value_font = ImageFont.load_default()
    
    try: footer_font = ImageFont.truetype("ariali.ttf", 22)
    except: footer_font = ImageFont.load_default()

    # 2. Design Elements
    
    # Header Background
    draw.rectangle([(0, 0), (width, 220)], fill=navy_blue)
    
    # Accent Line
    draw.rectangle([(0, 220), (width, 230)], fill=sky_blue)
    
    # Title
    draw.text((80, 60), "OFFICIAL", font=header_font, fill=sky_blue)
    draw.text((80, 120), "VOTING RECEIPT", font=title_font, fill=(255, 255, 255))
    
    # Logo / Icon (Mockup)
    # Draw a simple shield or check circle
    icon_x, icon_y = width - 180, 110
    r = 70
    draw.ellipse([(icon_x-r, icon_y-r), (icon_x+r, icon_y+r)], outline=gold, width=5)
    draw.text((icon_x-25, icon_y-35), "✔", font=title_font, fill=gold)
    
    # 3. Watermark
    cx, cy = width//2, height//2 + 100
    wr = 350
    draw.ellipse([(cx-wr, cy-wr), (cx+wr, cy+wr)], outline=light_gray, width=20)
    
    # 4. Details Container
    box_x, box_y = 100, 350
    box_w = width - 200
    box_h = 1000
    
    # Background for details
    draw.rectangle([(box_x, box_y), (box_x+box_w, box_y+box_h)], fill=light_gray)
    draw.rectangle([(box_x, box_y), (box_x+box_w, box_y+box_h)], outline=navy_blue, width=2)
    
    # Fields
    fields = [
        ("Voter Name", username),
        ("Voter ID", f"PID-{person_id}"),
        ("Date & Time", timestamp),
        ("Election", election),
        ("Transaction Hash", f"TX-{hash(timestamp + str(person_id)) % 10000000:08x}".upper())
    ]
    
    curr_y = box_y + 60
    for i, (label, val) in enumerate(fields):
        # Row bg for alternates if we wanted, but let's keep clean
        draw.text((box_x + 60, curr_y), label.upper(), font=label_font, fill=text_dark)
        draw.text((box_x + 400, curr_y), str(val), font=value_font, fill=navy_blue)
        
        # Line
        line_y = curr_y + 60
        if i < len(fields) - 1:
            draw.line([(box_x + 40, line_y), (box_x + box_w - 40, line_y)], fill=(200, 200, 200), width=1)
        
        curr_y += 100
        
    # 5. VOTE HIGHLIGHT (The "Party Voted" Section)
    vote_y = curr_y + 50
    draw.rectangle([(box_x, vote_y), (box_x+box_w, vote_y + 250)], fill=navy_blue)
    
    draw.text((width//2 - 120, vote_y + 30), "VOTE CAST FOR", font=header_font, fill=sky_blue)
    
    party_full = f"{party_symbol} {party_name}"
    bbox = draw.textbbox((0, 0), party_full, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw)//2, vote_y + 110), party_full, font=title_font, fill=gold)
    
    # 6. Verification & Footer
    footer_y = height - 150
    
    # QR Code placeholder (Box)
    qr_size = 150
    qr_x = 100
    qr_y = footer_y - 20
    draw.rectangle([(qr_x, qr_y), (qr_x+qr_size, qr_y+qr_size)], outline=text_dark, width=2)
    draw.text((qr_x + 40, qr_y + 60), "QR", font=title_font, fill=text_dark)
    
    disclaimer = [
        "This receipt is an official record of your encrypted vote.",
        f"Biometric Authentication Confidence: {confidence_score*100:.2f}%",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    ]
    
    txt_x = 300
    txt_y = qr_y + 20
    for line in disclaimer:
        draw.text((txt_x, txt_y), line, font=footer_font, fill=text_dark)
        txt_y += 35
        
    # Blue bottom bar
    draw.rectangle([(0, height-40), (width, height)], fill=navy_blue)

    # 7. Save
    receipt_dir = "receipts"
    if not os.path.exists(receipt_dir):
        os.makedirs(receipt_dir)
        
    filename = f"vote_receipt_{person_id}_{int(datetime.datetime.now().timestamp())}.pdf"
    filepath = os.path.join(receipt_dir, filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
    img.save(filepath, "PDF", resolution=150.0)
    return filepath

def generate_jpeg_receipt(person_id, username, party_name, party_symbol, timestamp, confidence_score, election="General"):
    """
    Generate a high-quality JPEG receipt.
    Same logic as PDF but saves as image.
    """
    
    width = 1240
    height = 1754 
    bg_color = (255, 255, 255)
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    navy_blue = (15, 23, 42); sky_blue = (56, 189, 248); gold = (245, 158, 11)
    light_gray = (241, 245, 249); text_dark = (30, 41, 59)
    
    try: title_font = ImageFont.truetype("seguiemj.ttf", 60)
    except: 
        try: title_font = ImageFont.truetype("arialbd.ttf", 60)
        except: title_font = ImageFont.load_default()
    try: header_font = ImageFont.truetype("arialbd.ttf", 45)
    except: header_font = ImageFont.load_default()
    try: label_font = ImageFont.truetype("arial.ttf", 30)
    except: label_font = ImageFont.load_default()
    try: value_font = ImageFont.truetype("arialbd.ttf", 30)
    except: value_font = ImageFont.load_default()
    try: footer_font = ImageFont.truetype("ariali.ttf", 22)
    except: footer_font = ImageFont.load_default()

    # Header
    draw.rectangle([(0, 0), (width, 220)], fill=navy_blue)
    draw.rectangle([(0, 220), (width, 230)], fill=sky_blue)
    draw.text((80, 60), "OFFICIAL", font=header_font, fill=sky_blue)
    draw.text((80, 120), "VOTING RECEIPT", font=title_font, fill=(255, 255, 255))
    
    # Icon
    icon_x, icon_y = width - 180, 110; r = 70
    draw.ellipse([(icon_x-r, icon_y-r), (icon_x+r, icon_y+r)], outline=gold, width=5)
    draw.text((icon_x-25, icon_y-35), "✔", font=title_font, fill=gold)
    
    # Watermark
    cx, cy = width//2, height//2 + 100; wr = 350
    draw.ellipse([(cx-wr, cy-wr), (cx+wr, cy+wr)], outline=light_gray, width=20)
    
    # Details
    box_x, box_y = 100, 350; box_w = width - 200; box_h = 1000
    draw.rectangle([(box_x, box_y), (box_x+box_w, box_y+box_h)], fill=light_gray)
    draw.rectangle([(box_x, box_y), (box_x+box_w, box_y+box_h)], outline=navy_blue, width=2)
    
    fields = [("Voter Name", username), ("Voter ID", f"PID-{person_id}"),
              ("Date & Time", timestamp), ("Election", election),
              ("Transaction Hash", f"TX-{hash(timestamp + str(person_id)) % 10000000:08x}".upper())]
    
    curr_y = box_y + 60
    for i, (label, val) in enumerate(fields):
        draw.text((box_x + 60, curr_y), label.upper(), font=label_font, fill=text_dark)
        draw.text((box_x + 400, curr_y), str(val), font=value_font, fill=navy_blue)
        line_y = curr_y + 60
        if i < len(fields) - 1: draw.line([(box_x + 40, line_y), (box_x + box_w - 40, line_y)], fill=(200, 200, 200), width=1)
        curr_y += 100
        
    vote_y = curr_y + 50
    draw.rectangle([(box_x, vote_y), (box_x+box_w, vote_y + 250)], fill=navy_blue)
    draw.text((width//2 - 120, vote_y + 30), "VOTE CAST FOR", font=header_font, fill=sky_blue)
    party_full = f"{party_symbol} {party_name}"
    bbox = draw.textbbox((0, 0), party_full, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw)//2, vote_y + 110), party_full, font=title_font, fill=gold)
    
    # Footer
    footer_y = height - 150
    qr_size = 150; qr_x = 100; qr_y = footer_y - 20
    draw.rectangle([(qr_x, qr_y), (qr_x+qr_size, qr_y+qr_size)], outline=text_dark, width=2)
    draw.text((qr_x + 40, qr_y + 60), "QR", font=title_font, fill=text_dark)
    
    disclaimer = ["This receipt is an official record of your encrypted vote.",
                  f"Biometric Authentication Confidence: {confidence_score*100:.2f}%",
                  f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"]
    txt_x = 300; txt_y = qr_y + 20
    for line in disclaimer:
        draw.text((txt_x, txt_y), line, font=footer_font, fill=text_dark)
        txt_y += 35
        
    draw.rectangle([(0, height-40), (width, height)], fill=navy_blue)
    
    # Save as JPEG in receipts folder
    receipt_dir = "receipts"
    if not os.path.exists(receipt_dir):
        os.makedirs(receipt_dir)

    filename = f"vote_receipt_{person_id}_{int(datetime.datetime.now().timestamp())}.jpg"
    filepath = os.path.join(receipt_dir, filename)
    
    if os.path.exists(filepath): os.remove(filepath)
    img.save(filepath, "JPEG", quality=95)
    return filepath

if __name__ == "__main__":
    # Test
    print(generate_pdf_receipt("101", "Test User", "Democratic Party", "🔵", "2026-02-15 10:30:00", 0.985))
