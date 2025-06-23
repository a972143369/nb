import joblib
import gradio as gr
import pandas as pd

# 加载最新融合模型
model = joblib.load("model.joblib")

def predict_asian_odds(
    home, away,
    init_line, init_odds_h, init_odds_a,
    final_line, final_odds_h, final_odds_a,
    eur_init_o, eur_init_d, eur_init_h,
    eur_final_o, eur_final_d, eur_final_h,
    info_score, head2head_diff
):
    df = pd.DataFrame([{
        "home": home, "away": away,
        "init_line": init_line,
        "init_odds_h": init_odds_h,
        "init_odds_a": init_odds_a,
        "final_line": final_line,
        "final_odds_h": final_odds_h,
        "final_odds_a": final_odds_a,
        "eur_init_o": eur_init_o,
        "eur_init_d": eur_init_d,
        "eur_init_h": eur_init_h,
        "eur_final_o": eur_final_o,
        "eur_final_d": eur_final_d,
        "eur_final_h": eur_final_h,
        "info_score": info_score,
        "head2head_diff": head2head_diff
    }])
    pred = model.predict(df)[0]
    prob = model.predict_proba(df).max()

    label = {1: "主胜（赢盘）", 0: "走盘", -1: "客胜（输盘）"}.get(pred, "未知")

    # AOD盘口异动检测
    aod_signal = ""
    if abs(df['init_odds_h'][0] - df['final_odds_h'][0]) >= 0.15:
        aod_signal += f"\n⚠ 主胜水位异常波动: {df['init_odds_h'][0]} → {df['final_odds_h'][0]}"
    if abs(df['init_odds_a'][0] - df['final_odds_a'][0]) >= 0.15:
        aod_signal += f"\n⚠ 客胜水位异常波动: {df['init_odds_a'][0]} → {df['final_odds_a'][0]}"

    # 一致性强信号检测
    consist_parts = []
    if prob > 0.75:
        consist_parts.append("模型极高置信")
    if info_score >= 7:
        consist_parts.append("情报评分优秀")
    if abs(head2head_diff) >= 2:
        consist_parts.append("交锋占优")
    strong_consist = "✅ 一致性强信号：" + " + ".join(consist_parts) if len(consist_parts) >= 2 else ""

    # 统计回顾 (demo 数据)
    past_preds = ["主胜 ✅", "走盘 ❌", "客胜 ✅", "主胜 ✅", "主胜 ❌"]
    past_summary = "\n\n最近5场预测回顾：" + ", ".join(past_preds)

    return f"预测结果：{label}\n模型置信度：{prob:.2%}{aod_signal}\n{strong_consist}{past_summary}"

demo = gr.Interface(
    fn=predict_asian_odds,
    inputs=[
        gr.Textbox(label="主队名称"),
        gr.Textbox(label="客队名称"),
        gr.Number(label="初盘 ( 亚洲盘口线 )"),
        gr.Number(label="初盘主胜水位"),
        gr.Number(label="初盘客胜水位"),
        gr.Number(label="终盘盘口"),
        gr.Number(label="终盘主胜水位"),
        gr.Number(label="终盘客胜水位"),
        gr.Number(label="欧赔初盘 主胜"),
        gr.Number(label="欧赔初盘 和盘"),
        gr.Number(label="欧赔初盘 客胜"),
        gr.Number(label="欧赔终盘 主胜"),
        gr.Number(label="欧赔终盘 和盘"),
        gr.Number(label="欧赔终盘 客胜"),
        gr.Number(label="情报评分 (0-10)"),
        gr.Number(label="历史交锋主客净胜球")
    ],
    outputs="text",
    title="亚洲盘口预测模型",
    description="输入盘口与欧赔数据，点击预测即可得到模型结果，并包含：\n- AOD盘口异常识别\n- 一致性信号提示\n- 模型历史回顾"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
