import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import cv2

st.title("🖼️ 余白率チェッカー")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
threshold = st.slider("余白とみなす明度（0～255）", min_value=0, max_value=255, value=230)

if uploaded_file is not None:
    # 画像を読み込み
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)
    
    # グレースケール変換と輪郭検出のための前処理
    gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    
    # 輪郭検出
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 物体部分を白、余白部分を黒に
    mask = np.ones_like(gray_image) * 255  # 白い画像で初期化
    cv2.drawContours(mask, contours, -1, (0), thickness=cv2.FILLED)  # 物体部分を黒で塗りつぶし

    # 余白部分の計算
    white_space_pixels = np.sum(mask == 255)
    total_pixels = mask.size
    white_space_ratio = (white_space_pixels / total_pixels) * 100

    # 結果表示
    st.image(uploaded_file, caption="アップロードされた画像", use_column_width=True)
    st.markdown(f"### ✨ この画像の余白率は **{white_space_ratio:.2f}%** です")

    # 余白部分のハイライト表示
    if st.checkbox("余白部分をハイライト表示"):
        mask_rgb = np.zeros((*mask.shape, 3), dtype=np.uint8)
        mask_rgb[..., 2] = mask * 255  # 青色でマスク
        overlay = Image.fromarray(mask_rgb).convert("RGBA")

        # 元画像をカラーで再読み込み
        original = Image.open(uploaded_file).convert("RGBA")
        blended = Image.blend(original, overlay, alpha=0.3)

        st.image(blended, caption="青くハイライトされた余白", use_column_width=True)