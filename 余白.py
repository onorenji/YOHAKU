import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.title("🖼️ 画像領域選択ビューア")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    # キャンバスの設定
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.3)",  # 半透明白
        stroke_width=3,
        stroke_color="#ff0000",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="rect",  # 矩形選択モード
        key="canvas",
    )

    if canvas_result.json_data is not None:
        # 最初の矩形だけを処理
        objects = canvas_result.json_data["objects"]
        if objects:
            obj = objects[0]
            left = int(obj["left"])
            top = int(obj["top"])
            width = int(obj["width"])
            height = int(obj["height"])

            cropped = image.crop((left, top, left + width, top + height))
            st.markdown("### 🟩 選択された領域")
            st.image(cropped)