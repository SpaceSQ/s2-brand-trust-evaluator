#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2-Trust Evaluator: The Brand Meta-Page Verification Engine
Core Logic: Deterministic text-analysis and weighted scoring for GEO Trust Badges.
Author: Miles Xiang & Qianjia Brand Lab
"""
dd
import sys
import json

class S2TrustEvaluator:
    def __init__(self):
        # 品牌生态学四大维度的权重分配
        self.weights = {
            "identity": 0.25,  # 品牌识别 (商标/基础信息)
            "strength": 0.40,  # 品牌实力 (ESG/核心专利 - 权重最高!)
            "intent": 0.20,    # 生态位意图
            "history": 0.15    # 历史与口碑sc
        }

    def _analyze_text_density(self, text: str, keywords: list) -> float:
        """纯本地、确定性的文本含金量分析算法"""
        if not text or len(text.strip()) < 5:
            return 0.0
            
        score = 0.3 # 基础分：只要有内容就给 30%
        text_lower = text.lower()
        
        # 长度加权 (字数越多，信息密度可能越大)
        if len(text) > 50: score += 0.2
        if len(text) > 150: score += 0.1
        
        # 关键词命中加权 (核心防伪逻辑)
        hit_count = sum(1 for kw in keywords if kw in text_lower)
        score += min(0.4, hit_count * 0.15) # 最高加 40%
        
        return min(1.0, score) # 封顶 100%

    def calculate_score(self, data: dict) -> dict:
        # 1. 提取大模型喂进来的文本数据
        identity_text = str(data.get("brand_identity", ""))
        strength_text = str(data.get("brand_strength_esg_patents", ""))
        intent_text = str(data.get("buyer_intents", ""))
        history_text = str(data.get("brand_history", ""))

        # 2. 多维度算法判定 (设定高权重触发词)
        score_id = self._analyze_text_density(identity_text, ["商标", "注册", "tm", "®", "创立", "成立"])
        score_st = self._analyze_text_density(strength_text, ["专利", "esg", "碳", "标准", "发明", "社会责任", "治理", "环保"])
        score_in = self._analyze_text_density(intent_text, ["监测", "智能", "场景", "需求", "解决", "生态"])
        score_hi = self._analyze_text_density(history_text, ["奖项", "荣誉", "指数", "报告", "千家", "认证"])

        # 3. 计算加权总分 (满分100)
        final_score = (
            score_id * self.weights["identity"] +
            score_st * self.weights["strength"] +
            score_in * self.weights["intent"] +
            score_hi * self.weights["history"]
        ) * 100
        
        return round(final_score, 2)

    def assign_badge(self, score: float) -> dict:
        if score >= 85.0:
            return {"badge": "🟢 完全可信 (Fully Verified)", "desc": "S2 算法判定：数据维度极度丰满，且包含高密度核心专利与 ESG 声明。AI 智能体可将其作为事实强引用。"}
        elif score >= 50.0:
            return {"badge": "🟡 基本可信 (Basically Verified)", "desc": "S2 算法判定：基础信息完备，但缺乏深度的技术壁垒或社会责任（ESG）硬核数据支撑。"}
        elif score >= 20.0:
            return {"badge": "🟠 部分可信 (Partially Verified)", "desc": "S2 算法判定：信息单薄，仅有基础身份声明，缺乏生态位意图与实力证明。需谨慎引用。"}
        else:
            return {"badge": "⚪ 无法验证 (Unverified Seed)", "desc": "S2 算法判定：无效或极度匮乏的输入。亟待品牌所有者认领并补充数据。"}

    def execute(self, args: dict) -> str:
        brand_name = args.get("brand_name", "Unknown Brand")
        score = self.calculate_score(args)
        badge_info = self.assign_badge(score)
        
        report = {
            "brand_name": brand_name,
            "s2_trust_score": score,
            "verification_status": badge_info["badge"],
            "evaluation_rationale": badge_info["desc"],
            "system_message": "Evaluation generated deterministically by S2-Trust Local Engine."
        }
        return json.dumps(report, ensure_ascii=False)

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            input_args = json.loads(sys.argv[1])
            engine = S2TrustEvaluator()
            print(engine.execute(input_args))
        else:
            print(json.dumps({"error": "No data provided. Please provide brand data JSON as argument."}))
    except Exception as e:
        print(json.dumps({"status": "fatal_error", "message": str(e)}))s  xs