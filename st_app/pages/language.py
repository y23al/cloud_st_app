# import json
# import requests
# import streamlit as st
# from annotated_text import annotated_text

# class YahooNlpApi:
#     post_id = 0
    
#     def __init__(self, client_id):
#         self.__client_id = client_id
    
#     @classmethod
#     def get_id(cls):
#         post_id = cls.post_id
#         cls.post_id += 1
#         return str(post_id)
    
#     def get_headers(self):
#         headers = {
#             "Content-Type":"application/json",
#             "User-Agent":f"Yahoo AppID: {self.__client_id}"
#         }
#         return headers
    
#     def parameterize(self, post_id=None, jsonrpc="2.0", method="", params={}): 
#         if post_id is None:
#             post_id = self.get_id()
#         else:
#             post_id = str(post_id)
#         req_obj = {
#             "id":post_id,
#             "jsonrpc":jsonrpc,
#             "method":method,
#             "params":params
#         }
#         return json.dumps(req_obj).encode("utf-8")
    
#     def post(self, url, *args, **kwargs):
#         headers = self.get_headers()
#         payload = self.parameterize(*args, **kwargs)
#         resp = requests.post(url, headers=headers, data=payload)
#         return json.loads(resp.content)
    
#     @staticmethod
#     def tokenize(token):
#         var_names = ["表記","読みがな","基本形表記","品詞","品詞細分類","活用型","活用系"]
#         return dict(zip(var_names, token))
    
#     def parse(self, q):
#         url = "https://jlp.yahooapis.jp/MAService/V2/parse"
#         method = "jlp.maservice.parse"
#         params = {"q":q}
#         data = self.post(url=url, method=method, params=params)
#         tokens = data["result"]["tokens"]
#         tokens = list(map(self.tokenize, tokens))
#         return tokens
    
#     def extract(self, q):
#         url = "https://jlp.yahooapis.jp/KeyphraseService/V2/extract"
#         method = "jlp.keyphraseservice.extract"
#         params = {"q":q}
#         data = self.post(url=url, method=method, params=params)
#         tokens = data["result"]["phrases"]
#         return tokens

# api = YahooNlpApi(st.secrets["yahoo_app_id"])

# if "result" not in st.session_state:
#     st.session_state["result"] = None
# if "keyword" not in st.session_state:
#     st.session_state["keyword"] = None

# def reset():
#     st.session_state["result"] = None
#     st.session_state["keyword"] = None

# st.markdown("# 品詞解析")
# st.markdown("## 入力")
# document = st.text_area("分析したい文章を入力してください。")
# mode = st.radio("分析モード", ["形態素解析", "キーワード抽出"], on_change=reset)

# if st.button("分析"):
#     if mode == "形態素解析":
#         st.session_state["result"] = api.parse(document)
#     elif mode == "キーワード抽出":
#         st.session_state["result"] = api.extract(document)

# if st.session_state["result"]:
#     st.markdown("## 分析結果")
#     if mode == "形態素解析":
#         words = list(map(lambda wd: (wd["表記"], wd["品詞"]), st.session_state["result"]))
#         annotated_text(words)
#     elif mode == "キーワード抽出":
#         keywords = list(map(lambda kw: kw["text"], st.session_state["result"]))
#         kw = st.selectbox("キーワード", keywords)
#         words = document.split(kw)
#         for i in range(len(words)-1):
#             words.insert(2*i+1, (kw,))
#         annotated_text(words)

import json
import requests
import streamlit as st
from annotated_text import annotated_text
import io

class YahooNlpApi:
    post_id = 0
    
    def __init__(self, client_id):
        self.__client_id = client_id
    
    @classmethod
    def get_id(cls):
        post_id = cls.post_id
        cls.post_id += 1
        return str(post_id)
    
    def get_headers(self):
        headers = {
            "Content-Type":"application/json",
            "User-Agent":f"Yahoo AppID: {self.__client_id}"
        }
        return headers
    
    def parameterize(self, post_id=None, jsonrpc="2.0", method="", params={}): 
        if post_id is None:
            post_id = self.get_id()
        else:
            post_id = str(post_id)
        req_obj = {
            "id":post_id,
            "jsonrpc":jsonrpc,
            "method":method,
            "params":params
        }
        return json.dumps(req_obj).encode("utf-8")
    
    def post(self, url, *args, **kwargs):
        headers = self.get_headers()
        payload = self.parameterize(*args, **kwargs)
        resp = requests.post(url, headers=headers, data=payload)
        return json.loads(resp.content)
    
    @staticmethod
    def tokenize(token):
        var_names = ["表記","読みがな","基本形表記","品詞","品詞細分類","活用型","活用系"]
        return dict(zip(var_names, token))
    
    def parse(self, q):
        url = "https://jlp.yahooapis.jp/MAService/V2/parse"
        method = "jlp.maservice.parse"
        params = {"q":q}
        data = self.post(url=url, method=method, params=params)
        tokens = data["result"]["tokens"]
        tokens = list(map(self.tokenize, tokens))
        return tokens
    
    def extract(self, q):
        url = "https://jlp.yahooapis.jp/KeyphraseService/V2/extract"
        method = "jlp.keyphraseservice.extract"
        params = {"q":q}
        data = self.post(url=url, method=method, params=params)
        tokens = data["result"]["phrases"]
        return tokens

api = YahooNlpApi(st.secrets["yahoo_app_id"])

if "result" not in st.session_state:
    st.session_state["result"] = None
if "keyword" not in st.session_state:
    st.session_state["keyword"] = None
if "document" not in st.session_state:
    st.session_state["document"] = ""

def reset():
    st.session_state["result"] = None
    st.session_state["keyword"] = None

st.markdown("# 品詞解析")
st.markdown("## 入力")

# サンプル文章を選べるようにする
sample_texts = {
    "--なし--": "",
    "天気のサンプル": "今日はいい天気です。散歩に出かけました。",
    "学習のサンプル": "機械学習の勉強をしています。データ前処理が重要です。",
    "旅行のサンプル": "東京で美味しいラーメンを食べました。"
}
col1, col2 = st.columns([4,1])
with col1:
    document = st.text_area("分析したい文章を入力してください。", key="document", height=140)
with col2:
    sample = st.selectbox("サンプル文章", list(sample_texts.keys()))
    if st.button("挿入"):
        st.session_state["document"] = sample_texts[sample]

mode = st.radio("分析モード", ["形態素解析", "キーワード抽出"], on_change=reset)

# 表示オプション
st.sidebar.markdown("## 表示オプション")
show_table = st.sidebar.checkbox("表形式で表示（形態素解析）", value=True)
show_freq = st.sidebar.checkbox("頻度表示（形態素解析）", value=False)
show_raw = st.sidebar.checkbox("生JSONを表示/ダウンロード", value=False)

# キーワード用オプション
if mode == "キーワード抽出":
    top_n = st.sidebar.slider("上位N件を表示", min_value=1, max_value=20, value=5)

actions = st.columns([1,1,1])
with actions[0]:
    if st.button("分析"):
        if mode == "形態素解析":
            st.session_state["result"] = api.parse(st.session_state["document"])
        elif mode == "キーワード抽出":
            st.session_state["result"] = api.extract(st.session_state["document"])
with actions[1]:
    if st.button("リセット"):
        st.session_state["document"] = ""
        reset()
with actions[2]:
    # 何もしないが将来の拡張用に配置
    pass

def make_download_buttons(data, label_prefix="result"):
    if data is None:
        return
    json_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    st.download_button(f"{label_prefix} をJSONでダウンロード", data=json_bytes, file_name=f"{label_prefix}.json", mime="application/json")
    # CSV 用意できる場合だけ（形態素解析の表形式など）
    if isinstance(data, list) and len(data)>0 and isinstance(data[0], dict):
        # simple CSV
        headers = list(data[0].keys())
        buf = io.StringIO()
        buf.write(",".join(headers) + "\n")
        for row in data:
            row_vals = [str(row.get(h,"")).replace(",", " ") for h in headers]
            buf.write(",".join(row_vals) + "\n")
        st.download_button(f"{label_prefix} をCSVでダウンロード", data=buf.getvalue().encode("utf-8"), file_name=f"{label_prefix}.csv", mime="text/csv")

if st.session_state["result"]:
    st.markdown("## 分析結果")
    if mode == "形態素解析":
        tokens = st.session_state["result"]
        # annotated_text 用短縮表示（表記と品詞）
        words = list(map(lambda wd: (wd["表記"], wd["品詞"]), tokens))
        annotated_text(words)
        if show_table:
            st.markdown("### トークン表")
            st.dataframe(tokens)
        if show_freq:
            # 単語頻度
            freq = {}
            for t in tokens:
                w = t.get("表記","")
                freq[w] = freq.get(w,0) + 1
            freq_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
            st.markdown("### 出現頻度（表記）")
            st.table([{ "単語":k, "頻度":v } for k,v in freq_items])
        if show_raw:
            st.markdown("### 生JSON")
            st.json(st.session_state["result"])
        make_download_buttons(st.session_state["result"], label_prefix="morph_result")
    elif mode == "キーワード抽出":
        keywords = list(map(lambda kw: kw.get("text", str(kw)), st.session_state["result"]))
        # 上位N件が選べるようにする
        display_kw = keywords[:top_n]
        kw = st.selectbox("キーワード", display_kw, index=0)
        st.markdown("### 文中でハイライト")
        # document を選択したキーワードで簡易ハイライト（annotated_text 用）
        parts = st.session_state["document"].split(kw)
        annotated_parts = []
        for i, p in enumerate(parts):
            if p:
                annotated_parts.append(p)
            if i < len(parts)-1:
                annotated_parts.append((kw, "keyword"))
        annotated_text(annotated_parts)
        if show_raw:
            st.markdown("### 生JSON")
            st.json(st.session_state["result"])
        make_download_buttons(st.session_state["result"], label_prefix="keyword_result")