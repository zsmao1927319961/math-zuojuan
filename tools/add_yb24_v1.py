# -*- coding: utf-8 -*-
# 2026-10-15: 录入 24余炳森五套卷·卷一 错题 7 题（选4/6/8/9 + 填12/14/16）
# 答案与解析对官方源：森哥五套卷数二.pdf 模拟一答案解析 p9-p13（已视觉核对）
import json, io, sys

P = 'data/mock_errors.json'
d = json.load(io.open(P, encoding='utf-8'))

E = []

E.append({
 'no': 4, 'type': '选择', 'subject': '高数', 'chapter': '一元函数积分学',
 'kp': '对称区间积分与奇偶性、原函数奇偶性判断',
 'q': '设非常值函数 $f(x)$ 在 $[-1,1]$ 上连续，若对 $[-1,1]$ 上的任意偶函数 $g(x)$，积分 $\\int_{-1}^{1} f(x)g(x)\\,\\mathrm{d}x=0$，则下列不正确的是（　）。\nA. $\\int_{-1}^{1}[f(x)+f(-x)]g(x)\\,\\mathrm{d}x=0$\nB. $\\int_{-1}^{1}[f(x)-f(-x)]g(x)\\,\\mathrm{d}x=0$\nC. $f(x)$ 为奇函数\nD. $f(x)$ 未必一定是奇函数',
 'ans': 'D',
 'sol': '由 $g(-x)=g(x)$，作 $x\\to -x$ 代换得 $\\int_{-1}^{1}f(-x)g(x)\\,\\mathrm{d}x=\\int_{-1}^{1}f(u)g(-u)\\,\\mathrm{d}u=\\int_{-1}^{1}f(x)g(x)\\,\\mathrm{d}x=0$，故 A、B 均正确。又 $f(x)+f(-x)$ 是偶函数，在 A 中取 $g(x)=f(x)+f(-x)$，得 $\\int_{-1}^{1}[f(x)+f(-x)]^2\\,\\mathrm{d}x=0$，由连续性得 $f(x)+f(-x)\\equiv 0$，即 $f(x)$ 必为奇函数，C 正确。故不正确的是 D。',
})

E.append({
 'no': 6, 'type': '选择', 'subject': '高数', 'chapter': '多元函数微分学',
 'kp': '二元函数在 $(0,0)$ 处连续·偏导·可微的判定',
 'q': '关于函数 $f(x,y)=\\begin{cases} y\\sin\\dfrac{1}{x^2+y^2}, & x^2+y^2\\neq 0,\\\\[2pt] 0, & x^2+y^2=0\\end{cases}$，给出下列结论：① $f(x,y)$ 在点 $(0,0)$ 处连续；② $\\left.\\dfrac{\\partial f}{\\partial x}\\right|_{(0,0)}=0$；③ $\\left.\\dfrac{\\partial f}{\\partial y}\\right|_{(0,0)}=0$；④ $f(x,y)$ 在点 $(0,0)$ 处可微。其中正确的个数为（　）。\nA. 1　　B. 2　　C. 3　　D. 4',
 'ans': 'B（①②正确）',
 'sol': '$\\lim_{(x,y)\\to(0,0)}|f|\\le|y|=0=f(0,0)$，①正确；$f(\\Delta x,0)=0$，故 $\\left.\\dfrac{\\partial f}{\\partial x}\\right|_{(0,0)}=0$，②正确；$\\dfrac{f(0,\\Delta y)-f(0,0)}{\\Delta y}=\\sin\\dfrac{1}{\\Delta y^2}$ 当 $\\Delta y\\to 0$ 极限不存在，③错误；偏导不全存在必不可微，④错误。共 2 个正确，选 B。',
})

E.append({
 'no': 8, 'type': '选择', 'subject': '线代', 'chapter': '矩阵·伴随·正交',
 'kp': '代数余子式与 $A^T=A^*$、正交矩阵、可逆性判定',
 'q': '设 $E$ 为三阶单位矩阵，$A=(a_{ij})$ 为三阶非零实矩阵，$A_{ij}$ 是 $|A|$ 中元素 $a_{ij}$ 的代数余子式。若 $A_{ij}=a_{ij}$（$i,j=1,2,3$），则（　）。\nA. 矩阵 $A-E$ 不可逆\nB. 矩阵 $A-E$ 可逆\nC. 矩阵 $A+E$ 可逆\nD. 矩阵 $A+E$ 可逆',
 'ans': 'A',
 'note': '⚠️ 做题本此题 C、D 选项印重（均为「A+E 可逆」），森哥原卷 C/D 应为一对可逆/不可逆；以官方解析答案 A 为准。',
 'sol': '$A_{ij}=a_{ij}\\Rightarrow A^{T}=A^{*}$，于是 $AA^{T}=AA^{*}=|A|E$。取行列式得 $|A|^2=|A|^3$；又按行展开 $|A|=\\sum_j a_{ij}A_{ij}=\\sum_j a_{ij}^2>0$（$A$ 非零），故 $|A|=1$，即 $A$ 为正交矩阵。于是 $|A-E|=|A-AA^{T}|=|A|\\,|E-A^{T}|=|E-A|=-|A-E|$，得 $|A-E|=0$，即 $A-E$ 必不可逆，选 A。$A+E$ 的可逆性不确定：正交旋转阵时 $|A+E|>0$ 可逆，关于直线的反射阵（特征值 $1,-1,-1$）时 $|A+E|=0$。',
})

E.append({
 'no': 9, 'type': '选择', 'subject': '线代', 'chapter': '线性方程组·同解',
 'kp': '分块方程组同解、秩的等式 $r(A^T)=r(AA^T)$',
 'q': '设 $A$ 为 $n$ 阶实矩阵，$E$ 为 $n$ 阶单位矩阵，则（　）。\nA. 线性方程组 $\\begin{pmatrix}E&O\\\\O&A^{T}\\end{pmatrix}x=0$ 与 $\\begin{pmatrix}E&A^{T}\\\\A&O\\end{pmatrix}x=0$ 同解\nB. 线性方程组 $\\begin{pmatrix}E&O\\\\O&A\\end{pmatrix}x=0$ 与 $\\begin{pmatrix}E&A^{T}\\\\A&O\\end{pmatrix}x=0$ 同解\nC. 线性方程组 $\\begin{pmatrix}E&O\\\\O&A^{T}\\end{pmatrix}x=0$ 与 $\\begin{pmatrix}E&A^{T}\\\\A&A^{T}\\end{pmatrix}x=0$ 同解\nD. 线性方程组 $\\begin{pmatrix}E&O\\\\O&A\\end{pmatrix}x=0$ 与 $\\begin{pmatrix}E&A^{T}\\\\A&A^{T}\\end{pmatrix}x=0$ 同解',
 'ans': 'A',
 'sol': '把 $\\begin{pmatrix}E&A^{T}\\\\A&O\\end{pmatrix}$ 用分块初等行变换化为 $\\begin{pmatrix}E&A^{T}\\\\O&-AA^{T}\\end{pmatrix}$，与 $\\begin{pmatrix}E&A^{T}\\\\O&AA^{T}\\end{pmatrix}$ 行等价；而 $r(A^{T})=r(AA^{T})$ 保证 $A^{T}y=0$ 与 $AA^{T}y=0$ 同解。展开写：$\\begin{pmatrix}E&O\\\\O&A^{T}\\end{pmatrix}x=0$ 即 $x_1=0,\\ A^{T}x_2=0$；$\\begin{pmatrix}E&A^{T}\\\\A&O\\end{pmatrix}x=0$ 即 $x_1+A^{T}x_2=0,\\ Ax_1=0$，由 $x_1\\in N(A)$ 且 $A^{T}x_2=-x_1$ 有解知两解集一致，A 成立。B、C、D 可用特例否定（如二阶取 $E=\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix},A=\\begin{pmatrix}1&1\\\\0&0\\end{pmatrix}$，及 $A=E$）。',
})

E.append({
 'no': 12, 'type': '填空', 'subject': '高数', 'chapter': '一元函数微分学',
 'kp': '导数定义求 $f\'(1)$（含隐零因子）',
 'q': '设 $f(x)=(x^{2024}-1)\\arctan\\dfrac{2(x^2+1)}{1+2x^2+x^3}$，则 $f\'(1)=$ ______。',
 'ans': '$506\\pi$',
 'sol': '含 $\\arctan$ 复合因子的乘积在 $x=1$ 处求导，用导数定义最稳：$f\'(1)=\\lim_{x\\to 1}\\dfrac{f(x)-f(1)}{x-1}=\\lim_{x\\to 1}\\dfrac{x^{2024}-1}{x-1}\\cdot\\arctan\\dfrac{2(x^2+1)}{1+2x^2+x^3}=2024\\times\\arctan 1=2024\\times\\dfrac{\\pi}{4}=506\\pi$。其中 $x=1$ 时 arctan 项恰为 $\\arctan 1=\\dfrac{\\pi}{4}$。',
})

E.append({
 'no': 14, 'type': '填空', 'subject': '高数', 'chapter': '定积分·几何应用',
 'kp': '参数曲线绕 $y$ 轴旋转的旋转曲面侧面积',
 'q': '设 $C$ 为曲线 $\\begin{cases}x=\\ln(1+t^2),\\\\ y=2\\arctan t-t\\end{cases}$ 上从 $t=0$ 到 $t=1$ 之间的一段弧，则曲线 $C$ 绕 $y$ 轴旋转一周所得到的旋转曲面的侧面积 $S=$ ______。',
 'ans': '$\\pi(\\pi+2\\ln 2-4)$',
 'sol': '绕 $y$ 轴：$S_y=2\\pi\\int_a^b x(t)\\sqrt{x\'^2(t)+y\'^2(t)}\\,\\mathrm{d}t$。$x\'=\\dfrac{2t}{1+t^2}$，$y\'=\\dfrac{2}{1+t^2}-1=\\dfrac{1-t^2}{1+t^2}$，$\\sqrt{x\'^2+y\'^2}=\\dfrac{\\sqrt{4t^2+(1-t^2)^2}}{1+t^2}=\\dfrac{1+t^2}{1+t^2}=1$，故 $S=2\\pi\\int_0^1\\ln(1+t^2)\\,\\mathrm{d}t=2\\pi\\left[t\\ln(1+t^2)-2t+2\\arctan t\\right]_0^1=2\\pi\\left(\\ln 2-2+\\dfrac{\\pi}{2}\\right)=\\pi(\\pi+2\\ln 2-4)$。',
})

E.append({
 'no': 16, 'type': '填空', 'subject': '线代', 'chapter': '二次型·规范形',
 'kp': '规范形定惯性指数、由特征值定参数',
 'q': '若三元实二次型 $f(x_1,x_2,x_3)=ax_1^2+ax_2^2+(a-1)x_3^2+2x_1x_3-2x_2x_3$ 的规范形为 $y_1^2+y_2^2$，则 $a=$ ______。',
 'ans': '$2$',
 'sol': '二次型矩阵 $A=\\begin{pmatrix}a&0&1\\\\0&a&-1\\\\1&-1&a-1\\end{pmatrix}$，$\\det(A-\\lambda E)$ 按第一行展开因式分解得 $\\lambda$ 的三次式 $-(\\lambda-a)(\\lambda-a+2)(\\lambda-a-1)$，即特征值为 $a,\\ a-2,\\ a+1$。规范形 $y_1^2+y_2^2$ 表示正惯性指数为 2、负惯性指数为 0，即特征值两正一零，故 $a-2=0$，得 $a=2$（此时特征值为 $0,2,3$）。',
})

sr = [s for s in d['series'] if s['id'] == 'yb24'][0]
v1 = sr['vols'][0]
assert v1['vol'] == 1
if v1['errors']:
    print('vol1 already has errors, abort'); sys.exit(1)
v1['errors'] = sorted(E, key=lambda e: e['no'])
v1['sol_checked'] = '森哥五套卷数二.pdf 模拟一答案解析 p9-p13'

io.open(P, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
print('vol1 errors:', [(e['no'], e['type']) for e in v1['errors']])
