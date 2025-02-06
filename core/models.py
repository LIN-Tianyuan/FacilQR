from PIL import Image, ImageOps, ImageDraw, ImageFont
from core.utils import font_path

# ---------------------------------------- Model 01 (sans logo) ----------------------------------------
def first_model_qrcode(bordered, radius, poweredBy, qrcode_image):
    plan = Image.new(mode="RGB", size=(400, 468), color=(255, 255, 255))
    poweredBy = poweredBy.resize((292, 48))
    poweredBy_position = ((plan.width - poweredBy.width) // 2, plan.height - poweredBy.height - 20)
    plan.paste(poweredBy, poweredBy_position, poweredBy)

    qrcode_image = qrcode_image.resize((360, 360))
    qrcode_image_position = ((plan.width - qrcode_image.width) // 2, 20)
    plan.paste(qrcode_image, qrcode_image_position)

    if bordered:
        draw = ImageDraw.Draw(plan)
        border_width = 5
        draw.rectangle([border_width // 2, border_width // 2, plan.width - border_width // 2, plan.height - border_width // 2], outline=(0, 0, 0), width=border_width)

    if radius:
        mask = Image.new("L", plan.size, 0)
        corner_radius = 16
        rounded_rectangle = ImageDraw.Draw(mask)
        rounded_rectangle.rounded_rectangle(
            [0, 0, plan.width, plan.height],
            radius=corner_radius, fill=255
        )
        plan.putalpha(mask)

    return plan

# ---------------------------------------- Model 02 (avec logo) ----------------------------------------
def second_model_qrcode(bordered, radius, expand, poweredBy, qrcode_image, logo):
    plan = Image.new(mode="RGB", size=(400, 600), color=(255, 255, 255))
    poweredBy = poweredBy.resize((292, 48))
    poweredBy_position = ((plan.width - poweredBy.width) // 2, plan.height - poweredBy.height - 20)
    plan.paste(poweredBy, poweredBy_position, poweredBy)

    qrcode_image = qrcode_image.resize((360, 360))
    qrcode_image_position = ((plan.width - qrcode_image.width) // 2, poweredBy_position[1] - qrcode_image.height - 20)
    plan.paste(qrcode_image, qrcode_image_position)

    logo_frame_size = (292, 112)
    logo_frame = Image.new(mode="RGB", size=logo_frame_size, color=(255, 255, 255))
    logo = ImageOps.expand(logo, logo_frame_size) if expand else ImageOps.contain(logo, logo_frame_size)
    logo_position_in_frame = ((logo_frame.width - logo.width) // 2, (logo_frame.height - logo.height) // 2)
    logo_frame.paste(logo, logo_position_in_frame, logo)

    logo_position = ((plan.width - logo_frame.width) // 2, qrcode_image_position[1] - logo_frame.height - 20)
    plan.paste(logo_frame, logo_position)

    if bordered:
        draw = ImageDraw.Draw(plan)
        border_width = 5
        draw.rectangle([border_width // 2, border_width // 2, plan.width - border_width // 2, plan.height - border_width // 2], outline=(0, 0, 0), width=border_width)

    if radius:
        mask = Image.new("L", plan.size, 0)
        corner_radius = 16
        rounded_rectangle = ImageDraw.Draw(mask)
        rounded_rectangle.rounded_rectangle(
            [0, 0, plan.width, plan.height],
            radius=corner_radius, fill=255
        )
        plan.putalpha(mask)

    return plan

# ---------------------------------------- Model 03 (avec logo) ----------------------------------------
def third_model_qrcode(bordered, radius, withID, beginID, poweredBy, qrcode_image, logo):
    plan = Image.new(mode="RGB", size=(600, 400), color=(255, 255, 255))

    poweredBy = poweredBy.resize((292, 48))
    poweredBy_position = (20, plan.height - poweredBy.height - 20)
    plan.paste(poweredBy, poweredBy_position, poweredBy)

    qrcode_image = qrcode_image.resize((292, 292))
    qrcode_image_position = (20, poweredBy_position[1] - qrcode_image.height - 20)
    plan.paste(qrcode_image, qrcode_image_position)

    if withID:
        if beginID is None:
            raise ValueError("beginID must be provided when withID is True")

        logo_frame_size = (248, 292)
        logo_frame = Image.new(mode="RGB", size=logo_frame_size, color=(255, 255, 255))
        logo_with_padding = ImageOps.contain(logo, logo_frame_size)
        logo_position_in_frame = ((logo_frame.width - logo_with_padding.width) // 2, (logo_frame.height - logo_with_padding.height) // 2)
        logo_frame.paste(logo_with_padding, logo_position_in_frame, logo_with_padding)

        logo_position = (plan.width - logo_frame.width - 20, 20)
        plan.paste(logo_frame, logo_position)

        font = ImageFont.truetype(str(font_path), 42)
        text = f" {str(beginID)} "

        withID_frame = Image.new(mode="RGB", size=(248, 48), color=(255, 255, 255))
        draw_text_frame = ImageDraw.Draw(withID_frame)

        text_bbox = draw_text_frame.textbbox((0, 0), text, font=font)

        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = withID_frame.width - text_width # aligner à droite
        text_y = (withID_frame.height - text_height) // 2 - 14 # centrage vertical

        draw_text_frame.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

        withID_position = (plan.width - withID_frame.width - 20, logo_position[1] + logo_frame.height + 20)
        plan.paste(withID_frame, withID_position)

    else:
        logo_frame_size = (248, 360)
        logo_frame = Image.new(mode="RGB", size=logo_frame_size, color=(255, 255, 255))
        logo_with_padding = ImageOps.contain(logo, logo_frame_size)
        logo_position_in_frame = ((logo_frame.width - logo_with_padding.width) // 2, (logo_frame.height - logo_with_padding.height) // 2)
        logo_frame.paste(logo_with_padding, logo_position_in_frame, logo_with_padding)

        logo_position = (plan.width - logo_frame.width - 20, plan.height - logo_frame.height - 20)
        plan.paste(logo_frame, logo_position)

    if bordered:
        draw = ImageDraw.Draw(plan)
        border_width = 5
        draw.rectangle([border_width // 2, border_width // 2, plan.width - border_width // 2, plan.height - border_width // 2], outline=(0, 0, 0), width=border_width)

    if radius:
        mask = Image.new("L", plan.size, 0)
        corner_radius = 16
        rounded_rectangle = ImageDraw.Draw(mask)
        rounded_rectangle.rounded_rectangle(
            [0, 0, plan.width, plan.height],
            radius=corner_radius, fill=255
        )
        plan.putalpha(mask)

    return plan


# ---------------------------------------- Model 04 (avec logo moitié) ----------------------------------------
def fourth_model_qrcode(bordered, radius, withID, beginID, poweredBy, qrcode_image, logo):
    plan = Image.new(mode="RGB", size=(300, 200), color=(255, 255, 255))

    poweredBy = poweredBy.resize((292 // 2, 48 // 2))
    poweredBy_position = (10, plan.height - poweredBy.height - 10)
    plan.paste(poweredBy, poweredBy_position, poweredBy)

    qrcode_image = qrcode_image.resize((292 // 2, 292 // 2))
    qrcode_image_position = (10, poweredBy_position[1] - qrcode_image.height - 10)
    plan.paste(qrcode_image, qrcode_image_position)

    if withID:
        if beginID is None:
            raise ValueError("beginID must be provided when withID is True")

        logo_frame_size = (248 // 2, 292 // 2)
        logo_frame = Image.new(mode="RGB", size=logo_frame_size, color=(255, 255, 255))
        logo_with_padding = ImageOps.contain(logo, logo_frame_size)
        logo_position_in_frame = ((logo_frame.width - logo_with_padding.width) // 2, (logo_frame.height - logo_with_padding.height) // 2)
        logo_frame.paste(logo_with_padding, logo_position_in_frame, logo_with_padding)

        logo_position = (plan.width - logo_frame.width - 10, 10)
        plan.paste(logo_frame, logo_position)

        font = ImageFont.truetype(str(font_path), 25)
        text = f" {str(beginID)} "

        withID_frame = Image.new(mode="RGB", size=(248 // 3, 48 // 3), color=(255, 255, 255))
        draw_text_frame = ImageDraw.Draw(withID_frame)

        text_bbox = draw_text_frame.textbbox((0, 0), text, font=font)

        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = withID_frame.width - text_width # aligner à droite
        text_y = (withID_frame.height - text_height) // 2 - 14 # centrage vertical

        draw_text_frame.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

        withID_position = (plan.width - withID_frame.width - 10, logo_position[1] + logo_frame.height)
        plan.paste(withID_frame, withID_position)

    else:
        logo_frame_size = (248, 360)
        logo_frame = Image.new(mode="RGB", size=logo_frame_size, color=(255, 255, 255))
        logo_with_padding = ImageOps.contain(logo, logo_frame_size)
        logo_position_in_frame = ((logo_frame.width - logo_with_padding.width) // 2, (logo_frame.height - logo_with_padding.height) // 2)
        logo_frame.paste(logo_with_padding, logo_position_in_frame, logo_with_padding)

        logo_position = (plan.width - logo_frame.width - 20, plan.height - logo_frame.height - 20)
        plan.paste(logo_frame, logo_position)

    if bordered:
        draw = ImageDraw.Draw(plan)
        border_width = 5
        draw.rectangle([border_width // 2, border_width // 2, plan.width - border_width // 2, plan.height - border_width // 2], outline=(0, 0, 0), width=border_width)

    if radius:
        mask = Image.new("L", plan.size, 0)
        corner_radius = 16
        rounded_rectangle = ImageDraw.Draw(mask)
        rounded_rectangle.rounded_rectangle(
            [0, 0, plan.width, plan.height],
            radius=corner_radius, fill=255
        )
        plan.putalpha(mask)

    return plan