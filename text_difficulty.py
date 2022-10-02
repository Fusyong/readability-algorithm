# %%
import re
from collections import Counter
from tokenize import Number

import numpy as np
import pandas as pd

char_table = pd.read_csv("character_graded_d1-2022-03-26.csv", encoding="utf8",  index_col=0)
char_table = char_table[["frXle","fre_pct","grade"]]
# char_table[char_table.isnull().values == True]
char_table["grade"].fillna(0, inplace=True)
char_table["grade"] = char_table["grade"].astype(int)

# %%[markdown]
## 单字难度

# * 假设记忆一个字分成3个环节
#     * 记忆字音（音意整体）
#     * 记忆字形
#     * 音形联系
# * 每个环节需要主动重复r（3、4、5、6、7）次
# * 每个环节都会引动其他未完成的环节，难度累积
# * 最容易的字（记住音意整体）与最难的字（三个环节都未完成）的难度区间为$r^2 * 2$ 至 $r^3 * 3$：

# %%
def difficulty_range(r):
    '''难度范围'''
    begin = pow(r, 2) * 2
    end = pow(r, 3) * 3
    return begin, end 
# %%[markdown]
# 实测：
# ```python
# for r in range(3, 7):
#     begin, end = difficulty_range(r)
#     print(f'重复次数 {r}, 最低难度 {begin}, 最高难度 {end}, 难度倍数 {end / begin}')
# ```
# 结果：
# * 重复次数 3, 最低难度 18, 最高难度 81, 难度倍数 4.5
# * 重复次数 4, 最低难度 32, 最高难度 192, 难度倍数 6.0
# * 重复次数 5, 最低难度 50, 最高难度 375, 难度倍数 7.5
# * 重复次数 6, 最低难度 72, 最高难度 648, 难度倍数 9.0

# %%
# 单字难度（难度分摊：把字表按频率顺序等距分散到以上区间，算出每个字的难度系数）
repeat = 5 # 预设重复学习次数
char_num = 2150 # 有效字表长度，保证至少10字次
def char_difficulty(index, repeat=repeat, char_num=char_num):
    '''单字难度'''
    begin, end = difficulty_range(repeat)
    step = (end - begin) / char_num
    d = None
    if index <= char_num -1:
        d = begin + index * step
    else:
        # 超char_num号字按char_num号字计算
        d =  begin + char_num * step
    return d

char_table['rowIndex'] = np.arange(len(char_table))
char_table["diffic"] = char_table.apply(lambda x: char_difficulty(x["rowIndex"]), axis=1)


# %% [markdown]
## 文本难度

# * 前扰系数$f_b=0.2$
# * 后扰系数$f_a=0.1$
# * 句中单字难度：$D_c = {前字难度} \times f_b + {本字难度} + {后字难度} \times f_a$
# * 单句难度：$\sum {句中单字难度}$
# * 文中分句难度（在有标点分割的复句中）：${前句难度} \times f_b + {分句难度} + {后句难度} \times f_a$；
# * 文本难度（即分句平均难度）：$\overline{d_t}=\frac{\sum {分句难度}}{句数}$
# * 文章学习任务量：$d_t=\sum {分句难度}$

# %%
c_ignore = r"[啊呀哇哪哦咦吧啦呢呼噜嘘咯嘛呵哈呃哎哟呦噢]" # 忽略惊叹、强调类语气词
def difficulty_char_alone(char):
    # 忽略字按0号字计算
    if char in c_ignore:
        d =char_table.iloc[0]["diffic"]
    elif char in char_table.index.values:
        d =  char_table.loc[char,"diffic"]
    else:
        # 表外字按3500字表中最后一字计算
        d = char_table.iloc[char_num]["diffic"]
    return d

def difficulty_char_in_context(text, char_idex, actual_repeat):
    c = difficulty_char_alone(text[char_idex])
    base = char_table.iloc[0]["diffic"] # 字表第一个字的难度
    c = c - (c - base) / (1*repeat) * (actual_repeat - 1) # 难度依次递减，1*repeat次后与字表第一个字相同
    if c == 0:
        return 0
    else:
        factor_before = 0.07 # 前字干扰系数
        factor_after = factor_before * 2 # 后字干扰系数
        b = difficulty_char_alone(text[char_idex-1]) if char_idex>1 else 0
        a = difficulty_char_alone(text[char_idex+1]) if char_idex<(len(text)-1) else 0
        out = factor_before * b / c + c +  factor_after * a / c
        return out

# %%
chinese_p = re.compile("[\u4E00-\u9FA5]")
def is_chinese(text):
    return True if chinese_p.fullmatch(text) else False

# %%
def difficulty_text(text):
    """统计文本难度

    Args:
        text (str): 文本

    Returns:
        c_num: 字数
        c_cat_num: 字种
        difficulty_sum: 总难度
        difficulty_per_sentence: 句子难度
        difficulty_per_sub_sentence: 分句难度
        difficulty_per_char: 单字难度
    """    
    p_end = r"[。？！…\n]"
    p_middle = r"[，、；：—]"
    # p_ignore = r"[“”（）《》]"

    sentence_num = 0
    sub_sentence_num = 0
    c_list = []
    difficulty_sum = 0
    last_state = "end" # 上一个字符的性质

    for i, c in enumerate(text):
        if is_chinese(c):
            last_state = "c"
            c_list.append(c)
            actual_repeat = Counter(c_list)[c]
            # print(c, actual_repeat, difficulty_char_in_context(text,i,actual_repeat))
            difficulty_sum += difficulty_char_in_context(text,i,actual_repeat)
        elif c in p_end:
            if last_state != "end":
                sentence_num += 1
                sub_sentence_num += 1
            last_state = "end"
        elif c in p_middle:
            if last_state != "middle":
                sub_sentence_num += 1
            last_state = "middle"
        # print(i, c, sentence_num, sub_sentence_num, c_num)

    c_num = len(c_list)
    c_cat_num = len(set(c_list))
    difficulty_per_sentence = difficulty_sum / sentence_num if sentence_num != 0 else 0
    difficulty_per_sub_sentence = difficulty_sum / sub_sentence_num if sub_sentence_num != 0 else 0
    difficulty_per_char = difficulty_sum / c_num if c_num != 0 else 0

    return c_num, c_cat_num,  difficulty_sum, difficulty_per_sentence, difficulty_per_sub_sentence, difficulty_per_char

# %% 
if __name__ == "__main__":


    text1 = """
解落三秋叶，
能开二月花。
过江千尺浪，
入竹万竿斜。
    """

    text2 = """
灞原风雨定，
晚见雁行频。
落叶他乡树，
寒灯独夜人。
    """

    print(difficulty_text(text1))
    print(difficulty_text(text2))

    # 结果（字数，字种，文难度，句难度，分句难度，字难度）：
    # (20, 20, 2273.8219594390007, 1136.9109797195003, 568.4554898597502, 113.69109797195003)
    # (20, 20, 2290.0942398107927, 1145.0471199053964, 572.5235599526982, 114.50471199053963)

# %%
