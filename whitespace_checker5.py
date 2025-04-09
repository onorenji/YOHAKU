import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import numpy as np

st.title("🖼️ 余白率チェッカー")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
threshold = st.slider("余白とみなす明度（0～255）", min_value=0, max_value=255, value=230)

if uploaded_file is not None:
    # 画像を読み込み
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)
    
    # グレースケール変換
    gray_image = image.convert("L")
    gray_image_array = np.array(gray_image)

    # 画像のコントラスト強調（余白を強調）
    enhanced_image = gray_image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    enhanced_image_array = np.array(enhanced_image)

    # 余白部分の計算
    white_space_pixels = np.sum(enhanced_image_array >= threshold)
    total_pixels = enhanced_image_array.size
    white_space_ratio = (white_space_pixels / total_pixels) * 100

    # 結果表示
    st.image(uploaded_file, caption="アップロードされた画像", use_column_width=True)
    st.markdown(f"### ✨ この画像の余白率は **{white_space_ratio:.2f}%** です")

    # 余白部分のハイライト表示
    if st.checkbox("余白部分をハイライト表示"):
        mask = enhanced_image_array >= threshold
        mask_rgb = np.zeros((*mask.shape, 3), dtype=np.uint8)
        mask_rgb[..., 2] = mask * 255  # 青色でマスク
        overlay = Image.fromarray(mask_rgb).convert("RGBA")

        # 元画像をカラーで再読み込み
        original = Image.open(uploaded_file).convert("RGBA")
        blended = Image.blend(original, overlay, alpha=0.3)

        st.image(blended, caption="青くハイライトされた余白", use_column_width=True)