import json
import streamlit as st
from google.cloud import vision
import time

st.set_page_config(
    page_title="AI画像認識アプリ",
    page_icon="🔍",
    layout="wide"
)

@st.cache_resource
def get_vision_client():
    try:
        credentials_dict = json.loads(st.secrets["google_credentials"], strict=False)
        return vision.ImageAnnotatorClient.from_service_account_info(info=credentials_dict)
    except Exception as e:
        st.error("認証エラーが発生しました。管理者に連絡してください。")
        st.stop()

client = get_vision_client()

@st.cache_data
def get_response(content):
    try:
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        return response
    except Exception as e:
        st.error(f"画像解析中にエラーが発生しました: {str(e)}")
        return None

st.markdown("""
# 🔍 AI画像認識アプリ
このアプリでは、Google Cloud Vision APIを使用して画像の内容を自動的に識別します。
""")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📷 画像をアップロード")
    file = st.file_uploader(
        "画像ファイルを選択してください",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        help="対応形式: PNG, JPG, JPEG, GIF, BMP"
    )

    if file is not None:
        st.success(f"✅ ファイルが選択されました: {file.name}")
        st.image(file, caption="アップロードされた画像", use_column_width=True)

        analyze_button = st.button(
            "🔍 画像を解析する",
            type="primary",
            use_container_width=True
        )
    else:
        st.info("👆 上記から画像ファイルを選択してください")
        analyze_button = False

with col2:
    st.markdown("### 📊 解析結果")

    if file is not None and analyze_button:
        with st.spinner("画像を解析中..."):
            content = file.getvalue()
            response = get_response(content)

        if response and response.label_annotations:
            if response.error.message:
                st.error(f"エラーが発生しました: {response.error.message}")
            else:
                st.success("✅ 解析完了!")

                st.markdown("#### 🏷️ 検出されたオブジェクト:")

                labels_data = []
                for label in response.label_annotations[:15]:
                    confidence = label.score * 100
                    confidence_color = "🟢" if confidence >= 90 else "🟡" if confidence >= 70 else "🔴"
                    labels_data.append({
                        "オブジェクト": f"**{label.description}**",
                        "確信度": f"{confidence_color} **{confidence:.1f}%**"
                    })

                st.table(labels_data)

                with st.expander("📊 詳細な確信度グラフ"):
                    for i, label in enumerate(response.label_annotations[:10], 1):
                        confidence = label.score * 100
                        st.write(f"{i}. {label.description}")
                        st.progress(confidence / 100, text=f"{confidence:.1f}%")

                if len(response.label_annotations) > 10:
                    st.info(f"他に{len(response.label_annotations) - 10}個のオブジェクトが検出されました")
        elif response:
            st.warning("画像からオブジェクトを検出できませんでした。別の画像をお試しください。")
        else:
            st.error("画像の解析に失敗しました。")
    elif file is None:
        st.info("画像をアップロードして解析ボタンを押してください")
    else:
        st.info("解析ボタンをクリックして開始してください")

st.markdown("---")
st.markdown("**💡 ヒント:** より良い結果を得るために、明るく鮮明な画像をアップロードしてください。")