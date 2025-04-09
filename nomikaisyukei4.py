import streamlit as st

st.title("🍻 千円単位 × 階級あり 割り勘アプリ")

# 総額入力
total = st.number_input("総額（円）を入力してください", min_value=0, step=1000)

# 人数入力
num_people = st.number_input("参加人数を入力してください", min_value=1, step=1)

# 名前と階級入力
st.subheader("🧑‍🤝‍🧑 参加者の名前と階級（1が一番上）")

names = []
ranks = []
for i in range(num_people):
    cols = st.columns([2, 1])
    name = cols[0].text_input(f"名前{i+1}", f"参加者{i+1}")
    rank = cols[1].number_input(f"階級{i+1}", min_value=1, value=2, key=f"rank{i}")
    names.append(name)
    ranks.append(rank)

# 階級から重みを作成（階級1が一番重い）
max_rank = max(ranks)
weights = [max_rank - r + 1 for r in ranks]
weight_sum = sum(weights)

# 仮の金額（割り当て）を計算し、千円単位に丸める
raw_amounts = [total * w / weight_sum for w in weights]
rounded_amounts = [int(round(a / 1000) * 1000) for a in raw_amounts]

# 差分の調整（上位から順に±差を吸収）
current_sum = sum(rounded_amounts)
diff = total - current_sum

sorted_indexes = sorted(range(num_people), key=lambda i: ranks[i])

i = 0
step = 1000 if diff > 0 else -1000
while diff != 0 and i < num_people:
    idx = sorted_indexes[i]
    if (step > 0) or (rounded_amounts[idx] >= 1000):  # 0円以下回避
        rounded_amounts[idx] += step
        diff -= step
    i = (i + 1) % num_people

# 金額調整後入力欄
st.subheader("💴 自動割り振り（千円単位・手動調整可能）")
final_amounts = []
for i in range(num_people):
    amt = st.number_input(f"{names[i]} さんの支払額", value=rounded_amounts[i], step=1000, key=f"amount_input{i}")
    final_amounts.append(amt)

# 集計表示
total_assigned = sum(final_amounts)
remaining = total - total_assigned

st.markdown("---")
st.subheader("📊 結果")
st.write(f"総額: {total} 円")
st.write(f"割り振られた合計: {total_assigned} 円")
st.write(f"残額: {remaining} 円")

if remaining < 0:
    st.error("⚠️ 割り振りすぎています。")
elif remaining > 0:
    st.warning("💡 まだ割り振られていない金額があります。")
else:
    st.success("🎉 ピッタリ割り振られました！")

# 支払い一覧（階級なし）
st.markdown("---")
st.subheader("📋 支払い一覧")

for i in range(num_people):
    st.write(f"{names[i]}: {final_amounts[i]} 円")

# 一覧の下に総額を表示
st.markdown("**合計: {} 円**".format(sum(final_amounts)))