import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import cv2

st.title("🖼️ 余白率チェッカー")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
threshold = st.slider("余白とみなす明度（0～255）", min_value=0, max_value=255, value=230)

if uploaded_file is not None:
    # 画像を読み込み
    image = Image.open(uploaded_file).convert("L")  # グレースケールに変換
    image_array = np.array(image)
    
    # ガウシアンブラーでノイズ除去
    blurred_image = cv2.GaussianBlur(image_array, (5, 5), 0)
    
    # Cannyエッジ検出
    edges = cv2.Canny(blurred_image, threshold1=100, threshold2=200)
    
    # 余白部分のピクセル数を計算
    white_space_pixels = np.sum(edges == 0)  # エッジがない部分が余白と判断
    total_pixels = image_array.size
    white_space_ratio = (white_space_pixels / total_pixels) * 100

    # 結果表示
    st.image(uploaded_file, caption="アップロードされた画像", use_column_width=True)
    st.markdown(f"### ✨ この画像の余白率は **{white_space_ratio:.2f}%** です")

    # 余白部分のハイライト表示
    if st.checkbox("余白部分をハイライト表示"):
        mask = edges == 0  # エッジがない部分
        mask_rgb = np.zeros((*mask.shape, 3), dtype=np.uint8)
        mask_rgb[..., 2] = mask * 255  # 青色でマスク
        overlay = Image.fromarray(mask_rgb).convert("RGBA")

        # 元画像をカラーで再読み込み
        original = Image.open(uploaded_file).convert("RGBA")
        blended = Image.blend(original, overlay, alpha=0.3)

        st.image(blended, caption="青くハイライトされた余白", use_column_width=True)