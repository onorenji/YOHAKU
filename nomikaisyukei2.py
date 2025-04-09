import streamlit as st

st.title("🍻 飲み会割り勘アプリ")

# 総額入力
total = st.number_input("総額（円）を入力してください", min_value=0, step=100)

# 人数入力
num_people = st.number_input("参加人数を入力してください", min_value=1, step=1)

# 各人の金額入力
st.subheader("各人の支払額（必要があれば修正できます）")
amounts = []

col1, col2 = st.columns([2, 1])
with col1:
    names = [st.text_input(f"名前{i+1}", f"参加者{i+1}") for i in range(num_people)]
with col2:
    default_amount = total // num_people if num_people > 0 else 0
    for i in range(num_people):
        amount = st.number_input(f"金額{i+1}", value=default_amount, key=f"amount{i}")
        amounts.append(amount)

# 残額計算
total_assigned = sum(amounts)
remaining = total - total_assigned

st.markdown("---")
st.subheader("💰 集計結果")
st.write(f"総額: {total} 円")
st.write(f"割り振られた合計: {total_assigned} 円")
st.write(f"残額: {remaining} 円")

if remaining < 0:
    st.error("⚠️ 割り振りすぎています。")
elif remaining > 0:
    st.warning("💡 まだ割り振られていない金額があります。")
else:
    st.success("🎉 ピッタリ割り振られました！")